#!/usr/bin/env python3
"""
FortiCNAPP / Lacework — Azure pre-PoV sizing (standalone single-file edition)
=============================================================================
Version: v6 (2026-05-18)

Produces the metric that drives FortiCNAPP licensing: **average vCPU per
month** across your Azure estate, over a configurable retroactive window
(default: last 12 completed months).

This is a single-file extract of the `forticnapp-sizing` tool, packaged as
one script so it can be reviewed and run without cloning a repository.

────────────────────────────────────────────────────────────────────────────
WHAT CHANGED IN v6 vs v4/v5
────────────────────────────────────────────────────────────────────────────
- Azure Cost Management no longer accepts `UnitOfMeasure` as a query
  grouping dimension (the API returns BadRequest at every scope). v6 stops
  asking for it and infers hour-vs-second from the meter name instead
  (`Duration`/`Second` → seconds; everything else → hours).
- App Service Premium / Isolated and Functions Premium plan SKUs now
  translate to vCPU via an explicit table (P1V3, I3V2, EP2, …) since the
  meter name carries the plan, not the vCPU count.
- nextLink pagination now re-sends the QueryDefinition body (was empty),
  fixing the 429-after-first-page issue on large MG queries.
- Retry-with-backoff on 408/429/5xx honouring the Retry-After header.
- New `--throttle <sec>` to space out per-subscription queries on big
  tenants (default 0.5s; raise to 1.5–2 on large MGs if 429s persist).
- JSON output now includes `accounts`, `subs_queried_ok`, `subs_skipped`
  and `unmapped_meters` for easier diagnosis of partial runs.

────────────────────────────────────────────────────────────────────────────
WHY vCPU-HOUR INSTEAD OF "VM COUNT"
────────────────────────────────────────────────────────────────────────────
FortiCNAPP is sold by average vCPU-hour consumed per month. A snapshot
("how many VMs do you have right now?") can be off by 4× in either
direction depending on autoscaling, dev/test schedules, batch jobs, and
seasonality. This script reads from Azure Cost Management billing data,
so the numbers reflect actual consumption — including spot, autoscale,
ephemeral and seasonal workloads.

────────────────────────────────────────────────────────────────────────────
WHAT YOU GET (output)
────────────────────────────────────────────────────────────────────────────
Two files written to the chosen --output directory:

  azure_sizing_<scope>_billing_<coverage>_<start>_<end>.csv
      Long format, one row per (month, subscription, service).

  azure_sizing_<scope>_billing_<coverage>_<start>_<end>.json
      Same data plus aggregates:
        - headline_avg_vcpu_yearly        ← THE LICENSING NUMBER
        - headline_peak_month_avg_vcpu
        - monthly: per-month avg vCPU + by_service breakdown
        - growth: MoM, CAGR, YoY, OLS trend slope
        - notes: caveats from the run (unknown SKUs, etc.)

────────────────────────────────────────────────────────────────────────────
PERMISSIONS REQUIRED
────────────────────────────────────────────────────────────────────────────
Two roles, both READ-ONLY:

  1. Cost Management read at the chosen scope:
     - "Cost Management Reader" (or higher) on the scope. The scope is one of:
        - A management group:   /providers/Microsoft.Management/managementGroups/<id>
        - A billing account:    /providers/Microsoft.Billing/billingAccounts/<id>
        - A subscription:       /subscriptions/<id>
     - The billing-account or root-management-group scope is preferred —
       one query covers the whole tenant.

  2. "Reader" on at least one subscription so we can resolve VM sizes
     (Standard_D8s_v5 → 8 vCPU) from Microsoft.Compute/skus. No data
     is read; only the size catalogue.

The script does NOT write to any resource. It does not deploy agents,
modify configuration, or read workload contents.

────────────────────────────────────────────────────────────────────────────
SETUP
────────────────────────────────────────────────────────────────────────────
Python 3.10 or newer.

  pip install azure-identity azure-mgmt-costmanagement \\
              azure-mgmt-resourcegraph azure-mgmt-compute \\
              azure-mgmt-subscription

Auth — any one of these works (DefaultAzureCredential):

  # Interactive
  az login

  # Service principal
  export AZURE_CLIENT_ID=...
  export AZURE_CLIENT_SECRET=...
  export AZURE_TENANT_ID=...

  # Managed identity (when running inside Azure)
  # — picked up automatically.

────────────────────────────────────────────────────────────────────────────
USAGE
────────────────────────────────────────────────────────────────────────────
Whole tenant via management group (preferred):

  python forticnapp_azure_sizing.py \\
      --management-group <root-mg-or-tenant-id> \\
      --output ./out

Whole enrolment via billing account:

  python forticnapp_azure_sizing.py \\
      --billing-account <billing-account-id> \\
      --output ./out

Specific subscriptions:

  python forticnapp_azure_sizing.py \\
      --subscriptions <sub-id-1> <sub-id-2> \\
      --output ./out

Different window (default = last 12 completed months):

  python forticnapp_azure_sizing.py \\
      --management-group <id> \\
      --start 2025-05 --end 2026-04 \\
      --output ./out

Coverage:
  --coverage extended  (default) — VM, VMSS, ACI, Container Apps,
                       App Service Premium, Functions Premium,
                       AKS Virtual Nodes, SQL/PostgreSQL/MySQL vCores
  --coverage parity              — VM and VMSS only

Operational fallback (if billing access is genuinely unavailable):

  python forticnapp_azure_sizing.py --mode operational \\
      --subscriptions <sub-id> \\
      --output ./out

  Operational mode is a Resource Graph snapshot extrapolated to a full
  month. It misses autoscaling and dev/test schedules; use --mode billing
  whenever possible.

────────────────────────────────────────────────────────────────────────────
WHAT TO RETURN
────────────────────────────────────────────────────────────────────────────
Send back the JSON and CSV files written under --output. They are
self-contained — no separate config, secrets or PII.
"""
from __future__ import annotations

import argparse
import calendar
import csv
import json
import logging
import math
import re
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from functools import cache
from pathlib import Path
from typing import Callable, Optional

# ------------------------------------------------------------------ azure SDKs
try:
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.compute import ComputeManagementClient
    from azure.mgmt.costmanagement import CostManagementClient
    from azure.mgmt.costmanagement.models import (
        QueryAggregation,
        QueryDataset,
        QueryDefinition,
        QueryGrouping,
        QueryTimePeriod,
        TimeframeType,
    )
    from azure.mgmt.resourcegraph import ResourceGraphClient
    from azure.mgmt.resourcegraph.models import QueryRequest
    from azure.mgmt.subscription import SubscriptionClient
except ImportError as e:
    sys.stderr.write(
        f"Missing Azure SDK: {e}\n"
        "Run: pip install azure-identity azure-mgmt-costmanagement "
        "azure-mgmt-resourcegraph azure-mgmt-compute azure-mgmt-subscription\n"
    )
    sys.exit(2)

log = logging.getLogger("forticnapp_azure_sizing")


# ============================================================================
# Time-window helpers
# ============================================================================

@dataclass(frozen=True)
class MonthWindow:
    """Inclusive [start, end] window of calendar months, UTC-aligned."""

    start: date  # day=1
    end: date    # day=1 of the last month included

    def months(self) -> list[date]:
        out: list[date] = []
        cur = self.start
        while cur <= self.end:
            out.append(cur)
            cur = _add_month(cur)
        return out

    @property
    def start_iso(self) -> str:
        return f"{self.start.year:04d}-{self.start.month:02d}"

    @property
    def end_iso(self) -> str:
        return f"{self.end.year:04d}-{self.end.month:02d}"

    @classmethod
    def parse(cls, start: Optional[str], end: Optional[str]) -> "MonthWindow":
        end_d = _parse_yyyy_mm(end) if end else _shift_months(_today_month_first(), -1)
        start_d = _parse_yyyy_mm(start) if start else _shift_months(end_d, -11)
        if start_d > end_d:
            raise ValueError(f"start ({start_d}) is after end ({end_d})")
        return cls(start=start_d, end=end_d)


def hours_in_month(d: date) -> int:
    days = calendar.monthrange(d.year, d.month)[1]
    return days * 24


def _add_month(d: date) -> date:
    if d.month == 12:
        return date(d.year + 1, 1, 1)
    return date(d.year, d.month + 1, 1)


def _shift_months(d: date, delta: int) -> date:
    total = d.year * 12 + (d.month - 1) + delta
    y, m = divmod(total, 12)
    return date(y, m + 1, 1)


def _parse_yyyy_mm(s: str) -> date:
    parts = s.strip().split("-")
    if len(parts) != 2:
        raise ValueError(f"expected YYYY-MM, got {s!r}")
    y, m = int(parts[0]), int(parts[1])
    if not 1 <= m <= 12:
        raise ValueError(f"invalid month: {s!r}")
    return date(y, m, 1)


def _today_month_first() -> date:
    today = datetime.now(timezone.utc).date()
    return date(today.year, today.month, 1)


# ============================================================================
# Data models
# ============================================================================

@dataclass(frozen=True)
class UsageRow:
    month: date
    account_id: str
    account_name: str
    service: str
    vcpu_hours: float

    @property
    def avg_vcpu(self) -> float:
        return self.vcpu_hours / hours_in_month(self.month) if self.vcpu_hours else 0.0

    @property
    def month_iso(self) -> str:
        return f"{self.month.year:04d}-{self.month.month:02d}"


@dataclass
class SizingReport:
    cloud: str
    mode: str
    coverage: str
    window: MonthWindow
    rows: list[UsageRow] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    # (MeterCategory, MeterSubCategory, Meter) tuples that arrived under one of
    # the categories we care about but did NOT match any classification rule.
    # Used to surface coverage gaps to the operator without having to re-run.
    unmapped_meters: set[tuple[str, str, str]] = field(default_factory=set)
    # Per-subscription state: which ones returned rows and which failed.
    subs_queried_ok: set[str] = field(default_factory=set)
    subs_skipped: list[tuple[str, str]] = field(default_factory=list)

    def add(self, row: UsageRow) -> None:
        self.rows.append(row)

    def headline_yearly_avg_vcpu(self) -> float:
        if not self.rows:
            return 0.0
        total_hours = sum(hours_in_month(m) for m in self.window.months())
        total_vcpu_h = sum(r.vcpu_hours for r in self.rows)
        return total_vcpu_h / total_hours if total_hours else 0.0

    def headline_peak_month_avg_vcpu(self) -> float:
        if not self.rows:
            return 0.0
        by_month: dict[date, float] = {}
        for r in self.rows:
            by_month[r.month] = by_month.get(r.month, 0.0) + r.vcpu_hours
        return max(
            (h / hours_in_month(m) for m, h in by_month.items()),
            default=0.0,
        )


# ============================================================================
# VM SKU → vCPU catalogue (from Microsoft.Compute/skus)
# ============================================================================

@cache
def _sku_table(subscription_id: str) -> dict[str, int]:
    """Build {normalized_size_name: vCPUs} from Microsoft.Compute/skus."""
    cred = DefaultAzureCredential()
    client = ComputeManagementClient(cred, subscription_id)
    table: dict[str, int] = {}
    for sku in client.resource_skus.list():
        if sku.resource_type != "virtualMachines":
            continue
        if not sku.name or not sku.capabilities:
            continue
        v = None
        for cap in sku.capabilities:
            if cap.name == "vCPUs":
                try:
                    v = int(cap.value)
                except (TypeError, ValueError):
                    pass
                break
        if v is None:
            continue
        for variant in _name_variants(sku.name):
            table[variant] = v
    log.info("indexed %d VM size variants", len(table))
    return table


def _name_variants(raw: str) -> list[str]:
    out = [raw]
    bare = raw.removeprefix("Standard_") if raw.startswith("Standard_") else raw
    out.append(bare)
    out.append(bare.replace("_", " "))
    return out


def vcpus_for_size(size: str, subscription_id: str) -> Optional[int]:
    if not size:
        return None
    table = _sku_table(subscription_id)
    for candidate in (
        size,
        size.replace(" ", "_"),
        size.replace("_", " "),
        f"Standard_{size.replace(' ', '_')}",
    ):
        v = table.get(candidate)
        if v is not None:
            return v
    return None


# ============================================================================
# Service classification — Cost Management meter rows → (service, vCPU-hours)
# ============================================================================

PARITY_SERVICES = {"VM", "VMSS"}
EXTENDED_EXTRA = {
    "ContainerInstances", "ContainerApps", "AppService", "FunctionsPremium",
    "AKSVirtualNodes", "SQLDatabase", "PostgreSQL", "MySQL",
}

# Cost Management meter names whose quantity is expressed in vCPU-seconds.
# Identified by substring match on the Meter name (case-insensitive).
_SECOND_METER_HINTS = ("duration", "second")

# App Service Premium / Isolated plan -> vCPU count. Used to translate meter
# names like "P1V3 App" into a vCPU-per-hour figure since the Meter dimension
# carries the SKU, not the vCPU count, and Azure no longer exposes
# UnitOfMeasure as a query dimension.
_APPSERVICE_PLAN_VCPUS: dict[str, int] = {
    # PremiumV2
    "P1V2": 1, "P2V2": 2, "P3V2": 4,
    # PremiumV3
    "P0V3": 1, "P1V3": 2, "P2V3": 4, "P3V3": 8,
    "P1MV3": 2, "P2MV3": 4, "P3MV3": 8, "P4MV3": 16, "P5MV3": 32,
    # PremiumV4
    "P0V4": 1, "P1V4": 2, "P2V4": 4, "P3V4": 8,
    "P1MV4": 2, "P2MV4": 4, "P3MV4": 8, "P4MV4": 16, "P5MV4": 32,
    # Isolated v2 / v3
    "I1V2": 2, "I2V2": 4, "I3V2": 8,
    "I1MV2": 2, "I2MV2": 4, "I3MV2": 8, "I4MV2": 16, "I5MV2": 32, "I6MV2": 64,
}

_APPSERVICE_PLAN_RE = re.compile(
    r"\b(P[0-9]M?V[2-4]|I[1-9]M?V[23])\b", re.IGNORECASE,
)

# Functions Premium per-instance meters (e.g. "EP1 Instance", "EP2 App").
# The Meter dimension carries the plan SKU; vCPU count must be inferred.
_FUNCTIONS_PREMIUM_PLAN_VCPUS: dict[str, int] = {
    "EP1": 1, "EP2": 2, "EP3": 4,
}
_FUNCTIONS_PREMIUM_PLAN_RE = re.compile(r"\b(EP[123])\b", re.IGNORECASE)


@dataclass
class Classification:
    service: str
    vcpu_hours: float
    note: Optional[str] = None


def _meter_is_in_seconds(meter: str) -> bool:
    """Heuristic: meters whose quantity is in vCPU-seconds.

    Cost Management names these consistently across services — `Standard
    vCPU Duration`, `vCPU Duration`, `vCPU Active Time`, etc. Hour-billed
    meters never contain those tokens. Used to compensate for the absence
    of the UnitOfMeasure dimension in the Query API response.
    """
    ml = (meter or "").lower()
    return any(h in ml for h in _SECOND_METER_HINTS)


def classify_vm_row(
    meter_subcategory: str,
    meter: str,
    usage_quantity: float,
    unit: str,  # ignored — UnitOfMeasure is no longer available as a dimension; kept for signature compatibility
    vcpu_lookup: Callable[[str], Optional[int]],
) -> Optional[Classification]:
    if usage_quantity <= 0:
        return None
    size = re.sub(r"\s*(Spot|Low Priority)\s*$", "", meter or "").strip()
    if not size:
        return None
    # VM compute meters are billed per hour. Skip any oddball seconds-based
    # meter that might sneak in (none observed in practice, but cheap to guard).
    if _meter_is_in_seconds(size):
        return None
    vcpus = vcpu_lookup(size)
    if vcpus is None:
        return Classification("VM", 0.0, note=f"unknown VM size '{size}' ({meter_subcategory})")
    return Classification("VM", vcpus * usage_quantity)


def _appservice_vcpus_for_meter(meter: str) -> Optional[int]:
    if not meter:
        return None
    mt = meter.upper().replace(" ", "")
    if mt in _APPSERVICE_PLAN_VCPUS:
        return _APPSERVICE_PLAN_VCPUS[mt]
    match = _APPSERVICE_PLAN_RE.search(meter or "")
    if match:
        key = match.group(1).upper()
        return _APPSERVICE_PLAN_VCPUS.get(key)
    return None


def classify_other_row(
    meter_category: str,
    meter_subcategory: str,
    meter: str,
    usage_quantity: float,
    unit: str,  # ignored — UnitOfMeasure is no longer available as a dimension; kept for signature compatibility
) -> Optional[Classification]:
    """Classify a non-VM Cost Management row into (service, vcpu-hours).

    Without the UnitOfMeasure dimension the unit must be inferred from the
    meter name: meters containing 'Duration' or 'Second' carry vCPU-seconds,
    everything else is treated as vCPU-hours.
    """
    if usage_quantity <= 0:
        return None
    cat = meter_category or ""
    m = meter or ""
    sub = meter_subcategory or ""

    def _to_vcpu_hours(qty: float) -> float:
        return qty / 3600.0 if _meter_is_in_seconds(m) else qty

    if cat == "Container Instances":
        if "vCPU" in m:
            return Classification("ContainerInstances", _to_vcpu_hours(usage_quantity))
        return None

    if cat == "Container Apps":
        # Container Apps bills vCPU exclusively in seconds (vCPU Duration /
        # Active vCPU Duration). Treat any vCPU-bearing meter as such.
        if "vCPU" in m:
            return Classification("ContainerApps", usage_quantity / 3600.0)
        return None

    if cat == "Functions" and sub.startswith("Premium"):
        if "vCPU" in m:
            return Classification("FunctionsPremium", _to_vcpu_hours(usage_quantity))
        # Per-instance plan meters (e.g. "EP1 Instance"): no vCPU substring,
        # vCPU count must come from the SKU.
        match = _FUNCTIONS_PREMIUM_PLAN_RE.search(m)
        if match:
            v = _FUNCTIONS_PREMIUM_PLAN_VCPUS.get(match.group(1).upper())
            if v is not None:
                return Classification("FunctionsPremium", v * usage_quantity)
        return None

    if cat == "Azure App Service":
        # The meter does not contain "vCPU"; the SKU (P1V3, I3V2, …) does.
        v = _appservice_vcpus_for_meter(m)
        if v is None:
            return None
        # App Service plan SKU meters are billed per hour.
        return Classification("AppService", v * usage_quantity)

    if cat == "Azure Kubernetes Service":
        if sub.lower().startswith("virtual node") and "vCPU" in m:
            return Classification("AKSVirtualNodes", _to_vcpu_hours(usage_quantity))
        return None

    if cat == "SQL Database" and "vCore" in m:
        return Classification("SQLDatabase", usage_quantity)
    if cat == "Azure Database for PostgreSQL" and "vCore" in m:
        return Classification("PostgreSQL", usage_quantity)
    if cat == "Azure Database for MySQL" and "vCore" in m:
        return Classification("MySQL", usage_quantity)
    return None


def is_in_coverage(service: str, coverage: str) -> bool:
    if coverage == "parity":
        return service in PARITY_SERVICES
    return service in PARITY_SERVICES or service in EXTENDED_EXTRA


# ============================================================================
# Billing-mode collector — Cost Management Query API
# ============================================================================

# Cost Management Query API quotas are tight (per-tenant QPU, per-client RPS).
# Both the initial SDK call and the manual nextLink POSTs can return 429 with a
# Retry-After header. Honour it instead of giving up.
_RETRYABLE_STATUSES = {408, 429, 500, 502, 503, 504}
_DEFAULT_RETRY_AFTER = 30.0
_MAX_RETRY_AFTER = 120.0
_MAX_RETRIES = 6


def _parse_retry_after(headers) -> Optional[float]:
    if headers is None:
        return None
    val = None
    try:
        val = headers.get("Retry-After")
        if val is None:
            val = headers.get("retry-after")
    except Exception:
        return None
    if not val:
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def _sdk_call_with_retry(call: Callable[[], object], *, what: str) -> object:
    """Call an Azure SDK operation, retrying on 429/5xx with Retry-After."""
    from azure.core.exceptions import HttpResponseError
    delay = 5.0
    last_exc: Optional[Exception] = None
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            return call()
        except HttpResponseError as exc:
            status = getattr(exc, "status_code", None) or (
                getattr(exc.response, "status_code", None) if getattr(exc, "response", None) else None
            )
            if status not in _RETRYABLE_STATUSES or attempt == _MAX_RETRIES:
                raise
            ra = _parse_retry_after(getattr(getattr(exc, "response", None), "headers", None))
            wait = min(ra if ra is not None else delay, _MAX_RETRY_AFTER)
            log.warning(
                "%s -> %s, retrying in %.1fs (attempt %d/%d)",
                what, status, wait, attempt, _MAX_RETRIES,
            )
            time.sleep(wait)
            delay = min(delay * 2, _MAX_RETRY_AFTER)
            last_exc = exc
    if last_exc is not None:
        raise last_exc
    return None


def _post_next_link_with_retry(client, next_link: str, body_json: Optional[str]) -> dict:
    """POST to a Cost Management nextLink, retrying on 429/5xx with Retry-After."""
    from azure.core.rest import HttpRequest
    headers = {"Content-Type": "application/json"} if body_json else {}
    delay = 5.0
    for attempt in range(1, _MAX_RETRIES + 1):
        req = HttpRequest("POST", next_link, headers=headers, content=body_json)
        http_resp = client._client.send_request(req)
        status = http_resp.status_code
        if status < 400:
            try:
                return http_resp.json() or {}
            except Exception:
                return {}
        if status in _RETRYABLE_STATUSES and attempt < _MAX_RETRIES:
            ra = _parse_retry_after(http_resp.headers)
            wait = min(ra if ra is not None else delay, _MAX_RETRY_AFTER)
            log.warning(
                "nextLink POST -> %s, retrying in %.1fs (attempt %d/%d)",
                status, wait, attempt, _MAX_RETRIES,
            )
            time.sleep(wait)
            delay = min(delay * 2, _MAX_RETRY_AFTER)
            continue
        http_resp.raise_for_status()
    return {}


def collect_billing(
    credential: DefaultAzureCredential,
    scope: str,
    sku_subscription_id: str,
    window: MonthWindow,
    coverage: str,
) -> SizingReport:
    client = CostManagementClient(credential)
    report = SizingReport(cloud="azure", mode="billing", coverage=coverage, window=window)

    rows = _query_scope(client, scope, window)
    log.info("billing: %d raw meter rows from %s", len(rows), scope)

    def vlookup(s: str) -> Optional[int]:
        return vcpus_for_size(s, sku_subscription_id)

    for r in rows:
        sub_id = r.get("SubscriptionId") or r.get("SubscriptionGuid") or scope.split("/")[-1]
        sub_name = r.get("SubscriptionName") or sub_id
        category = r.get("MeterCategory") or ""
        sub_cat = r.get("MeterSubCategory") or ""
        meter = r.get("Meter") or ""
        unit = r.get("UnitOfMeasure") or ""
        qty = float(r.get("UsageQuantity") or r.get("totalQty") or 0.0)
        month_start = _parse_month(r.get("UsageDate") or r.get("BillingMonth") or "")
        if month_start is None:
            continue

        if category == "Virtual Machines":
            cls = classify_vm_row(sub_cat, meter, qty, unit, vlookup)
        else:
            cls = classify_other_row(category, sub_cat, meter, qty, unit)

        # Surface meters that fell through classification but came from a
        # category we said we'd cover AND look like compute (vCPU / Core /
        # plan-SKU pattern). Filtering by the compute hint keeps Memory /
        # Storage / Network meters out of the noise.
        if (
            cls is None
            and category in _COVERED_CATEGORIES
            and qty > 0
            and _meter_looks_like_compute(category, meter)
        ):
            report.unmapped_meters.add((category, sub_cat, meter))
            continue

        if cls is None or not is_in_coverage(cls.service, coverage):
            continue
        if cls.note:
            report.notes.append(f"{sub_id} {month_start}: {cls.note}")
        if cls.vcpu_hours <= 0:
            continue
        report.add(UsageRow(
            month=month_start,
            account_id=sub_id,
            account_name=sub_name,
            service=cls.service,
            vcpu_hours=cls.vcpu_hours,
        ))

    _aggregate_inplace(report)
    return report


# MeterCategory values whose unmapped meters are worth surfacing back to the
# operator. Anything else (Storage, Networking, etc.) is correctly ignored.
_COVERED_CATEGORIES = {
    "Virtual Machines",
    "Container Instances",
    "Container Apps",
    "Functions",
    "Azure App Service",
    "Azure Kubernetes Service",
    "SQL Database",
    "Azure Database for PostgreSQL",
    "Azure Database for MySQL",
}

# Heuristic: tokens that appear in compute meters but not in memory / storage /
# network meters. Used to filter the `unmapped_meters` diagnostic so we don't
# report e.g. "Container Instances / Memory Duration" as a coverage gap.
_COMPUTE_METER_HINTS = ("vcpu", "vcore", " core", "cpu")
_PLAN_SKU_HINTS_RE = re.compile(r"\b(?:P[0-9]M?V[2-4]|I[1-9]M?V[23]|EP[123])\b", re.IGNORECASE)


def _meter_looks_like_compute(category: str, meter: str) -> bool:
    """Return True if a meter under a covered category looks like compute.

    Used to filter the `unmapped_meters` diagnostic. False positives here are
    cheap (a memory meter showing as a "gap"); false negatives are costly (a
    real compute SKU silently ignored). When in doubt, lean toward True.
    """
    if not meter:
        return False
    if category == "Virtual Machines":
        # Every VM compute meter carries a SKU name, which is what we
        # ultimately look up. The only common non-compute things under
        # this category are "Managed Disks" or similar (already filtered
        # by being a different MeterCategory). Default to True here.
        return True
    if category == "Azure App Service":
        return bool(_PLAN_SKU_HINTS_RE.search(meter))
    if category == "Functions":
        return bool(_PLAN_SKU_HINTS_RE.search(meter)) or "vcpu" in meter.lower()
    ml = meter.lower()
    return any(h in ml for h in _COMPUTE_METER_HINTS)


def _query_scope(client: CostManagementClient, scope: str, window: MonthWindow) -> list[dict]:
    """Issue a Cost Management Usage query, paginating via nextLink.

    Cost Management Query API rules we have to dance around:
      - "to" cannot exceed start + 1 year at MG / billing-account scope. We
        use the last day of the end month at 23:00:00 UTC, which stays
        strictly under 365 days for any 12-month window.
      - "UnitOfMeasure" is NOT a valid grouping dimension. Azure rejects it
        at every scope (including subscription) with a BadRequest listing
        the allowed dimensions. We classify by Meter / MeterSubCategory /
        MeterCategory only, and infer hour vs second from the meter name
        (see classify_other_row).
      - Pagination is done by POSTing to nextLink with the SAME
        QueryDefinition body. POSTing nextLink with no body returns
        400 / empty.
    """
    start_dt = datetime(window.start.year, window.start.month, 1, tzinfo=timezone.utc)
    last_day = calendar.monthrange(window.end.year, window.end.month)[1]
    end_dt = datetime(
        window.end.year, window.end.month, last_day, 23, 0, 0, tzinfo=timezone.utc,
    )

    grouping = [
        QueryGrouping(type="Dimension", name="SubscriptionId"),
        QueryGrouping(type="Dimension", name="MeterCategory"),
        QueryGrouping(type="Dimension", name="MeterSubCategory"),
        QueryGrouping(type="Dimension", name="Meter"),
    ]

    definition = QueryDefinition(
        type="Usage",
        timeframe=TimeframeType.CUSTOM,
        time_period=QueryTimePeriod(from_property=start_dt, to=end_dt),
        dataset=QueryDataset(
            granularity="Monthly",
            aggregation={"totalQty": QueryAggregation(name="UsageQuantity", function="Sum")},
            grouping=grouping,
        ),
    )

    # Serialize once — reused as the POST body for every nextLink page.
    try:
        body_dict = definition.serialize(keep_readonly=True)
    except Exception:
        body_dict = None
    body_json = json.dumps(body_dict) if body_dict is not None else None

    out: list[dict] = []
    resp = _sdk_call_with_retry(
        lambda: client.query.usage(scope=scope, parameters=definition),
        what=f"query.usage({scope})",
    )
    cols = [c.name for c in (resp.columns or [])]
    for row in resp.rows or []:
        out.append({col: row[i] for i, col in enumerate(cols) if i < len(row)})
    next_link = getattr(resp, "next_link", None)

    pages = 1
    while next_link and pages < 50:
        pages += 1
        body = _post_next_link_with_retry(client, next_link, body_json)
        props = body.get("properties", body) if isinstance(body, dict) else {}
        cols = [c["name"] for c in props.get("columns", [])]
        for row in props.get("rows", []) or []:
            out.append({c: row[i] for i, c in enumerate(cols) if i < len(row)})
        next_link = props.get("nextLink")
    if next_link:
        log.warning(
            "aborting Cost Management pagination after %d pages — results may be truncated",
            pages,
        )
    log.info("Cost Management: collected %d row(s) over %d page(s) from %s", len(out), pages, scope)
    return out


def _parse_month(s) -> Optional[date]:
    if isinstance(s, str) and len(s) >= 7:
        try:
            if "-" in s:
                y, m = s[:4], s[5:7]
                return date(int(y), int(m), 1)
            if s.isdigit() and len(s) == 8:
                return date(int(s[:4]), int(s[4:6]), 1)
        except ValueError:
            return None
    if isinstance(s, (int, float)):
        as_int = int(s)
        if as_int >= 19700101:
            year = as_int // 10000
            month = (as_int // 100) % 100
            if 1 <= month <= 12:
                return date(year, month, 1)
    return None


def _aggregate_inplace(report: SizingReport) -> None:
    bucket: dict[tuple[date, str, str], UsageRow] = {}
    for r in report.rows:
        key = (r.month, r.account_id, r.service)
        if key in bucket:
            existing = bucket[key]
            bucket[key] = UsageRow(
                month=existing.month,
                account_id=existing.account_id,
                account_name=existing.account_name or r.account_name,
                service=existing.service,
                vcpu_hours=existing.vcpu_hours + r.vcpu_hours,
            )
        else:
            bucket[key] = r
    report.rows = list(bucket.values())


# ============================================================================
# Operational fallback — Resource Graph snapshot
# ============================================================================

VM_QUERY = """
Resources
| where type =~ 'microsoft.compute/virtualmachines'
| extend powerState = tostring(properties.extended.instanceView.powerState.code)
| where powerState == 'PowerState/running'
| project subscriptionId, vmSize = tostring(properties.hardwareProfile.vmSize)
| summarize count_=count() by subscriptionId, vmSize
"""

VMSS_QUERY = """
Resources
| where type =~ 'microsoft.compute/virtualmachinescalesets'
| extend capacity = toint(sku.capacity), vmSize = tostring(sku.name)
| project subscriptionId, vmSize, capacity
| summarize total=sum(capacity) by subscriptionId, vmSize
"""


def collect_operational(
    credential: DefaultAzureCredential,
    subscription_ids: list[str],
    subscription_names: dict[str, str],
    window: MonthWindow,
    coverage: str,
    sku_subscription_id: str,
) -> SizingReport:
    report = SizingReport(cloud="azure", mode="operational", coverage=coverage, window=window)
    if coverage == "extended":
        report.notes.append(
            "Extended coverage (ACI/Container Apps/AppService/SQL/PostgreSQL/MySQL/...) "
            "is only available in --mode billing. Operational covers VM and VMSS only."
        )
    report.notes.append(
        "Operational mode is a snapshot extrapolated to a full month. "
        "Use --mode billing for true retroactive measurement."
    )

    client = ResourceGraphClient(credential)

    if is_in_coverage("VM", coverage):
        for r in _rg_query(client, VM_QUERY, subscription_ids):
            sub_id = r.get("subscriptionId") or ""
            size = r.get("vmSize") or ""
            count = int(r.get("count_") or 0)
            v = vcpus_for_size(size, sku_subscription_id) if size else None
            if v is None or count <= 0:
                if size:
                    report.notes.append(f"{sub_id}: unknown VM size '{size}'")
                continue
            for month in window.months():
                report.add(UsageRow(
                    month=month,
                    account_id=sub_id,
                    account_name=subscription_names.get(sub_id, sub_id),
                    service="VM",
                    vcpu_hours=v * count * hours_in_month(month),
                ))

    if is_in_coverage("VMSS", coverage):
        for r in _rg_query(client, VMSS_QUERY, subscription_ids):
            sub_id = r.get("subscriptionId") or ""
            size = r.get("vmSize") or ""
            total = int(r.get("total") or 0)
            v = vcpus_for_size(size, sku_subscription_id) if size else None
            if v is None or total <= 0:
                if size:
                    report.notes.append(f"{sub_id}: unknown VMSS size '{size}'")
                continue
            for month in window.months():
                report.add(UsageRow(
                    month=month,
                    account_id=sub_id,
                    account_name=subscription_names.get(sub_id, sub_id),
                    service="VMSS",
                    vcpu_hours=v * total * hours_in_month(month),
                ))

    return report


def _rg_query(client: ResourceGraphClient, query: str, subscriptions: list[str]) -> list[dict]:
    out: list[dict] = []
    skip_token = None
    while True:
        opts = {"$top": 1000}
        if skip_token:
            opts["$skipToken"] = skip_token
        req = QueryRequest(subscriptions=subscriptions, query=query, options=opts)
        resp = client.resources(req)
        rows = resp.data or []
        if isinstance(rows, dict) and "rows" in rows and "columns" in rows:
            cols = [c["name"] for c in rows["columns"]]
            for row in rows["rows"]:
                out.append({cols[i]: row[i] for i in range(len(cols))})
        else:
            for r in rows:
                out.append(dict(r))
        skip_token = getattr(resp, "skip_token", None)
        if not skip_token:
            break
    return out


# ============================================================================
# Growth analytics
# ============================================================================

@dataclass(frozen=True)
class GrowthMetrics:
    series: list[tuple[str, float]]
    mom_growth_pct: list[tuple[str, Optional[float]]]
    mom_avg_pct: Optional[float]
    cagr_monthly_pct: Optional[float]
    yoy_growth_pct: Optional[float]
    trend_slope_per_month: Optional[float]
    r_squared: Optional[float]

    def to_dict(self) -> dict:
        return {
            "series": [{"month": m, "avg_vcpu": round(v, 4)} for m, v in self.series],
            "mom_growth_pct": [
                {"month": m, "mom_pct": (round(v, 2) if v is not None else None)}
                for m, v in self.mom_growth_pct
            ],
            "mom_avg_pct": round(self.mom_avg_pct, 2) if self.mom_avg_pct is not None else None,
            "cagr_monthly_pct": round(self.cagr_monthly_pct, 2) if self.cagr_monthly_pct is not None else None,
            "yoy_growth_pct": round(self.yoy_growth_pct, 2) if self.yoy_growth_pct is not None else None,
            "trend_slope_per_month": round(self.trend_slope_per_month, 4) if self.trend_slope_per_month is not None else None,
            "r_squared": round(self.r_squared, 4) if self.r_squared is not None else None,
        }


def compute_growth(series: list[tuple[str, float]]) -> GrowthMetrics:
    n = len(series)
    mom: list[tuple[str, Optional[float]]] = []
    deltas: list[float] = []
    for i, (m, v) in enumerate(series):
        if i == 0:
            mom.append((m, None))
            continue
        prev = series[i - 1][1]
        if prev <= 0:
            mom.append((m, None))
            continue
        pct = (v - prev) / prev * 100.0
        mom.append((m, pct))
        deltas.append(pct)
    mom_avg = sum(deltas) / len(deltas) if deltas else None

    cagr = None
    if n >= 2 and series[0][1] > 0 and series[-1][1] > 0:
        ratio = series[-1][1] / series[0][1]
        months = n - 1
        cagr = (ratio ** (1.0 / months) - 1) * 100.0 if months > 0 else None

    yoy = None
    if n >= 13 and series[-13][1] > 0:
        yoy = (series[-1][1] - series[-13][1]) / series[-13][1] * 100.0

    slope, r2 = _linear_fit([v for _, v in series])
    return GrowthMetrics(series, mom, mom_avg, cagr, yoy, slope, r2)


def _linear_fit(ys: list[float]) -> tuple[Optional[float], Optional[float]]:
    n = len(ys)
    if n < 2:
        return None, None
    xs = list(range(n))
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den_x = sum((x - mean_x) ** 2 for x in xs)
    den_y = sum((y - mean_y) ** 2 for y in ys)
    if den_x == 0:
        return None, None
    slope = num / den_x
    if den_y == 0:
        return slope, 1.0 if num == 0 else 0.0
    r = num / math.sqrt(den_x * den_y)
    return slope, r * r


# ============================================================================
# Output writers
# ============================================================================

CSV_HEADERS = ["month", "account_id", "account_name", "service",
               "vcpu_hours", "hours_in_month", "avg_vcpu"]


def write_csv(report: SizingReport, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(CSV_HEADERS)
        for r in sorted(report.rows, key=lambda x: (x.month, x.account_id, x.service)):
            w.writerow([
                r.month_iso, r.account_id, r.account_name, r.service,
                f"{r.vcpu_hours:.4f}", hours_in_month(r.month), f"{r.avg_vcpu:.4f}",
            ])


def write_json(report: SizingReport, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    monthly = _monthly_breakdown(report)
    growth = compute_growth([(m["month"], m["avg_vcpu"]) for m in monthly])

    # Deduplicate notes while preserving order — repetition of the same
    # "unknown VM size 'X'" across months produces a lot of noise otherwise.
    seen: set[str] = set()
    deduped_notes: list[str] = []
    for n in report.notes:
        if n not in seen:
            seen.add(n)
            deduped_notes.append(n)

    # Group services per subscription for a quick by-account roll-up.
    by_sub: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    name_by_sub: dict[str, str] = {}
    for r in report.rows:
        by_sub[r.account_id][r.service] += r.vcpu_hours
        if r.account_name and r.account_name != r.account_id:
            name_by_sub[r.account_id] = r.account_name
    total_hours = sum(hours_in_month(m) for m in report.window.months()) or 1
    accounts = [
        {
            "account_id": sid,
            "account_name": name_by_sub.get(sid, sid),
            "avg_vcpu": round(sum(svcs.values()) / total_hours, 4),
            "by_service": {svc: round(v / total_hours, 4) for svc, v in sorted(svcs.items())},
        }
        for sid, svcs in sorted(by_sub.items())
    ]

    unmapped = sorted(
        [
            {"meter_category": cat, "meter_subcategory": sub, "meter": meter}
            for (cat, sub, meter) in report.unmapped_meters
        ],
        key=lambda d: (d["meter_category"], d["meter_subcategory"], d["meter"]),
    )

    payload = {
        "cloud": report.cloud,
        "mode": report.mode,
        "coverage": report.coverage,
        "window": {"start": report.window.start_iso, "end": report.window.end_iso},
        "rows": [
            {
                "month": r.month_iso,
                "account_id": r.account_id,
                "account_name": r.account_name,
                "service": r.service,
                "vcpu_hours": round(r.vcpu_hours, 4),
                "hours_in_month": hours_in_month(r.month),
                "avg_vcpu": round(r.avg_vcpu, 4),
            }
            for r in sorted(report.rows, key=lambda x: (x.month, x.account_id, x.service))
        ],
        "monthly": monthly,
        "accounts": accounts,
        "headline_avg_vcpu_yearly": round(report.headline_yearly_avg_vcpu(), 4),
        "headline_peak_month_avg_vcpu": round(report.headline_peak_month_avg_vcpu(), 4),
        "growth": growth.to_dict(),
        "subs_queried_ok": sorted(report.subs_queried_ok),
        "subs_skipped": [{"subscription_id": sid, "error": err} for sid, err in report.subs_skipped],
        # Meters that came back from Cost Management under a category we said
        # we'd cover but didn't match any classification rule. If this list is
        # non-empty AND the headline number looks low, you're likely missing a
        # SKU/plan mapping in the script (e.g. a new App Service plan).
        "unmapped_meters": unmapped,
        "notes": deduped_notes,
    }
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=False)
        f.write("\n")


def _monthly_breakdown(report: SizingReport) -> list[dict]:
    by_month: dict[date, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for r in report.rows:
        by_month[r.month][r.service] += r.vcpu_hours
    result = []
    for m in sorted(by_month):
        services = by_month[m]
        hrs = hours_in_month(m)
        result.append({
            "month": f"{m.year:04d}-{m.month:02d}",
            "avg_vcpu": round(sum(services.values()) / hrs, 4) if hrs else 0.0,
            "by_service": {svc: round(v / hrs, 4) for svc, v in sorted(services.items())},
        })
    return result


def headline_growth_line(metrics: GrowthMetrics) -> Optional[str]:
    if metrics.cagr_monthly_pct is None:
        return None
    parts = [f"trend: {metrics.cagr_monthly_pct:+.1f}%/month CAGR"]
    if metrics.yoy_growth_pct is not None:
        parts.append(f"{metrics.yoy_growth_pct:+.1f}% YoY")
    if metrics.trend_slope_per_month is not None:
        parts.append(f"slope {metrics.trend_slope_per_month:+.2f} vCPU/month")
    return " · ".join(parts)


# ============================================================================
# CLI
# ============================================================================

def _build_scope(args: argparse.Namespace) -> Optional[str]:
    if args.scope:
        return args.scope
    if args.management_group:
        return f"/providers/Microsoft.Management/managementGroups/{args.management_group}"
    if args.billing_account:
        return f"/providers/Microsoft.Billing/billingAccounts/{args.billing_account}"
    return None


def _enumerate_subscriptions(credential, requested: Optional[list[str]]) -> dict[str, str]:
    """List subscriptions visible to the credential.

    If a service principal lacks tenant-wide visibility but has explicit
    --subscriptions, fall back to using the IDs as-is rather than failing.
    """
    sub_map: dict[str, str] = {}
    try:
        sub_client = SubscriptionClient(credential)
        for s in sub_client.subscriptions.list():
            if s.subscription_id and s.state == "Enabled":
                sub_map[s.subscription_id] = s.display_name or s.subscription_id
    except Exception as exc:
        log.warning("could not list subscriptions (%s); using requested IDs as-is", exc)
    if requested:
        sub_map = {sid: sub_map.get(sid, sid) for sid in requested}
    return sub_map


def _pick_sku_subscription(credential, sub_map: dict[str, str]) -> str:
    """Return a subscription id whose Microsoft.Compute/skus we can actually list.

    Falls back to the first id if no SKU lookup works (the size lookup will
    just yield unknown-VM-size notes; better than hard-failing).
    """
    last_exc: Optional[Exception] = None
    for sid in list(sub_map.keys())[:5]:
        try:
            c = ComputeManagementClient(credential, sid)
            it = c.resource_skus.list()
            for _ in it:
                # First page reachable -> good enough.
                log.info("using subscription %s for VM SKU lookup", sid)
                return sid
        except Exception as exc:
            last_exc = exc
            log.warning("subscription %s cannot list Compute SKUs (%s) — trying next", sid, exc)
    first = next(iter(sub_map.keys()))
    log.warning(
        "no subscription could list Microsoft.Compute/skus (last error: %s); "
        "VM sizes will be reported as unknown",
        last_exc,
    )
    return first


def _enumerate_mg_subscriptions(credential, mg_id: str) -> dict[str, str]:
    """Return {sub_id: name} for all enabled subscriptions under a management group.

    Uses the Management Groups API to walk the MG hierarchy. Falls back to the
    full tenant subscription list (already RBAC-filtered) if unavailable.
    """
    try:
        from azure.mgmt.managementgroups import ManagementGroupsAPI
        mg_client = ManagementGroupsAPI(credential)
        entities = mg_client.entities.list(group_name=mg_id)
        sub_map: dict[str, str] = {}
        for e in entities:
            if getattr(e, "type", "") == "/subscriptions":
                sid = (e.name or "").strip()
                name = getattr(e, "display_name", None) or sid
                if sid:
                    sub_map[sid] = name
        if sub_map:
            log.info("management group %s: found %d subscription(s) via MG entities API", mg_id, len(sub_map))
            return sub_map
        log.warning("MG entities API returned no subscriptions for %s; falling back", mg_id)
    except Exception as exc:
        log.warning("MG entities API unavailable (%s); falling back to full subscription list", exc)

    # Fallback: all subscriptions visible to the credential (RBAC already scopes them)
    sub_client = SubscriptionClient(credential)
    sub_map = {}
    for s in sub_client.subscriptions.list():
        if s.subscription_id and s.state == "Enabled":
            sub_map[s.subscription_id] = s.display_name or s.subscription_id
    log.info("management group fallback: using all %d visible subscription(s)", len(sub_map))
    return sub_map


def main() -> int:
    p = argparse.ArgumentParser(
        description="FortiCNAPP / Lacework Azure pre-PoV sizing (avg vCPU/month).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--mode", choices=("billing", "operational"), default="billing",
                   help="billing (default; needs Cost Management read) or operational fallback.")
    p.add_argument("--coverage", choices=("parity", "extended"), default="extended",
                   help="parity = VM/VMSS only; extended (default) adds ACI/Container Apps/AppService/SQL/PostgreSQL/MySQL/AKS-VirtualNodes.")
    scope_grp = p.add_argument_group("scope (pick one — most-recommended at top)")
    scope_grp.add_argument("--billing-account", help="MCA / EA billing account id — single query covers entire enrolment.")
    scope_grp.add_argument("--management-group", help="Management group id (use the tenant id for the Tenant Root MG).")
    scope_grp.add_argument("--scope", help="Raw Cost Management scope path.")
    scope_grp.add_argument("--subscriptions", nargs="+", help="Restrict to these subscription ids.")
    p.add_argument("--start", help="Start month YYYY-MM (default: end-11).")
    p.add_argument("--end", help="End month YYYY-MM (default: previous completed month).")
    p.add_argument("--output", type=Path, default=Path.cwd(),
                   help="Directory for the JSON + CSV (default: current directory).")
    p.add_argument("--throttle", type=float, default=0.5,
                   help="Seconds to sleep between per-subscription Cost Management queries (default: 0.5). "
                        "Raise (e.g. 1.5) on large tenants if you keep hitting 429s.")
    p.add_argument("-v", "--verbose", action="store_true", help="DEBUG logging.")
    args = p.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    try:
        window = MonthWindow.parse(args.start, args.end)
    except ValueError as e:
        sys.stderr.write(f"window error: {e}\n")
        return 2

    credential = DefaultAzureCredential()

    sub_map = _enumerate_subscriptions(credential, args.subscriptions)
    if not sub_map:
        sys.stderr.write(
            "No accessible Azure subscriptions found.\n"
            "Run `az login` (or set AZURE_* env vars for a service principal).\n"
            "If using a service principal, ensure it has at least Reader on one subscription.\n"
        )
        return 2
    # Try a few subscriptions for the SKU catalogue lookup — the first one may
    # not have Reader for Microsoft.Compute/skus on every credential.
    sku_subscription_id = _pick_sku_subscription(credential, sub_map)

    print(f"Window: {window.start_iso}..{window.end_iso}  ({len(window.months())} months)")
    print(f"Subscriptions visible: {len(sub_map)}  (SKU lookup uses {sku_subscription_id})")

    def _per_sub_billing(subs: dict[str, str], label: str) -> tuple["SizingReport", str]:
        """Query Cost Management per-subscription and merge results.

        Throttles between subscriptions to stay under Cost Management QPU
        limits when iterating large tenants (the API will return 429 well
        before 1 query/s sustained on big MGs).
        """
        r = SizingReport(cloud="azure", mode="billing", coverage=args.coverage, window=window)
        total = len(subs)
        for idx, (sid, name) in enumerate(subs.items(), start=1):
            print(f"  ▸ [{idx}/{total}] querying /subscriptions/{sid} ({name})")
            try:
                sr = collect_billing(
                    credential, f"/subscriptions/{sid}", sku_subscription_id, window, args.coverage,
                )
            except Exception as exc:
                err_first = str(exc).splitlines()[0]
                print(f"    ! skipped ({err_first})")
                r.subs_skipped.append((sid, err_first))
                continue
            r.subs_queried_ok.add(sid)
            for row in sr.rows:
                if not row.account_name or row.account_name == row.account_id:
                    row = UsageRow(row.month, row.account_id or sid, name, row.service, row.vcpu_hours)
                r.add(row)
            r.notes.extend(sr.notes)
            r.unmapped_meters |= sr.unmapped_meters
            if idx < total:
                time.sleep(args.throttle)
        if r.subs_skipped:
            preview = "; ".join(f"{sid}: {e}" for sid, e in r.subs_skipped[:5])
            tail = " ..." if len(r.subs_skipped) > 5 else ""
            r.notes.append(f"{len(r.subs_skipped)} subscription(s) skipped due to errors: {preview}{tail}")
        sl = label if label else ("tenant" if len(subs) > 1 else next(iter(subs.keys())))
        return r, sl

    if args.mode == "billing":
        scope = _build_scope(args)
        if scope:
            # Default path: single query at the chosen scope (MG / billing
            # account / explicit). MG scope is preferred because Cost
            # Management QPU consumption is much lower than 1-query-per-sub.
            # If MG / billing-account rejects the query (e.g. no consolidated
            # billing under that MG, or it 429s persistently), fall back to
            # per-subscription queries with throttle.
            print(f"Mode: billing  scope: {scope}")
            try:
                report = collect_billing(credential, scope, sku_subscription_id, window, args.coverage)
                scope_label = scope.split("/")[-1] or "scope"
            except Exception as exc:
                err = str(exc)
                should_fallback = args.management_group and (
                    "valid subscriptions" in err or "BadRequest" in err or "Too many requests" in err
                )
                if should_fallback:
                    mg_id = args.management_group
                    print(
                        f"  ! MG scope failed: {err.splitlines()[0]}\n"
                        f"  ↳ Falling back to per-subscription queries under MG {mg_id}"
                    )
                    mg_subs = _enumerate_mg_subscriptions(credential, mg_id)
                    if not mg_subs:
                        sys.stderr.write(f"No subscriptions found under management group {mg_id}\n")
                        return 2
                    print(f"  ↳ Found {len(mg_subs)} subscription(s) under {mg_id}")
                    report, scope_label = _per_sub_billing(mg_subs, mg_id)
                elif args.billing_account and ("BadRequest" in err or "Too many requests" in err):
                    print(
                        f"  ! billing-account scope failed: {err.splitlines()[0]}\n"
                        f"  ↳ Falling back to per-subscription queries"
                    )
                    report, scope_label = _per_sub_billing(sub_map, args.billing_account)
                else:
                    raise
        else:
            # No scope flag at all → per-subscription queries against every
            # visible subscription, merged.
            print(f"Mode: billing  scope: enumerated subscriptions ({len(sub_map)})")
            report, scope_label = _per_sub_billing(sub_map, "")
    else:
        print(f"Mode: operational  subscriptions: {len(sub_map)}")
        report = collect_operational(
            credential, list(sub_map.keys()), sub_map, window, args.coverage, sku_subscription_id,
        )
        scope_label = "tenant" if len(sub_map) > 1 else next(iter(sub_map.keys()))

    args.output.mkdir(parents=True, exist_ok=True)
    base = (
        f"azure_sizing_{scope_label}_{report.mode}_{report.coverage}_"
        f"{report.window.start_iso}_{report.window.end_iso}"
    )
    csv_path = args.output / f"{base}.csv"
    json_path = args.output / f"{base}.json"
    write_csv(report, csv_path)
    write_json(report, json_path)

    headline = report.headline_yearly_avg_vcpu()
    peak = report.headline_peak_month_avg_vcpu()

    # Roll up rows by service so the operator gets a quick read-out without
    # having to crack open the JSON.
    by_service: dict[str, float] = defaultdict(float)
    for r in report.rows:
        by_service[r.service] += r.vcpu_hours
    total_hours = sum(hours_in_month(m) for m in report.window.months()) or 1

    print()
    print("===== SUMMARY =====")
    print(f"Window:                          {report.window.start_iso}..{report.window.end_iso}  ({len(report.window.months())} months)")
    print(f"Mode / coverage:                 {report.mode} / {report.coverage}")
    print(f"Raw rows aggregated:             {len(report.rows)}")
    if report.subs_queried_ok or report.subs_skipped:
        total_attempted = len(report.subs_queried_ok) + len(report.subs_skipped)
        print(f"Subscriptions queried OK:        {len(report.subs_queried_ok)} / {total_attempted}")
        if report.subs_skipped:
            print(f"Subscriptions skipped:           {len(report.subs_skipped)}  (see JSON 'subs_skipped')")
    if by_service:
        print("By service (avg vCPU over window):")
        for svc, h in sorted(by_service.items(), key=lambda x: -x[1]):
            print(f"  {svc:20s} {h / total_hours:10.2f}")
    if report.unmapped_meters:
        print(f"Unmapped meters (in covered categories): {len(report.unmapped_meters)}  (see JSON 'unmapped_meters')")
    print()
    print(f"Headline avg vCPU (window):      {headline:.2f}")
    print(f"Headline peak month avg vCPU:    {peak:.2f}")
    growth = compute_growth(
        [(m["month"], m["avg_vcpu"]) for m in _monthly_breakdown(report)]
    )
    line = headline_growth_line(growth)
    if line:
        print(line)
    if report.notes:
        print(f"\n{len(report.notes)} note(s) attached in JSON.")
    print(f"\nWrote: {csv_path}\nWrote: {json_path}")

    # Loud warnings on suspicious outcomes — the operator should NOT have to
    # parse JSON to realise that a 200-sub run produced zero data.
    warnings: list[str] = []
    if headline == 0.0:
        if report.subs_queried_ok and not report.rows:
            warnings.append(
                f"Headline is 0 even though {len(report.subs_queried_ok)} subscription(s) returned successfully. "
                "Either the tenant truly had no covered workloads in the window, or the meter-name "
                "heuristic is missing coverage for what is actually billed. Inspect 'unmapped_meters' "
                "in the JSON."
            )
        if report.subs_skipped and not report.subs_queried_ok:
            warnings.append(
                f"All {len(report.subs_skipped)} subscription queries failed. First error: "
                f"{report.subs_skipped[0][1]}"
            )
    if report.unmapped_meters and (not report.rows or headline < 1.0):
        warnings.append(
            f"{len(report.unmapped_meters)} meter(s) in covered categories didn't classify. "
            "If the customer runs ACI / Container Apps / App Service / AKS-VirtualNodes / "
            "Functions Premium, check 'unmapped_meters' for missing SKU mappings."
        )
    for w in warnings:
        sys.stderr.write("\n!! WARNING: " + w + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())

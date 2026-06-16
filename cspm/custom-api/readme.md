# FortiCNAPP Framework Migration

This guide demonstrates how to export selected custom frameworks from a source FortiCNAPP tenant and import them into a target tenant using the Frameworks API.

## Prerequisites

* Source tenant API Key ID and Secret
* Target tenant API Key ID and Secret
* `curl`
* `jq`

---

## Variables

### Template

```bash
SOURCE_TENANT=<SOURCE_TENANT>
SOURCE_KEYID=<SOURCE_KEYID>
SOURCE_SECRET=<SOURCE_SECRET>

TARGET_TENANT=<TARGET_TENANT>
TARGET_KEYID=<TARGET_KEYID>
TARGET_SECRET=<TARGET_SECRET>
```

### Example

```bash
SOURCE_TENANT=654321
SOURCE_KEYID=lw-uak-xxxxxxxx
SOURCE_SECRET=xxxxxxxxxxxxxxxx

TARGET_TENANT=123456
TARGET_KEYID=lw-uak-yyyyyyyy
TARGET_SECRET=yyyyyyyyyyyyyyyy
```

---

# Export Frameworks from the Source Tenant

## Generate Source Tenant Token

```bash
STOK=$(curl -s -X POST "https://${SOURCE_TENANT}.lacework.net/api/v2/access/tokens" \
  -H "X-LW-UAKS: $SOURCE_SECRET" \
  -H "Content-Type: application/json" \
  -d "{\"keyId\":\"$SOURCE_KEYID\",\"expiryTime\":3600}" \
  | jq -r '.token')
```

## Export Selected Frameworks

```bash
curl -s "https://${SOURCE_TENANT}.lacework.net/api/v2/Frameworks" \
  -H "Authorization: Bearer $STOK" \
| jq '
[
  .data[]
  | select(.name | test("ISO/IEC 42001:2023 — AIMS|Microsoft Cloud Security Benchmark v3"))
  | select((.sections | length) > 0)
  | {
      name,
      domains,
      sections: [
        .sections[]
        | {
            name,
            policies: [
              .policies[]
              | { policyId }
            ]
          }
      ],
      tags
    }
]' > frameworks.json
```

## Verify Export

List exported framework names:

```bash
jq '.[].name' frameworks.json
```

Count exported frameworks:

```bash
jq length frameworks.json
```

---

# Import Frameworks into the Target Tenant

## Generate Target Tenant Token

```bash
TTOK=$(curl -s -X POST "https://${TARGET_TENANT}.lacework.net/api/v2/access/tokens" \
  -H "X-LW-UAKS: $TARGET_SECRET" \
  -H "Content-Type: application/json" \
  -d "{\"keyId\":\"$TARGET_KEYID\",\"expiryTime\":3600}" \
  | jq -r '.token')
```

## Import Frameworks

```bash
jq -c '.[]' frameworks.json | while read -r fw; do
  curl -s -X POST "https://${TARGET_TENANT}.lacework.net/api/v2/Frameworks" \
    -H "Authorization: Bearer $TTOK" \
    -H "Content-Type: application/json" \
    -d "$fw" \
  | jq '{name: .data.name, sections: (.data.sections | length)}'
done
```

## Verify Import

```bash
curl -s "https://${TARGET_TENANT}.lacework.net/api/v2/Frameworks" \
  -H "Authorization: Bearer $TTOK" \
| jq -r '.data[].name'
```

---

# Framework Selection Logic

Frameworks are selected based on the framework name:

```jq
select(.name | test("ISO/IEC 42001:2023 — AIMS|Microsoft Cloud Security Benchmark v3"))
```

This matches frameworks whose names contain:

* `ISO/IEC 42001:2023 — AIMS`
* `Microsoft Cloud Security Benchmark v3`

### Example new Custom Frameworks naming

```jq
select(
  .name == "ISO/IEC 42001:2023 — AIMS (AWS)"
  or
  .name == "ISO/IEC 42001:2023 — AIMS (GCP)"
  or
  .name == "Microsoft Cloud Security Benchmark v3 (AZURE)"
)
```

---

# Notes

Exclude empty frameworks:

```jq
select((.sections | length) > 0)
```

This prevents API validation failures because the Frameworks API rejects empty framework definitions.

The exported frameworks are stored in:

```text
frameworks.json
```

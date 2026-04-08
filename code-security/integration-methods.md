


flowchart TD
    A[Start] --> B[Install CLI]
    B --> C[Configure Authentication]
    C --> D{Git repo exists?}
    D -- No --> E[git init + add + commit]
    D -- Yes --> F[Proceed]
    E --> F
    F --> G[Run Scan]

    G --> H[Local Scan: lacework sca scan .]
    G --> I[Export File: -f sarif]
    G --> J[Upload UI: --save-results]

    H --> K[Terminal Results]
    I --> L[Report File]
    J --> M[FortiCNAPP UI]

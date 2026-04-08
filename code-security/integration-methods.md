


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




# Install
curl -sSL https://raw.githubusercontent.com/lacework/go-sdk/main/cli/install.sh | bash

# Configure
lacework configure -a <account> -k <key> -s <secret>

# Prepare repo
git init && git add . && git commit -m "init"

# Scan + upload
lacework sca scan . --save-results

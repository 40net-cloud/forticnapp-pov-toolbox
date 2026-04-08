


# Install
curl -sSL https://raw.githubusercontent.com/lacework/go-sdk/main/cli/install.sh | bash

# Configure
lacework configure -a <account> -k <key> -s <secret>

# Prepare repo
git init && git add . && git commit -m "init"

# Scan + upload
lacework sca scan . --save-results

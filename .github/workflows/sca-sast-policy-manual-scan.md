name: FortiCNAPP Manual Upload Test

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  test-upload:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v5

      - name: Install FortiCNAPP CLI
        run: |
          curl -sSL https://raw.githubusercontent.com/lacework/go-sdk/main/cli/install.sh | bash
          lacework configure \
            -a ${{ secrets.LW_ACCOUNT_NAME }}.lacework.net \
            -k ${{ secrets.LW_API_KEY }} \
            -s ${{ secrets.LW_API_SECRET }} \
            --noninteractive
          lacework component install sca

      - name: Run SCA (save + capture output)
        run: |
          mkdir -p lacework-reports
          lacework sca scan . \
            -f sarif \
            -o lacework-reports/scan.sarif.json \
            --save-results | tee scan-output.txt

      - name: Enforce policy (block pipeline)
        run: |
          if grep -E "Critical: [1-9]|High: [1-9]" scan-output.txt; then
            echo "❌ Blocking due to vulnerabilities"
            exit 1
          else
            echo "✅ No blocking vulnerabilities"
          fi

#!/bin/bash

# Script to test GitHub workflow locally using act
# Requires: https://github.com/nektos/act

echo "=== Local GitHub Actions Test for SPDX Sync ==="
echo

# Check if act is installed
if ! command -v act &> /dev/null; then
    echo "❌ 'act' is not installed."
    echo "Install it with:"
    echo "  - Mac: brew install act"
    echo "  - Linux: curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash"
    echo "  - Or download from: https://github.com/nektos/act/releases"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "Prerequisites check passed ✅"
echo

# Create a test event file for manual trigger
cat > /tmp/workflow_event.json << 'EOF'
{
  "action": "workflow_dispatch",
  "inputs": {}
}
EOF

echo "Testing workflow: sync-spdx-taxonomy.yml"
echo "----------------------------------------"

# Run the workflow with act
act workflow_dispatch \
    -W .github/workflows/sync-spdx-taxonomy.yml \
    -e /tmp/workflow_event.json \
    --container-architecture linux/amd64 \
    -v

RESULT=$?

# Cleanup
rm -f /tmp/workflow_event.json

if [ $RESULT -eq 0 ]; then
    echo
    echo "✅ Workflow test completed successfully!"
else
    echo
    echo "❌ Workflow test failed with exit code: $RESULT"
fi

exit $RESULT
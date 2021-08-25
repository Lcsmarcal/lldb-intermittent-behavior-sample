#!/bin/bash
cat <<EOF > ~/.lldb-remap
settings set target.source-map . $REPO_ROOT/
settings append target.source-map /APPLE_SDKROOT $SDKROOT/
settings append target.source-map /APPLE_PLATFORM_DIR $PLATFORM_DIR/
settings append target.source-map /APPLE_DEVELOPER_DIR $DEVELOPER_DIR/
EOF
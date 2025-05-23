#!/bin/sh

CONFIG_FILE=/app/public/config.js

cat <<EOF > $CONFIG_FILE
window.__CONFIG__ = {
  API_URL: "${API_URL}"
};
EOF

# Start the Next.js app
exec "$@" 
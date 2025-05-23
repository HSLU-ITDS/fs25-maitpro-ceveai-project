#!/bin/sh

# Replace placeholder in public/runtime-config.js with actual API_URL
echo "Injecting API_URL into runtime-config.js"
sed -i "s|__API_URL__|${API_URL}|g" /app/public/runtime-config.js

# Run the actual app
exec "$@"
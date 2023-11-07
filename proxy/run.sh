#!/bin/sh

#!/bin/sh

# Replace environment variables in the template and save to the configuration file
# sed -e "s/\${LISTEN_PORT}/${LISTEN_PORT}/" \
#     -e "s/\${APP_HOST}/${APP_HOST}/" \
#     -e "s/\${APP_PORT}/${APP_PORT}/" \
#     /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

# Start Nginx
# nginx -g 'daemon off;'

set -e

envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
nginx -g 'daemon off;'
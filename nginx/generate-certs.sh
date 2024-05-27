#!/bin/bash

if [ ! -d "/etc/letsencrypt/live/openbodylog.com" ]; then
  mkdir -p /var/www/certbot
  certbot certonly --nginx --email hii543424@gmail.com --agree-tos --no-eff-email --force-renewal -d openbodylog.com -d www.openbodylog.com
fi
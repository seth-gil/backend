#!/bin/bash

sudo systemctl restart app
sudo systemctl restart nginx
echo "Successfully restarted nginx and app"
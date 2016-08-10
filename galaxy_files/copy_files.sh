#!/bin/bash

LG_IP=$1

if [[ -z "$LG_IP" ]]; then
    echo "Galaxy ip needed"
    exit
fi
FRAME=$(ssh lg@$LG_IP "bash -s" < get_frame.sh)
scp tmp_files_galaxy/kml/slave.kml lg@$LG_IP:/var/www/html/kml
scp tmp_files_galaxy/sync_nlc_4.php lg@$LG_IP:/var/www/html
scp tmp_files_galaxy/myplaces.kml lg@$LG_IP:\$HOME
ssh lg@$LG_IP "scp \$HOME/myplaces.kml $FRAME:\$HOME/earth/kml/slave/"
ssh lg@$LG_IP "rm myplaces.kml"
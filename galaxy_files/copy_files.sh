#!/bin/bash

path="`dirname \"$0\"`"
cd $path

LG_IP=$1

if [[ -z "$LG_IP" ]]; then
    echo "Galaxy ip needed"
    exit
fi

FRAME=$(sshpass -p 'lqgalaxy' ssh lg@$LG_IP "bash -s" < get_frame.sh)
sshpass -p 'lqgalaxy' scp tmp_files_galaxy/kml/slave.kml lg@$LG_IP:/var/www/html/kml
sshpass -p 'lqgalaxy' scp tmp_files_galaxy/sync_nlc_4.php lg@$LG_IP:/var/www/html
sshpass -p 'lqgalaxy' scp tmp_files_galaxy/myplaces.kml lg@$LG_IP:\$HOME
sshpass -p 'lqgalaxy' ssh lg@$LG_IP "scp \$HOME/myplaces.kml $FRAME:\$HOME/earth/kml/slave/"
sshpass -p 'lqgalaxy' ssh lg@$LG_IP "rm myplaces.kml"
#!/bin/bash - 
#===============================================================================
#
#          FILE: monitorAP.sh 
# 
#         USAGE:  monitor status of wireless AP
# 
#   DESCRIPTION: 
# 
#       OPTIONS:  ---
#  REQUIREMENTS:  ---
#          BUGS:  ---
#         NOTES:  ---
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

#Check arguments
if [ $# -ne 1 ]; then
    echo 'Usage:'
    echo '    monitorAP.sh wlanDevice'
    echo 'Example:'
    echo '    monitorAP.sh wlan0'
    exit 1
fi

export wlanDev=$1
export logPath=./log/
export logFile=`date +%H_%M_%S`;

function showAllAP 
{ 
    iwlist $wlanDev scan |grep -iE 'cell|essid|signal' >> $logPath$logFile.log; 
    iwlist $wlanDev scan |grep -iE 'cell|essid|signal'; 
}
export -f showAllAP

watch -n 2 -d bash -c showAllAP


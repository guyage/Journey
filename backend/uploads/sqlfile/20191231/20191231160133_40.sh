#!/bin/bash

slowlogpath="/xs/logs/mysql"
slowdate=`date +%Y%m%d%H`
lastslowdate=`date -d "1 hour ago" +"%Y%m%d%H"`

#mysql connect info
dbhost="127.0.0.1"
dbport="3306"
dbuser="slowlogadmin"
dbpasswd="xsslowlogadmin"

#target path
targethost="10.30.0.37"
targetsshport="8000"
targetpath="/mddata2/backup/mysql/slowlog/xiangshang/"

mysqlbin="/xs/app/mysql/bin"

slowlogfile="$slowlogpath/$dbport/slow$slowdate.log"
echo "-------------------------------------------"$slowlogfile"-------------------------------------------"
echo $slowlogfile
lastslowlogfile="$slowlogpath/$dbport/slow$lastslowdate.log"
echo $lastslowlogfile


changeslowlog="set global slow_query_log_file=\"$slowlogfile\";"
echo $changeslowlog

$mysqlbin/mysql -u$dbuser -h$dbhost -p$dbpasswd -P$dbport -e "$changeslowlog"


date
if [ -f $lastslowlogfile ];then
  rsync -av -e "ssh -p $targetsshport" --bwlimit=20000 $lastslowlogfile root@$targethost:$targetpath
else
  echo $lastslowlogfile "is not exists!"
fi
date
echo -e "\n"

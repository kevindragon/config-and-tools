#!/bin/bash

#
# 通过查看 $target 目录是否可以访问，来检测NFS是否可以连通
# 如果未能连接，则先卸载，然后再挂载
# 如果上一个检测程序还未停止，此次检测退出不再做检测
# 日志文件写在/var/log/nfscheck.log文件里面
#

log_file="/var/log/nfscheck.log"
prog="nfscheck.sh"
source="10.123.4.22:/home/www/word"
target=/root/word

if [ `ps -C $prog --no-header | wc -l` -ne 0 ];then
    echo "$prog is running. exit" >> $log_file
    exit
fi 

s=`ls $target 2>&1 | grep "Stale NFS file handle" | wc -l`

if [[ $s -eq 1 ]];then
    echo "`date`" >> $log_file
    echo "Stale NFS file handle" >> $log_file
    echo -n "umount $target" >> $log_file
    umount -f $target
    if [ $? -eq 0 ];then
        echo "umount success" >> $log_file
        echo "re-mount $target" >> $log_file
        mount -t nfs $source $target
        if [ $? -ne 0 ];then
            echo "re-mount failed." >> $log_file
        else
            echo "re-mount success" >> $log_file
        fi
    else
        echo "umount failed." >> $log_file
        echo "nfs can not connect on $HOSTNAME" | mail -s "stale nfs" kevin.jiang@lexisnexis.com
        echo "nfs can not connect on $HOSTNAME" | mail -s "stale nfs" 13918543465@139.com
    fi
fi

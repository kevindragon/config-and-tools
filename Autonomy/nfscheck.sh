#!/bin/bash

#
# 通过查看 $target 目录是否可以访问，来检测NFS是否可以连通
# 如果未能连接，则先卸载，然后再挂载
# 如果上一个检测程序还未停止，此次检测退出不再做检测
# 日志文件写在/var/log/nfscheck.log文件里面
#

log_file="/var/log/nfscheck.log"
prog="nfscheck.sh"
src1="10.123.4.22:/home/www/word"
src2="10.123.4.22:/home/www/newsletters"
src3="10.123.4.22:/home/www/ipatt"
target1="/root/word"
target2="/root/newsletters"
target3="/root/ipatt"

FAILED_EXIT=2
failed_count=0

while :
do
    s=`ls $target1 2>&1 | grep "Stale NFS file handle" | wc -l`
    if [[ $s -eq 1 ]];then
        echo "`date`" >> $log_file
        echo "Stale NFS file handle" >> $log_file
        echo "umount $target1 $target2 $target3" >> $log_file
        umount -f $target1 $target2 $target3
        if [ $? -eq 0 ];then
            echo "umount success" >> $log_file
            echo "re-mount $target1 $target2 $target3" >> $log_file
            mount -t nfs $src1 $target1
            mount -t nfs $src2 $target2
            mount -t nfs $src3 $target3
            if [ $? -ne 0 ];then
                echo "re-mount failed." >> $log_file
                failed_count=$((failed_count+1))
            else
                failed_count=0
                echo "re-mount success" >> $log_file
            fi
        else
            echo "umount failed." >> $log_file
            echo "nfs can not connect on $HOSTNAME" | mail -s "stale nfs" kevin.jiang@lexisnexis.com
            echo "nfs can not connect on $HOSTNAME" | mail -s "stale nfs" 13918543465@139.com
        fi
    fi
    
    if [ $failed_count -gt $FAILED_EXIT ];then
        echo "nfs can not connect on $HOSTNAME. tried $FAILED_EXIT times" | mail -s "stale nfs" kevin.jiang@lexisnexis.com
        echo "nfs can not connect on $HOSTNAME. tried $FAILED_EXIT times" | mail -s "stale nfs" 13918543465@139.com
    fi

    sleep 600
done


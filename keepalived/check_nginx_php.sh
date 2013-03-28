#!/bin/bash

keepalived_log="/usr/local/keepalived/keepalived.log"

# monitor nginx process, if con't get nginx or restart process
# then kill keepalived let backup machine take the virtual ip
if [ `ps -C nginx --no-header | wc -l` -eq 0 ];then
    echo -e `date`"\nnginx was down, restart..." >> $keepalived_log
    if [ -f /usr/local/nginx/sbin/nginx ];then
        /usr/local/nginx/sbin/nginx
        sleep 3
    else
        echo -e "/usr/local/nginx/sbin/nginx not found.\nkill keepalived." >> $keepalived_log
        killall keepalived
        exit 1
    fi  
    if [ `ps -C nginx --no-header | wc -l` -eq 0 ];then
        echo -e "restart nginx failed.\nkill keepalived." >> $keepalived_log
        killall keepalived
        exit 1
    fi  
fi

# monitor php-fpm process, if con't get php-fpm or restart process
# then kill keepalived let backup machine take the virtual ip
if [ `ps -C php-fpm --no-header | wc -l` -eq 0 ];then
    echo -e `date`"\nphp-fpm was down, restart..." >> $keepalived_log
    if [ -f /usr/local/php/sbin/php-fpm ];then
        /usr/local/php/sbin/php-fpm
        sleep 3
    else
        echo -e "/usr/local/php/sbin/php-fpm not found.\nkill keepalived." >> $keepalived_log
        killall keepalived
        exit 1
    fi  
    if [ `ps -C php-fpm --no-header | wc -l` -eq 0 ];then
        echo -e "restart php-fpm failed.\nkill keepalived." >> $keepalived_log
        killall keepalived
        exit 1
    fi
fi

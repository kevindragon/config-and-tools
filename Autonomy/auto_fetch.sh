#!/bin/bash

template_file=tax.cfg.template
if [ ! -e $template_file ]; then
    echo "$template_file not exists. exit"
    exit
fi
template_str="{_ID_LIST_}"
files=`ls $1`

for f in $files
do
    proc_status=`ps aux | grep odbcfetch_inc | grep -v grep | wc -l`
    while [ $proc_status -eq 1 ]; do
        sleep 10
        proc_status=`ps aux | grep odbcfetch_inc | grep -v grep | wc -l`
    done
    if [ $proc_status == 0 ]; then
        echo "start handle $f"
        # read ids
        if [ "`wc -l $f | awk '{print $1}'`" -gt 1 ]; then
            ids=`tr "[\r\n]" "," < $f | sed 's/,,/,/g'`
        else
            ids=`cat $f`
        fi

        if [ "$ids" ]; then
            echo "read $f done"
            # change config file
            sed "s/$template_str/$ids/g" $template_file > tax.cfg
            # start fetch
            if [ $? == 0 ]; then
                ./clean.sh
                ./StartODBCFetch.sh 
            else
                echo "change config file failed. exit"
                exit
            fi
        else
            echo "read ids failed. exit"
            exit
        fi
        sleep 5
        proc_status=`ps aux | grep odbcfetch_inc | grep -v grep | wc -l`
        if [ $proc_status -ne 1 ]; then
            echo "proc running failed. exit"
            exit
        fi
    else
        echo "handle $f done"
    fi

    sleep 120
done

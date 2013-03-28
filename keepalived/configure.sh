#!/bin/bash

popt_count=`rpm -qa | grep popt | wc -l`
if [ $popt_count -eq 0 ]; then
    echo -e "missing dependent package popt"
fi

./configure --prefix=/usr/local/keepalved-1.2.7

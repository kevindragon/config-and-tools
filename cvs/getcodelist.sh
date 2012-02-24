#!/bin/bash

# --------------------------------------------------
# 批量获取cvs模块里的文件
# Author: Kevin
# Email : kittymiky@gmail.com
# 
# command line format:
#   ./getcodelist.sh 
#
# notice:
#   首先需要更改module_name变量,改成自己的模块
#   然后要登录到cvs, cvs -d $CVSROOT login
#   然后运行此脚本即可
# --------------------------------------------------

module_name="alpha"

rm -rf $module_name/

cvs co -r "1.22" "$module_name/law/search_form_case_plus.php"

find $module_name/ -name 'CVS' -type d | while read f; do rm -rf $f; done

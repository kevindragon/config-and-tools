#!/bin/sh

# --------------------------------------------------
# cvs 文件的code review
# Author: Kevin
# Email : kittymiky@gmail.com
# 
# command line format:
#   ./codereview /filename branch_reversion
#
# notice:
#   首先需要更改临时目录tmpdir变量
#   然后要登录到cvs, cvs -d $CVSROOT login
# --------------------------------------------------

if (( $# < 2 )); then
  echo "Usage: $0 filename branch_reversion"
  exit 1
fi

tmpdir=/home/www/kevin/codereview

cd $tmpdir
rm -rf head-*
rm -rf branch-*
rm -rf cvs.log

if [ ${1:0:1} == "/" ]; then
  filename="alpha"$1
else
  filename="alpha/"$1
fi

suffix=${1##*/}
branch_file=branch-$suffix
head_file=head-$suffix

# get branch file
cvs co -p -r $2 $filename > $branch_file 2>>cvs.log

# get head branch file
head_rev=`echo $2|awk -F "." '{print $1"."$2}'`
cvs co -p -r $head_rev $filename > $head_file 2>>cvs.log

vimdiff -o +1 $branch_file $head_file

echo 'done'


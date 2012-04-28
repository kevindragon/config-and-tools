#!/bin/sh

for filename in $@
do
  echo "format" $filename
  xmllint --format $filename > tmp.xml
  mv tmp.xml $filename
done
exit


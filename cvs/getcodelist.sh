#!/bin/bash

rm -rf alpha/

cvs co -r "1.22" "alpha/law/search_form_case_plus.php"
cvs co -r "1.6" "alpha/law/search_form_case_plus_en.php"
cvs co -r "1.11" "alpha/law/search_form_expert.php"
cvs co -r "1.11" "alpha/law/search_form_foreignlaw.php"
cvs co -r "1.12" "alpha/law/template/search_form_expert.html"
cvs co -r "1.12" "alpha/law/template/search_form_newlaw.html"
cvs co -r "1.7" "alpha/law/template/search_form_newsletter.html"
cvs co -r "1.19" "alpha/law/template/search_form_book.html"

find alpha/ -name 'CVS' -type d | while read f; do rm -rf $f; done

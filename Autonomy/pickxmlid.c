/*
 * Autonomy/pickid.c
 *
 * 从一个已经格式化的xml文件里面提取<ID>123</ID>里面的数字
 *
 * Started by Kevin Jiang, Copyright (C) 2002
 *
 *   Kevin.Jiang<kittymiky@gmail.com>
 */

#include <stdio.h>
#include <sys/types.h>
#include <regex.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
  if (2 > argc) {
    printf("\nplese specify a filename\n");
    printf("Usage:\npickupid.py filename\n");
    return 1;
  }

  int          z;            //status
  int          cflags = REG_EXTENDED;   //compile flags
  regex_t      reg;          //compiled regular expression
  char         ebuf[128];    //error buffer
  regmatch_t   pm[10];       //pattern matches 0-9
  const size_t nmatch = 10;  //The size of array pm[]

  // 编译正则表达式
  z = regcomp(&reg, "<ID>([0-9]+)</ID>", cflags);
  if (0 != z) {
    regerror(z, &reg, ebuf, sizeof(ebuf));
    return 1;
  }
  
  char *filename = argv[1];


  FILE *fp = NULL;
  char buf[1024] = {0};

  fp = fopen(filename, "r");
  while (!feof(fp)) {
    fgets(buf, 1024, fp);

    z = regexec(&reg, buf, nmatch, pm, 0);

    if(z != REG_NOMATCH) {
      int i =0;
      for (; i<reg.re_nsub; i++) {
        char des[128];
        strncpy(des, buf+pm[i].rm_so+4, (pm[i].rm_eo-pm[i].rm_so-9));
        //printf("%d, %d = ", pm[i].rm_so, pm[i].rm_eo);
        printf("%s\n", des);
      }
    }
  }

  regfree(&reg);

  fclose(fp);

  return 0;
}

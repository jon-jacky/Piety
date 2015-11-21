/* echoer.c - test reading from stdin in rump kernel */

#include <stdio.h>

int main()
{
  char string[80];
  char *result = "Anything but NULL";
  while (result != NULL) {
    printf (">> ");
    result = fgets(string,80,stdin); /* returns null pointer if EOF */
    if (result != NULL) printf ("%s", string);  
  }
  printf("EOF\n");
  return 0;
}

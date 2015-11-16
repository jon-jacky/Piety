/* echo_c.c - an echo program in C, test reading from stdin in rump kernel */

#include <stdio.h>

int main()
{
  char command [80];
  while (command[0] != 'q') {
    printf (">> ");
    gets (command);
    printf ("%s\n", command);
  }
  return 0;
}

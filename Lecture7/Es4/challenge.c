#include <stdio.h>
#include <stdlib.h>

int main() {
    char destination[64];

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    puts("Welcome to my Teleporter! Where would you like to go?");
    printf("And don't worry, your destination is safely stored at %p\n", destination);
    gets(destination);

    puts("\nSafe journey!!\n");
    return 0;
}
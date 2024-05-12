#include <stdio.h>
#include <stdlib.h>

void win() {
    FILE *f = fopen("flag.txt", "r");
    char flag[64];
    fgets(flag, sizeof(flag), f);
    printf("How did you get here?\nAnyways, here is your flag: %s", flag);
    exit(0);
}

int main() {
    char destination[30];

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    puts("Welcome to my Teleporter! Where would you like to go?");
    gets(destination);

    puts("\nSafe journey!!\n");
    return 0;
} 
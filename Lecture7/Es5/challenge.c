#include <stdio.h>
#include <stdlib.h>

void win() {
    char flag[64];
    FILE *f = fopen("flag.txt", "r");
    if (f == NULL) {
        puts("Flag file is missing. Please contact an admin if you are running this on the shell server.");
        exit(0);
    }
    fgets(flag, sizeof(flag), f);
    printf("Congratulations! Here is the flag: %s", flag);
    fclose(f);
}

int main() {
    char destination[64];

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    int i = 0;
    while (i++ < 2) {
        puts("Welcome to my Teleporter! Where would you like to go?");
        read(0, destination, 128);
        printf("Teleporting to %s...\n", destination);
        if (i == 1) {
            puts("Didn't work? Try again!");
        }
    }

    puts("You've teleported too much! You're not allowed to teleport anymore!");

    return 0;
}
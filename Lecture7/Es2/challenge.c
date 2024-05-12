#include <stdio.h>
#include <stdlib.h>

int main() {
    int check = 0;
    char destination[30];

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    puts("Welcome to the Time Machine! When would you like to go?");
    gets(destination);

    puts("\nSafe journey!!\n");

    if (check == 0xdeadbeef) {
        puts("You've arrived at the wrong time! Use the flag to go back.");
        system("cat flag.txt");
    }
}
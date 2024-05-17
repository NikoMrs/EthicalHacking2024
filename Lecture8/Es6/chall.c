#include <stdio.h>
#include <stdlib.h>

int main() {
    char input[64];

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    printf("In my libc, printf() is at %p, can you guess where system() is? ", printf);
    gets(input);

    unsigned long int guess = atol(input);

    if(guess == (unsigned long int)system) {
        puts("Good job! You win!");
        puts("What now?");
    } else {
        puts("Nope, try again!");
        exit(0);
    }

    asm("mov $0, %rbx"); // Don't ask me why...
    return 0;
}
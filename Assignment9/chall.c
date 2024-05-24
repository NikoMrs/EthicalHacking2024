#include <stdio.h>
#include <stdlib.h>

int main() {
    char input[64];

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    gets(input);
    return 0;
}
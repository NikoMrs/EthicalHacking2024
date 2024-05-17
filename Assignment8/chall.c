#include <stdio.h>
#include <stdlib.h>

int main() {
    char input[64];

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    while(1) {
        printf("> ");
        fgets(input, sizeof(input), stdin);
        printf(input);
    }

    return 0;
}
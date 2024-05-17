#include <stdio.h>
#include <stdlib.h>
#include <string.h>

long random_long() {
    long ret;
	
    FILE *fp;
	fp = fopen("/dev/urandom", "r");

    if (fp == NULL) {
        printf("Error!");
        exit(1);
    }

    fread(&ret, sizeof(ret), 1, fp);
	return ret;
}

void win() {
    FILE *f = fopen("flag.txt", "r");
    char flag[64];
    fgets(flag, sizeof(flag), f);
    printf("Hello, admin\nHere is your flag: %s", flag);
    exit(0);
}

int main() {
    char name[1024];
    long password = random_long();
    long input;

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    printf("Welcome to the True Random Password Generator!\n\n");
    printf("username: ");
    fgets(name, sizeof(name), stdin);

    if (name[strlen(name) - 1] == '\n') {
        name[strlen(name) - 1] = '\0';
    }

    printf("Hello, ");
    printf(name);
    printf("\nPassword: ");
    scanf("%ld", &input);

    if (input == password) {
        win();
    } else {
        puts("Invalid password! Bye.\n");
    }

    return 0;
} 
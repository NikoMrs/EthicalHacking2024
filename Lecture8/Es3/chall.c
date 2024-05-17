#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PASS_LEN 16

char * random_password(int len) {
    char *password = malloc(len + 1);
	
    FILE *fp;
	fp = fopen("/dev/urandom", "r");

    if (fp == NULL) {
        printf("Error!");
        exit(1);
    }

    for (int i = 0; i < len; i++) {
        unsigned char c;
        fread(&c, 1, 1, fp);
        password[i] = (c % ('Z' - 'A')) + 'A';
    }

    password[len] = '\0';

	fclose(fp);
	return password;
}

void win() {
    FILE *f = fopen("flag.txt", "r");
    char flag[64];
    fgets(flag, sizeof(flag), f);
    printf("Hello, admin\nHere is your flag: %s", flag);
    exit(0);
}

int main() {
    char name[10];
    char *password = random_password(PASS_LEN);
    char input[PASS_LEN + 1];

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    printf("Welcome to the Very True Real Random Password Generator!\n\n");
    printf("username: ");
    fgets(name, sizeof(name), stdin);

    if (name[strlen(name) - 1] == '\n') {
        name[strlen(name) - 1] = '\0';
    }

    printf("Hello, ");
    printf(name);
    printf("\nPassword: ");
    fgets(input, sizeof(input), stdin);

    if (input[strlen(input) - 1] == '\n') {
        input[strlen(input) - 1] = '\0';
    }

    if (strcmp(input, password) == 0) {
        win();
    } else {
        puts("Invalid password! Bye.\n");
    }

    return 0;
} 
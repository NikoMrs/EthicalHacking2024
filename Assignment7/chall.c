#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>

pid_t father;

void win() {
    char flag[64];

    pid_t p = getpid();
    if (p != father) {
        puts("You are not allowed to win!");
        return;
    }

    FILE *f = fopen("flag.txt", "r");
    if (f == NULL) {
        puts("Flag file is missing. Please contact an admin if you are running this on the shell server.");
        exit(0);
    }
    fgets(flag, sizeof(flag), f);
    printf("Congratulations! Here is the flag: %s", flag);
    fclose(f);
}

void echo() {
    char input[64];

    puts("Data to be echoed: ");
    read(0, input, 73);
    printf("You said: %.79s\n", input);
}

void toUpper() {
    char input[64];
    int i;

    puts("Data to be uppercased: ");
    gets(input);
    for (i = 0; i < 64; i++) {
        if (input[i] >= 'a' && input[i] <= 'z') {
            input[i] -= 32;
        }
    }
    printf("Uppercased: %s\n", input);
}

int main() {
    char input[64];

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    father = getpid();

    while (1) {
        printf("Available commands:\n1. Echo\n2. Uppercase\n3. Exit\n");
        gets(input);
        int choice = atoi(input);
        if(choice == 3) {
            break;
        } else if(choice == 1) {
            pid_t p = fork();
            if (p == 0) {
                echo();
                exit(0);
            } else {
                wait(NULL);
            }
        } else if(choice == 2) {
            pid_t p = fork();
            if (p == 0) {
                toUpper();
                exit(0);
            } else {
                wait(NULL);
            }
        } else {
            puts("Invalid choice!");
        }
    }

    return 0;
}
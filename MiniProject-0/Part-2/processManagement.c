#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <fcntl.h>
#include <string.h>
int main(){
    int parent = getpid();
    int x = 25;
    pid_t pid;
    pid = fork();
    if(pid < 0){
        printf("Fork failed\n");
        exit(1);
    }
    else if(pid == 0){
        printf("Child Process: x = %d\n", x);
        x = x + 10;
        printf("Child Process changed x: x = %d\n", x);
    }
    else{
        printf("Parent Process: x = %d\n", x);
        x = x - 5;
        printf("Parent Process changed x: x = %d\n", x);
    }
    pid_t pid_2;
    pid_2 = fork();
    if(pid_2 < 0){
        printf("Fork failed\n");
        exit(1);
    }
    else if(pid_2 == 0){
        char string[10];
        sprintf(string, "%d", getppid());
        int fd = open("newfile.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
        if (fd < 0) {
            printf("Failed to open file\n");
            exit(1);
        }
        write(fd, string, strlen(string));
        close(fd);
    }
    pid_t pid_3;
    pid_3 = fork();
    if (pid_3 < 0){
        printf("Fork failed\n");
        exit(1);
    }
    else if(pid_3 > 0){
        printf("Killing parent process\n");
    }
    else{
        sleep(1);
        printf("Executing pid_3\n");
        printf("Parent pid: %d\n", getppid());
        exit(0);
    }
    return 0;
}
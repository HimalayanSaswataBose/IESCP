#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <stdlib.h>

int main() {
    int file_descriptor = open("newfile.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644); // Open file with specific permissions
    int standard_output = dup(1); // Save stdout to restore later
    int standard_input = dup(0); // Save stdin to restore later
    int c = 0;
    while (1){
        char input_msg[100];
        printf("Enter message: ");
        scanf("%s", input_msg);
        if (strcmp(input_msg, "STOP") == 0){
            break;
        }
        else if(strcmp(input_msg, "INPUT") == 0){
            printf("\tEnter input: ");
            char temp;
            scanf("%c", &temp);
            char input[100];
            scanf("%[^\n]s", input);
            dup2(file_descriptor, 1); // Redirect stdout to file for using printf
            printf("%s*", input);
            fflush(stdout);
            dup2(standard_output, 1); // Restore stdout
        }
        else if(strcmp(input_msg, "OUTPUT") == 0){
            // Print the first line
            char* line = (char*)malloc(sizeof(char)*100);
            dup2(file_descriptor, 0); // Redirect stdin to file for using scanf
            scanf("%[^\n]%*c", line);
            for (int i = 0; line[i] != '\0'; i++){
                if (line[i] == '*'){
                    line[i] = '\n';
                    break;
                }
            }
            printf("%s\n", line);
            free(line);
            dup2(standard_input, 0); // Restore stdin
        }
    }
    return 0;
}
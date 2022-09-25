// C program to illustrate the regexec() function
#include <regex.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdio.h>
 
void toUpperCase(char *wordBuffer)
{
    int j = 0;
 
    while (wordBuffer[j]) {
        wordBuffer[j] = toupper(wordBuffer[j]);
        j++;
    }
	printf("%s ", wordBuffer);
}

void tratarCaracter(char *wordBuffer){
	regex_t reegex;
	int value, pattern;

	pattern = regcomp(&reegex, "if|else|void|int|return", 0); 
	value = regexec( &reegex, wordBuffer, 0, NULL, 0);	
	if(value == 0){
		toUpperCase(wordBuffer);
	}
}

// Driver Code
int main()
{
	FILE *sourceFile;
    FILE *targetFile;
	regex_t reegex;

    char ch;
    sourceFile = fopen("gcd.txt", "r");
    targetFile = fopen("saida.txt", "w");
	char *wordBuffer = (char*)malloc(sizeof(char));
	int wordBufferLen = 0;
	int result = 1;

    while((ch = fgetc(sourceFile)) != EOF){
		if (ch == ')' || ch == '(' || ch == ',' || ch == ';' || isspace(ch) || ch == ' '){
			if(wordBufferLen > 0){
				wordBuffer[wordBufferLen] = '\0';
				
				result = regexec( &reegex, wordBuffer, 0, NULL, 0);	
				printf("%i", result);
				if(result == 0){
					printf("%s\n", wordBuffer);
					toUpperCase(wordBuffer);
				}
// tratarCaracter(wordBuffer);	
			 	// 

			}	
			 
			
		
			fputs(wordBuffer, targetFile);
			fputc(ch, targetFile);
			wordBuffer = NULL;
			wordBufferLen = 0;
		} else {
			wordBufferLen++;
			wordBuffer = (char*)realloc(wordBuffer, (wordBufferLen) * (sizeof(char)));
			wordBuffer[wordBufferLen-1] = ch;
		}
	}
        // fputc(ch, targetFile);
    
    fclose(sourceFile);
    fclose(targetFile);



	return 0;
}

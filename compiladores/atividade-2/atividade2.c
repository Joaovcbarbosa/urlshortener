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
}

void tratarCaracter(char *wordBuffer){	
	int value, pattern;
	regex_t reegex;

	pattern = regcomp(&reegex, "if|else|void|int|return", REG_EXTENDED|REG_NOSUB);
	value = regexec( &reegex, wordBuffer, 0, NULL, 0);	
	
	if(value == 0)
		toUpperCase(wordBuffer);	
}

int main()
{
	FILE *sourceFile;
    FILE *targetFile;
	

    char ch;
    sourceFile = fopen("gcd.txt", "r");
    targetFile = fopen("saida.txt", "w");
	char *wordBuffer = (char*)malloc(sizeof(char));
	int wordBufferLen = 0;
	
    while((ch = fgetc(sourceFile)) != EOF){
		if (ch == ')' || ch == '(' || ch == ',' || ch == ';' || isspace(ch) || ch == ' ' || ch == '\n' || ch == '\t'){
			if(wordBufferLen > 0){
				
				tratarCaracter(wordBuffer);	
				wordBuffer[wordBufferLen] = '\0';
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

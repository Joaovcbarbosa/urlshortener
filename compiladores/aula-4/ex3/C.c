#include <regex.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int comment = 0;

void toUpperCase(char *wordBuffer)
{
    int j = 0;
 
    while (wordBuffer[j]) {
        wordBuffer[j] = toupper(wordBuffer[j]);
        j++;
    }
}

int isBeginOfComment(char *wordBuffer){	
	return strcmp(wordBuffer, "/*");
}

int isEndOfComment(char *wordBuffer){
	return strcmp(wordBuffer, "*/");
}

int isReservedWord(char *wordBuffer){	
	int value, pattern;
	regex_t reegex;

	pattern = regcomp(&reegex, "if|else|void|int|return", REG_EXTENDED|REG_NOSUB);
	return regexec( &reegex, wordBuffer, 0, NULL, 0);	
}

int isEndOfSentence(char ch){
	if (ch == ')' || ch == '(' || ch == ',' || ch == ';' || isspace(ch) || ch == ' ' || ch == '\n' || ch == '\t')
		return 1;
	
	return 0;
}

void treatCharacter(char *wordBuffer, int wordBufferLen){		
	if (isBeginOfComment(wordBuffer) == 0){
		comment = 1;
		return;
	}

	if (isEndOfComment(wordBuffer) == 0){
		comment = 0;
		strcpy(wordBuffer, "");
		return;
	}

	if (isReservedWord(wordBuffer) == 0){		
		toUpperCase(wordBuffer);
	}			
}

int main()
{
	FILE *sourceFile = fopen("gcd.txt", "r");
    FILE *targetFile = fopen("saida.txt", "w");
    char ch;
	char *wordBuffer = '\0';
	int wordBufferLen = 0;
	int ascii;
	
    while((ch = fgetc(sourceFile)) != EOF){
		if (isEndOfSentence(ch) == 1){
			if(wordBufferLen > 0){				
				treatCharacter(wordBuffer, wordBufferLen);					
			}
			
			if(comment == 0){
				fputs(wordBuffer, targetFile);
				fputc(ch, targetFile);
			}
			wordBuffer = NULL;
			wordBufferLen = 0;
		} else {
			wordBufferLen++;
			wordBuffer = (char*)realloc(wordBuffer, (wordBufferLen) * (sizeof(char)));
			wordBuffer[wordBufferLen-1] = ch;
			wordBuffer[wordBufferLen] = '\0';
		}
	}
    
    fclose(sourceFile);
    fclose(targetFile);
	return 0;
}

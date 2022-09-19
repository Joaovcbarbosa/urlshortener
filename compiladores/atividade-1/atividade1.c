#include <stdio.h>
#include <stdlib.h>

int main()
{
    FILE *sourceFile;
    FILE *targetFile;
    char ch;

    sourceFile = fopen("gcd.txt", "r");
    targetFile = fopen("saida.txt", "w");

    while((ch = fgetc(sourceFile)) != EOF)
        fputc(ch, targetFile);
    
    fclose(sourceFile);
    fclose(targetFile);
}

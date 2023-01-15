#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int ehComentario = 0;;
char *palavra = '\0';
int palavraLen = 0;
char ch;

int ehComecoComentario(char *palavra){	
	return strcmp(palavra, "/*");
}

int ehFimComentario(char *palavra){
	return strcmp(palavra, "*/");
}

int ehFimPalavra(char ch){
	if (ch == ')' || ch == ',' || isspace(ch) || ch == ' ' || ch == '\n' || ch == '\t')
		return 1;
	
	return 0;
}

void VerificaComentario(char *palavra, int palavraLen){		
	if (ehComecoComentario(palavra) == 0){
		ehComentario = 1;
		return;
	}

	if (ehFimComentario(palavra) == 0){
		ehComentario = 0;
		strcpy(palavra, "");
		return;
	}
}

void RealocaPalavra(){
	palavraLen++;
	palavra = (char*)realloc(palavra, (palavraLen) * (sizeof(char)));
	palavra[palavraLen-1] = ch;
	palavra[palavraLen] = '\0';		
}

void PreProcessamento(char *nomeArquivoEntrada){ 
	FILE *arquivoEntrada = fopen(nomeArquivoEntrada, "r");
    FILE *arquivoPreProcessado = fopen("arquivoPreProcessado.txt", "w");
    while((ch = fgetc(arquivoEntrada)) != EOF){
		
		if(ch != 13){
			if (ehFimPalavra(ch) == 1){
				if(palavraLen > 0){				
					VerificaComentario(palavra, palavraLen);					
				}
				if(palavraLen == 0){				
					RealocaPalavra();		
				}	

				if(ehComentario == 0){				
					fputs(palavra, arquivoPreProcessado);

					if(palavra[0] != ch)
						fputc(ch, arquivoPreProcessado);
				}
				palavra = NULL;
				palavraLen = 0;
			} else 
				RealocaPalavra();	
		}	
	}
	if(palavraLen > 0){				
		fputs(palavra, arquivoPreProcessado);					
	}

    fclose(arquivoEntrada);
    fclose(arquivoPreProcessado);
}

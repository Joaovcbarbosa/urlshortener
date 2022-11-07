#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int laco = 1;
int estado = 0;
int novoEstado = 0;
int comentario = 0;

int aceitacao[3] = {0, 0, 1};
int transicao[3][3] = {
						{1,  -1, -1},
						{1,   1,  2},
						{-1, -1, -1}
					  };
int avanco[3][3] = {
						{1, 0, 0},
						{1, 1, 0},
						{0, 0, 0}
				   };

char palavraReservada[8][255] = {{"if"}, {"then"}, {"else"}, {"end"}, {"repeat"}, {"until"}, {"read"}, {"write"}};

char simbolosEspciais[10][255] = {{"+"}, {"-"}, {"*"}, {"/"}, {"="}, {"<"}, {"("}, {")"}, {";"}, {":="}};

char avancarCaracter(FILE *arquivo)
{
	char c = getc(arquivo);
	return c == EOF ? EOF : c;
}

char verificarProximoCaracter(FILE *arquivo)
{
	char c = getc(arquivo);
	return c == EOF ? EOF : ungetc(c, arquivo);
}

int ehPalavraReservada(char *bufferPalavra){
	int i;
    for(i = 0; i < 8; i++) {
        if(strcmp(bufferPalavra, palavraReservada[i]) == 0)
			return 1;
    }

	return 0;
}	

int ehIdentificador(char *bufferPalavra){	
	if(ehPalavraReservada(bufferPalavra) == 1)
		return 0;

	return 1;
}	

int ehLetra(int c){
	if((c >= 65 && c <= 90) || (c >= 97 && c <= 122))
		return 1;

	return 0;
}	

int ehDigito(int c){
	if(c >= 48 && c <= 57)
		return 1;

	return 0;
}	

int ehOutro(int c){
	if (ehDigito(c) == 0 && ehLetra(c) == 0)
		return 1;

	return 0;
}	

int ehComentario(int c, FILE *arquivo){
	if (c == 47 && verificarProximoCaracter(arquivo) == 42)
		return 1;

	return 0;
}	

int ehFimComentario(int c, FILE *arquivo){
	if (c == 42 && verificarProximoCaracter(arquivo) == 47)
		return 1;

	return 0;
}	

int grupo(int c){
	if (ehLetra(c) == 1) return 0;
	if (ehDigito(c) == 1) return 1;
	if (ehOutro(c) == 1) return 2;

	return -1;
}

int main()
{
	FILE *arquivoFonte = fopen("sort.txt", "r");
    FILE *arquivoDestino = fopen("saida.txt", "w");
	char c;

	while(c != EOF){
		char *bufferPalavra = '\0';
		int tamanhoBuffer = 0;
		int estado = 0;
		c = avancarCaracter(arquivoFonte);

		if (ehLetra(c) == 0) {
			if(ehComentario(c, arquivoFonte) == 1)
				comentario = 1;
			if(ehFimComentario(c, arquivoFonte) == 1)
				comentario = 0;

			fputc(c, arquivoDestino);
			continue; 
		}
		
		while (aceitacao[estado] == 0){
			novoEstado = transicao[estado][grupo(c)];
			if (avanco[estado][grupo(c)] == 1){
				tamanhoBuffer++;
				bufferPalavra = (char*)realloc(bufferPalavra, (tamanhoBuffer) * (sizeof(char)));
				bufferPalavra[tamanhoBuffer-1] = c;
				bufferPalavra[tamanhoBuffer] = '\0';
				c = avancarCaracter(arquivoFonte);	
			} 		
			estado = novoEstado;
		}		
		
		if(ehIdentificador(bufferPalavra) == 1 && comentario == 0)
			fputs("ID", arquivoDestino);
		else
			fputs(bufferPalavra, arquivoDestino);

		fputc(c, arquivoDestino);
		bufferPalavra = NULL;
		tamanhoBuffer = 0;
	}	
}

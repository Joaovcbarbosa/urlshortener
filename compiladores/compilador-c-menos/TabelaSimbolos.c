#include "TabelaSimbolos.h"

static int tabelaHash( char * chave ) { 
	int i = 0, aux = 0;
	while(chave[i] != '\0') { 
		aux = ((aux << TAMANHO_TAB) + chave[i]) % TAMANHO_TABELA_DE_SIMBOLOS; i++;
	}
	return aux;
}

void InsereTabelaDeSimbolos(char *nome, int tamanho, int numeroLinha, char *escopoVariavel, TipoPrimitivo tipo, int funcao) {
	int chaveHash = tabelaHash(nome);
	tabelaHashTipo valorHash = hashtable[chaveHash];

	while(valorHash != NULL && (strcmp(nome, valorHash->nome) != 0 || strcmp(valorHash->escopoVariavel, escopoVariavel) != 0 ))
		valorHash = valorHash->proximo;

	if(valorHash == NULL) {
		valorHash = (tabelaHashTipo) malloc(sizeof(struct estruturaHashTable));
		valorHash->nome = nome;
		valorHash->tamanho = tamanho;
		valorHash->linhas = (numeroLinhaTipo) malloc(sizeof(struct estruturaNumeroLinha));
		valorHash->linhas->numeroLinha = numeroLinha;
		if(!funcao) valorHash->id = ++contadorVariavel;
		if(strcmp(escopoVariavel, "global") == 0) {
			char* escopoGlobal = malloc(sizeof(char) * 8);
			strcat(escopoGlobal, "global");
			valorHash->escopoVariavel = escopoGlobal;
		} else 
			valorHash->escopoVariavel = escopoVariavel;
		
		valorHash->ehFuncao = funcao;
		valorHash->linhas->proximo = NULL;
		valorHash->tipo = tipo;
		valorHash->proximo = hashtable[chaveHash];
		hashtable[chaveHash] = valorHash; 
	} else { 
		numeroLinhaTipo linhasHash = valorHash->linhas;

		while (linhasHash->proximo != NULL)
			linhasHash = linhasHash->proximo;

		linhasHash->proximo = (numeroLinhaTipo) malloc(sizeof(struct estruturaNumeroLinha));
		linhasHash->proximo->proximo = NULL;
		linhasHash->proximo->numeroLinha = numeroLinha;
	}
}

int FuncaoJaDeclarada(char *nome) {
	int chaveHash = tabelaHash(nome);
	tabelaHashTipo valorHash = hashtable[chaveHash];
	while(valorHash != NULL && (strcmp(nome,valorHash->nome) != 0 || valorHash->ehFuncao == 0))
		valorHash = valorHash->proximo;

	return (valorHash == NULL) ? 0 : 1;
}

int VariavelJaDeclarada(char *nome) {
	int chaveHash = tabelaHash(nome);
	tabelaHashTipo valorHash = hashtable[chaveHash];
	while(valorHash != NULL && (strcmp(nome, valorHash->nome) != 0 || valorHash->ehFuncao == 1))
		valorHash = valorHash->proximo;

	return (valorHash == NULL) ? 0 : 1;
}

int VariavelJaDeclaradaNoEscopo(char *nome, char *escopoVariavel) {
	int chaveHash = tabelaHash(nome);
	tabelaHashTipo valorHash = hashtable[chaveHash];
	while(valorHash != NULL) {
		if((valorHash->ehFuncao == 0 && strcmp(nome, valorHash->nome) == 0) && strcmp(escopoVariavel, valorHash->escopoVariavel) == 0)
			break;
		valorHash = valorHash->proximo;
	}

	return (valorHash == NULL) ? 0 : 1;
}

int VariavelJaDeclaradaGlobal(char *nome) {
	int chaveHash = tabelaHash(nome);
	tabelaHashTipo valorHash = hashtable[chaveHash];;
	while(valorHash != NULL) {
		if((valorHash->ehFuncao == 0 && strcmp(nome, valorHash->nome) == 0) && strcmp(valorHash->escopoVariavel,"global") == 0)
			break;
		valorHash = valorHash->proximo;
	}

	return (valorHash == NULL) ? 0 : 1;
}

void RecebeTipoFuncao(char *nome, TipoPrimitivo *tipoPrimitivo) {
	int chaveHash = tabelaHash(nome);
	tabelaHashTipo valorHash =  hashtable[chaveHash];
	while((valorHash != NULL) && ((strcmp(nome,valorHash->nome) != 0)||(valorHash->ehFuncao == 0)))
		valorHash = valorHash->proximo;

	if(valorHash != NULL) 
		*tipoPrimitivo = valorHash->tipo;
}

void RecebeTipoVariavel(char *nome, char *escopoVariavel, TipoPrimitivo *tipoPrimitivo) {
	int chaveHash = tabelaHash(nome);
	tabelaHashTipo valorHash = hashtable[chaveHash];
	while((valorHash != NULL) && ((strcmp(nome,valorHash->nome) != 0)|| (strcmp(escopoVariavel,valorHash->escopoVariavel) != 0) ||(valorHash->ehFuncao == 1)))
		valorHash = valorHash->proximo;

	if(valorHash != NULL) 
		*tipoPrimitivo = valorHash->tipo;
}

void ImprimeTabelaDeSimbolos(FILE * arquivoSaida) {
	EscreveArquivo(arquivoSaida," |   Nome   |       Tipo      |   Escopo  |  Tamanho |            Linhas              \n");
	EscreveArquivo(arquivoSaida," |------------------------------------------------------------------------------------\n");

	for(int i = 0; i < TAMANHO_TABELA_DE_SIMBOLOS; i++) { 
		if(hashtable[i] != NULL) { 
			tabelaHashTipo valorHash = hashtable[i];

			while(valorHash != NULL) { 
				numeroLinhaTipo linhasHash = valorHash->linhas;
				fprintf(arquivoSaida, " |  %-6s ", valorHash->nome);				
				fprintf(arquivoSaida, " |  %-13s ", RecebeNomeTipo(valorHash->tipo));
				fprintf(arquivoSaida, " |  %-8s", valorHash->escopoVariavel);
				fprintf(arquivoSaida, " |  %-8d|", valorHash->tamanho);
				while(linhasHash != NULL) { 
					fprintf(arquivoSaida, "%4d ", linhasHash->numeroLinha);
					linhasHash = linhasHash->proximo;
				}
				EscreveArquivo(arquivoSaida,"\n");
				valorHash = valorHash->proximo;
			}
		}
	}

	EscreveArquivo(arquivoSaida," |-----------------------------------------------------------------------------------\n");
} 

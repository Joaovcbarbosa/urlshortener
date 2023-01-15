#include "Global.h"
typedef struct estruturaNumeroLinha { 
	struct estruturaNumeroLinha *proximo;
	int numeroLinha;
} *numeroLinhaTipo;
typedef struct estruturaHashTable { 
	char *nome, *escopoVariavel;
	int id, tamanho, ehFuncao; 
	struct estruturaHashTable* proximo;
	numeroLinhaTipo linhas;
	TipoPrimitivo tipo; 
} *tabelaHashTipo;
static tabelaHashTipo hashtable[TAMANHO_TABELA_DE_SIMBOLOS];
static int contadorVariavel = 0;
static int tabelaHash(char *chave);;
int FuncaoJaDeclarada(char *nome);
int VariavelJaDeclarada(char *nome);
int VariavelJaDeclaradaNoEscopo(char *nome, char *escopoVariavel);
int VariavelJaDeclaradaGlobal(char *nome);
void InsereTabelaDeSimbolos(char *nome, int tamanho, int numeroLinha, char *escopoVariavel, TipoPrimitivo tipo, int funcao);
void ImprimeTabelaDeSimbolos(FILE *arquivoSaida);


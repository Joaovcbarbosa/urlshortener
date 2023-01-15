#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define QUANTIDADE_MAXIMA_LINHAS 100
#define TAMANHO_MAXIMO_TOKEN 100
#define TAMANHO_MAXIMO_NOS_FILHOS 3
#define TAMANHO_TABELA_DE_SIMBOLOS 211
#define TAMANHO_TAB 4
#ifndef YYPARSER
#include "parse.tab.h"
#endif
extern FILE* arquivoEntrada;
static char* escopoVariavel = "global";
extern char* yytext;
int numeroLinha;
bool erro;
extern char tokenID[TAMANHO_MAXIMO_TOKEN];
extern char tokenNumero[TAMANHO_MAXIMO_TOKEN];
extern char tokenString[TAMANHO_MAXIMO_TOKEN];
static bool temFuncaoMain = false;
typedef int tipoToken;
typedef enum {noDeclaracao, noExpressao, noStatement} TipoNo;
typedef enum {declaracaoFuncao, declaracaoTipo, declaracaoVariavel} TipoDeclaracao;
typedef enum {statementAtribuicao, statementChamada, statementIf, statementReturn, statementWhile} TipoStatement;
typedef enum {expressaoID, expressaoNumero, expressaoOperacao} TipoExpressao;
typedef enum {Array, Boolean, Integer, Void} TipoPrimitivo;
int FuncaoJaDeclarada(char *nome);
int VariavelJaDeclarada(char *nome);
int VariavelJaDeclaradaNoEscopo(char *nome, char *escopo);
int VariavelJaDeclaradaGlobal(char *nome);
tipoToken RecebeToken();
void ImprimeTokens(char *nomeArquivo, FILE *arquivoSaida);
void EscreveArquivo(FILE *arquivoSaida, char *str);;
char *CopiarString(char *str);
char *RecebeNomeToken(tipoToken token);
char *RecebeNomeTipo(TipoPrimitivo t);
typedef struct estruturaPilha{ 
	struct estruturaPilha *proximo; 
	char *nome; 
} pilha;
typedef struct { 
	pilha* top; 
	int tamanho; 
} tipoPilha;
void  IniciaPilha(tipoPilha *pilha);
void  PushPilha(tipoPilha *pilha, char *nome);
char *PopPilha(tipoPilha *pilha);
typedef struct no {
	struct no *nosFilhos[TAMANHO_MAXIMO_NOS_FILHOS];
	struct no *nosIrmaos;
	int numeroLinha;
	TipoNo tipoNo;
	TipoPrimitivo tipoPrimitivo;
	union {
		char *nome;
		tipoToken simbolo;
		int valor;
	} valores;
	union { 
		TipoDeclaracao declaracao; 
		TipoExpressao expressao;
		TipoStatement statement; 
	} tipo;
} no;

no *parse(void);
no *IniciaNo(TipoNo tipoNo);
no *CriaNoDeclaracao(TipoDeclaracao tipo);
no *CriaNoStatement(TipoStatement tipo);
no *CriaNoExpressao(TipoExpressao tipo);
no* arvoreSintatica;
void ImprimeArvoreSintatica(no *arvore, FILE *arquivoSaida);
void AnaliseLexica(char *nomeArquivoEntrada, FILE *arquivoSaida);
void AnaliseSintatica(char *nomeArquivoEntrada, FILE *arquivoSaida);
void InsereTabelaDeSimbolos(char *nome, int length, int numeroLinha, char *escopo, TipoPrimitivo tipo, int isFunction);
void ImprimeTabelaDeSimbolos(FILE *arquivoSaida);
void IniciaTabelaDeSimbolos(no *arvore, FILE *arquivoSaida); 
void TabelaDeSimbolos(FILE *arquivoSaida);
void AnaliseSemantica(FILE *arquivoSaida);
void RecebeTipoFuncao(char *nome, TipoPrimitivo *tipoPrimitivo);
void RecebeTipoVariavel(char* nome, char* escopoVariavel, TipoPrimitivo* tipoPrimitivo);;
void VerificaTipoNo(no * arvore, FILE *out);



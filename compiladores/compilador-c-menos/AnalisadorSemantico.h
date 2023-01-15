#ifndef AnalisadorSemantico_H
#define AnalisadorSemantico_H
#include "Global.h"
static void InsereNo(no *t);
static void ImprimePosOrdem(no *arvore);
static void ImprimePreOrdem(no *arvore);
static void VerificaNo(no *t);
void VerificaTipoNo(no * arvore, FILE *arquivoSaida);
void IniciaTabelaDeSimbolos(no *arvore, FILE *arquivoSaida);
static void MensagemErro(no *t, char *message);
#endif

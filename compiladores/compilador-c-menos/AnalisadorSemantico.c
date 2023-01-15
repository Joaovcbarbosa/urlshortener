#include "AnalisadorSemantico.h"

void IniciaTabelaDeSimbolos(no *arvore, FILE *arquivoSaida) { 
	ImprimePreOrdem(arvore);

	if(!temFuncaoMain) {
		fprintf(stdout, "ERRO SEMÂNTICO: Função main não declarada!\n");
		erro = true;
	} else ImprimeTabelaDeSimbolos(arquivoSaida);
	
}

static void InsereNo(no *t) { 
	TipoPrimitivo *tipoPrimitivo = (TipoPrimitivo*) malloc(sizeof(TipoPrimitivo));

	switch (t->tipoNo){
		case noDeclaracao:
			switch (t->tipo.declaracao)
			{ 
				case declaracaoFuncao:
					if(strcmp(t->valores.nome, "main") == 0) 
						temFuncaoMain = true;
					if(strcmp(t->valores.nome, "input") == 0 || strcmp(t->valores.nome, "output") == 0) {
						printf("ERRO SEMÂNTICO | LINHA %d: Função %s é reservada!\n", t->numeroLinha, t->valores.nome);
						erro = true;
					} else {
						if(FuncaoJaDeclarada(t->valores.nome) == 0) {
							InsereTabelaDeSimbolos(t->valores.nome, 0, t->numeroLinha, "global", t->tipoPrimitivo, 1);
							escopoVariavel = t->valores.nome;
						} else {
							printf("ERRO SEMÂNTICO | LINHA %d: Função %s já declarada!\n", t->numeroLinha, t->valores.nome);
							erro = true;
						}
					}
				break;
				case declaracaoVariavel:
					if(t->tipoPrimitivo == Void) {
						MensagemErro(t, "Variável não é do tipo INT.\n");
						erro = true;
					}
					if (VariavelJaDeclarada(t->valores.nome) == 0) {
						if(t->nosFilhos[0] == NULL)
							InsereTabelaDeSimbolos(t->valores.nome, 1, t->numeroLinha, escopoVariavel, t->tipoPrimitivo, 0);
						else
							InsereTabelaDeSimbolos(t->valores.nome, t->nosFilhos[0]->valores.valor, t->numeroLinha, escopoVariavel, t->tipoPrimitivo, 0);
					} else {
						if(strcmp(escopoVariavel, "global") != 0) {
							if(VariavelJaDeclaradaNoEscopo(t->valores.nome, escopoVariavel) == 0) {
								if(t->nosFilhos[0] == NULL)
									InsereTabelaDeSimbolos(t->valores.nome, 1, t->numeroLinha, escopoVariavel, t->tipoPrimitivo, 0);
								else
									InsereTabelaDeSimbolos(t->valores.nome, t->nosFilhos[0]->valores.valor, t->numeroLinha, escopoVariavel, t->tipoPrimitivo, 0);
							} else {
								printf("ERRO SEMÂNTICO | LINHA %d: Variável %s já declarada!\n", t->numeroLinha, t->valores.nome);
								erro = true;
							}
						} 
						else {
							printf("ERRO SEMÂNTICO | LINHA %d: Variável global %s já declarada!\n", t->numeroLinha, t->valores.nome);
							erro = true;
						}
					}
				break;
				default: break;
			}
		break;
		case noStatement:
			switch (t->tipo.statement)
			{ 
				case statementChamada:
					if(strcmp(t->valores.nome, "input") == 0) { t->tipoPrimitivo = Integer; } 
					else if(strcmp(t->valores.nome, "output") == 0) { t->tipoPrimitivo = Integer; } 
					else if(FuncaoJaDeclarada(t->valores.nome) == 0) { 
						printf("ERRO SEMÂNTICO | LINHA: %d: Função %s não declarada!\n", t->numeroLinha, t->valores.nome);
						erro = true;
					} 
					else {
						RecebeTipoFuncao(t->valores.nome, tipoPrimitivo);
						t->tipoPrimitivo = *tipoPrimitivo;
						InsereTabelaDeSimbolos(t->valores.nome, 0, t->numeroLinha, "global", t->tipoPrimitivo, 1);
					}
				break;
				default: break;
			}
		break;
		case noExpressao:
			switch (t->tipo.expressao)
			{
				case expressaoID:
					if(strcmp(t->valores.nome, "void") != 0) {
						if(VariavelJaDeclarada(t->valores.nome) == 0) {
							printf("ERRO SEMÂNTICO | LINHA %d: Variável %s não declarada\n", t->numeroLinha, t->valores.nome);
							erro = true;
						} 
						else if(VariavelJaDeclaradaNoEscopo(t->valores.nome, escopoVariavel) == 1) {
							RecebeTipoVariavel(t->valores.nome, escopoVariavel, tipoPrimitivo);;
							if(t->tipoPrimitivo == Void) 
								t->tipoPrimitivo = *tipoPrimitivo;
							InsereTabelaDeSimbolos(t->valores.nome, 0, t->numeroLinha, escopoVariavel, t->tipoPrimitivo, 0);
						} 
						else {
							if(VariavelJaDeclaradaGlobal(t->valores.nome) == 0) {
								printf("ERRO SEMÂNTICO | LINHA %d: Variável %s não declarada\n",t->numeroLinha,t->valores.nome);
								erro = true;
							} 
							else {
								RecebeTipoVariavel(t->valores.nome, "global", tipoPrimitivo);
								if(t->tipoPrimitivo == Void) 
									t->tipoPrimitivo = *tipoPrimitivo;
								InsereTabelaDeSimbolos(t->valores.nome, 0, t->numeroLinha, "global", t->tipoPrimitivo, 0);
							}
						}
					}
				break;
				default:
					break;
			}
		break;
		default: 
			break;
	}
	free(tipoPrimitivo);
}

static void ImprimePosOrdem(no *arvore) { 
	if(arvore != NULL) { 
		for(int i=0; i < TAMANHO_MAXIMO_NOS_FILHOS; i++) 
			ImprimePosOrdem(arvore->nosFilhos[i]); 
		VerificaNo(arvore);
		ImprimePosOrdem(arvore->nosIrmaos);
	}
}

static void ImprimePreOrdem(no *arvore) { 
	if(arvore != NULL) { 
		InsereNo(arvore);
		for(int i=0; i < TAMANHO_MAXIMO_NOS_FILHOS; i++) 
			ImprimePreOrdem(arvore->nosFilhos[i]); 
		ImprimePreOrdem(arvore->nosIrmaos);
	}
}

static void VerificaNo(no *t) {
	switch (t->tipoNo)
	{ 
		case noExpressao:
			switch (t->tipo.expressao)
			{
				case expressaoOperacao:
					if((t->nosFilhos[0]->tipoPrimitivo != Integer) || (t->nosFilhos[1]->tipoPrimitivo != Integer))
						MensagemErro(t," Operação aplicada entre não inteiros!\n");
					else
						t->tipoPrimitivo = Integer;

					t->tipoPrimitivo = Integer;
					if(
						(t->valores.simbolo == IGUAL) 
						||	(t->valores.simbolo == DIFERENTE)  
						|| (t->valores.simbolo == MENOR_QUE) 
						|| (t->valores.simbolo == MENOR_OU_IGUAL_QUE)  
						|| (t->valores.simbolo == MAIOR_QUE)   
						|| (t->valores.simbolo == MAIOR_OU_IGUAL_QUE)
					)
						t->tipoPrimitivo = Boolean;
					else
						t->tipoPrimitivo = Integer;
				break;
				default: break;
			}
		break;
		case noStatement:
			switch (t->tipo.statement)
			{
				case statementIf:
					if (t->nosFilhos[0]->tipoPrimitivo == Integer) 
						MensagemErro(t->nosFilhos[0], "IF não é do tipo boolean.\n");
				break;
				case statementAtribuicao:
					if (t->nosFilhos[1]->tipoPrimitivo != t->nosFilhos[0]->tipoPrimitivo) 
						MensagemErro(t->nosFilhos[1], "Tipo da váriável e do valor a ser atribuído não condizentes.\n");
				break;
				case statementWhile:
					if (t->nosFilhos[0]->tipoPrimitivo == Integer) 
						MensagemErro(t->nosFilhos[0], "WHILE não é do tipo boolean.\n");
				break;
				default:
					break;
			}
		break;
		default: 
			break;
	}
}

void VerificaTipoNo(no * arvore, FILE *arquivoSaida) {
	ImprimePosOrdem(arvore);
}

static void MensagemErro(no *t, char *message) {
	erro = true;
	if(t->tipoNo != noExpressao && t->tipo.expressao != expressaoID)
		fprintf(stdout,"ERRO SEMÂNTICO | LINHA %d: %s\n", t->numeroLinha, message);
	else
		fprintf(stdout,"ERRO SEMÂNTICO:%s | LINHA %d: %s\n", t->valores.nome, t->numeroLinha, message);
}

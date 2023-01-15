%{
	#define YYPARSER 
	#include "Global.h"
	#define YYSTYPE no*  
	static int yylex();
	int yyerror(char *error_msg);
	static char *nomeAtributo, *nomeVariavel, *nomeFuncao;
	static tipoPilha pilhaFuncao;   
	static bool flagID = true;  
	static int numeroLinhaCorrente, numeroLinhaFuncaoCorrente;;  
	static no* arvoreRetornar;
%}

	%token IF ELSE WHILE RETURN INT VOID
	%token ID NUM
	%token ATRIBUICAO IGUAL DIFERENTE MENOR_QUE MAIOR_QUE MENOR_OU_IGUAL_QUE MAIOR_OU_IGUAL_QUE ADICAO SUBTRACAO MULTIPLICACAO DIVISAO
	%token ABRE_PARENTESES FECHA_PARENTESES ABRE_COLCHETES FECHA_COLCHETES ABRE_CHAVES FECHA_CHAVES PONTO_E_VIRGULA VIRGULA COMENT
	%token espaco novaLinha
	%token ERROR FIMARQ

%% 

	programa : declaracaoLista { 
		arvoreRetornar = $1;
	};

	declaracaoLista : declaracaoLista declaracao { 
	
		YYSTYPE aux = $1;
		if(aux != NULL) 
		{
			while(aux->nosFilhos[0]->nosIrmaos != NULL) { 
				aux = aux->nosFilhos[0]->nosIrmaos; 
			}
			aux->nosFilhos[0]->nosIrmaos = $2;

			$$ = $1;
		}
		else $$ = $2;
	}   
	| declaracao { $$ = $1; };

	declaracao : declaracaoVariavel { 
		$$ = $1; 
	} | declaracaoFuncao { 
		$$ = $1; 
	};

	declaracaoVariavel : tipoEspecificador ID { 
		nomeAtributo = CopiarString(tokenID);
		numeroLinhaCorrente = numeroLinha;
	} 
	PONTO_E_VIRGULA {
		$$ = $1;
		YYSTYPE no = CriaNoDeclaracao(declaracaoVariavel);
		no->valores.nome = nomeAtributo;
		no->numeroLinha = numeroLinhaCorrente;
		no->tipoPrimitivo = $1->tipoPrimitivo;
		$$->nosFilhos[0] = no;
	}
	| tipoEspecificador ID { 
		nomeAtributo = CopiarString(tokenID);
		numeroLinhaCorrente = numeroLinha;
	}
	ABRE_COLCHETES NUM FECHA_COLCHETES PONTO_E_VIRGULA { 
		$$ = $1;
		YYSTYPE noExpressao = CriaNoExpressao(expressaoNumero);
		noExpressao->valores.valor = atoi(tokenNumero);
		noExpressao->tipoPrimitivo = Integer;
		YYSTYPE no = CriaNoDeclaracao(declaracaoVariavel);
		no->valores.nome = nomeAtributo;
		no->numeroLinha = numeroLinhaCorrente;
		no->nosFilhos[0] = noExpressao;
		if($1->tipoPrimitivo == Integer)
		no->tipoPrimitivo = Array;
		else
		no->tipoPrimitivo = Void;
		$$->nosFilhos[0] = no; 
	};

	declaracaoFuncao : tipoEspecificador ID {
		nomeFuncao = CopiarString(tokenID);
		numeroLinhaFuncaoCorrente = numeroLinha;
	}
	ABRE_PARENTESES parametros FECHA_PARENTESES compostoDeclaracao{
		$$ = $1;
		YYSTYPE noFuncao = CriaNoDeclaracao(declaracaoFuncao);
		noFuncao->nosFilhos[0] = $5;
		noFuncao->nosFilhos[1] = $7;
		noFuncao->valores.nome = nomeFuncao;
		noFuncao->numeroLinha = numeroLinhaFuncaoCorrente;
		noFuncao->tipoPrimitivo = $1->tipoPrimitivo;
		$$->nosFilhos[0] = noFuncao;
	};

	tipoEspecificador : INT { 
		$$ = CriaNoDeclaracao(declaracaoTipo); 
		$$->tipoPrimitivo = Integer; 
	} 
	| VOID { 
		$$ = CriaNoDeclaracao(declaracaoTipo); 
		$$->tipoPrimitivo = Void; 
	};	

	parametros : listaParametros { 
		$$ = $1; 
	} 
	| VOID { 
		$$ = CriaNoExpressao(expressaoID); 
		$$->valores.nome = "void"; 
		$$->tipoPrimitivo = Void;
	};

	listaParametros : listaParametros VIRGULA parametro { 
		YYSTYPE aux = $1;
		if(aux != NULL)
		{
			while(aux->nosIrmaos != NULL) 
				aux = aux->nosIrmaos;
			aux->nosIrmaos = $3;
			$$ = $1;
		} 
		else $$ = $3; 
	} 
	| parametro { $$ = $1; };

	parametro : tipoEspecificador ID { 
		$$ = $1;
		nomeAtributo = CopiarString(tokenID);
		numeroLinhaCorrente = numeroLinha;
		YYSTYPE noDeclaracao = CriaNoDeclaracao(declaracaoVariavel); 
		noDeclaracao->valores.nome = nomeAtributo;
		noDeclaracao->numeroLinha = numeroLinhaCorrente;
		noDeclaracao->tipoPrimitivo = $1->tipoPrimitivo;
		$$->nosFilhos[0] = noDeclaracao;
	} 
	| tipoEspecificador ID {
		nomeAtributo = CopiarString(tokenID);
		numeroLinhaCorrente = numeroLinha;
	}
	ABRE_COLCHETES FECHA_COLCHETES{    
		$$ = $1;
		YYSTYPE noDeclaracao = CriaNoDeclaracao(declaracaoVariavel);
		noDeclaracao->valores.nome = nomeAtributo;
		noDeclaracao->numeroLinha = numeroLinhaCorrente;
		if($1->tipoPrimitivo == Integer)
			noDeclaracao->tipoPrimitivo = Array;
		else
			noDeclaracao->tipoPrimitivo = $1->tipoPrimitivo;

		$$->nosFilhos[0] = noDeclaracao;
	};

	compostoDeclaracao : ABRE_CHAVES localDeclaracao listaStatement FECHA_CHAVES { 
		YYSTYPE aux = $2;

		if(aux != NULL)	{
			while(aux->nosIrmaos != NULL) 
				aux = aux->nosIrmaos;

			aux->nosIrmaos = $3;
			$$ = $2;
		}
		else $$ = $3;
	};

	localDeclaracao : localDeclaracao declaracaoVariavel { 
		YYSTYPE aux = $1;
		if(aux != NULL) {
			while(aux->nosIrmaos != NULL) 
				aux = aux->nosIrmaos;
			aux->nosIrmaos = $2;
			$$ = $1;
		}
		else $$ = $2;
	} 
	| { $$ = NULL; };	

	listaStatement : listaStatement statement { 
		YYSTYPE aux = $1;
		if(aux != NULL)	{
			while(aux->nosIrmaos != NULL) 
				aux = aux->nosIrmaos;
			aux->nosIrmaos = $2;
			$$ = $1;
		}
		else $$ = $2;		
	} 
	| { $$ = NULL; };

	statement :   expressaoDeclaracao  { $$ = $1; }
				| compostoDeclaracao { $$ = $1; }
				| selecaoDeclaracao  { $$ = $1; }
				| iteracaoDeclaracao { $$ = $1; }
				| retornoDeclaracao  { $$ = $1; };

	expressaoDeclaracao : expressao PONTO_E_VIRGULA 
		{ $$ = $1; } 
	| PONTO_E_VIRGULA { $$ = NULL; };

	selecaoDeclaracao : IF ABRE_PARENTESES expressao FECHA_PARENTESES statement	{ 
		$$ = CriaNoStatement(statementIf);
		$$->nosFilhos[0] = $3;
		$$->nosFilhos[1] = $5;
	}
	| IF ABRE_PARENTESES expressao FECHA_PARENTESES statement ELSE statement{ 
		$$ = CriaNoStatement(statementIf);
		$$->nosFilhos[0] = $3;
		$$->nosFilhos[1] = $5;
		$$->nosFilhos[2] = $7;
	};

	iteracaoDeclaracao : WHILE ABRE_PARENTESES expressao FECHA_PARENTESES statement	{ 
		$$ = CriaNoStatement(statementWhile);
		$$->nosFilhos[0] = $3;
		$$->nosFilhos[1] = $5;
	};

	retornoDeclaracao : RETURN PONTO_E_VIRGULA { 
		$$ = CriaNoStatement(statementReturn);
	}    
	| RETURN expressao PONTO_E_VIRGULA {
		$$ = CriaNoStatement(statementReturn);
		$$->nosFilhos[0] = $2;
	};

	expressao : var ATRIBUICAO expressao{ 
		$$ = CriaNoStatement(statementAtribuicao);
		$$->nosFilhos[0] = $1;
		$$->nosFilhos[1] = $3;
		$$->tipoPrimitivo = Integer;
		$$->valores.simbolo = ATRIBUICAO; 
	}
	| simplesExpressao { $$ = $1; };

	var : ID { 
		nomeAtributo = CopiarString(tokenID);
		numeroLinhaCorrente = numeroLinha;
		$$ = CriaNoExpressao(expressaoID);
		$$->valores.nome = nomeAtributo;
		$$->numeroLinha = numeroLinhaCorrente;
		$$->tipoPrimitivo = Void;
	}
	| ID { 
		nomeVariavel = CopiarString(tokenID);
		numeroLinhaCorrente = numeroLinha;
	} 
	ABRE_COLCHETES expressao FECHA_COLCHETES {
		$$ = CriaNoExpressao(expressaoID);
		$$->valores.nome = nomeVariavel;
		$$->numeroLinha = numeroLinhaCorrente;
		$$->nosFilhos[0] = $4;
		$$->tipoPrimitivo = Integer; 
	};

	simplesExpressao : somaExpressao relacional somaExpressao{ 
		$$ = CriaNoExpressao(expressaoOperacao);

		$$->nosFilhos[0] = $1;
		$$->nosFilhos[1] = $3;
		$$->valores.simbolo = $2->valores.simbolo; 
	} 
	| somaExpressao { $$ = $1; };

	relacional : MENOR_OU_IGUAL_QUE { 
		$$ = CriaNoExpressao(expressaoID); 
		$$->valores.simbolo = MENOR_OU_IGUAL_QUE; 
	}
	| MENOR_QUE { 
		$$ = CriaNoExpressao(expressaoID); 
		$$->valores.simbolo = MENOR_QUE; 
	}
	| MAIOR_QUE { 
		$$ = CriaNoExpressao(expressaoID); 
		$$->valores.simbolo = MAIOR_QUE; 
	}
	| MAIOR_OU_IGUAL_QUE { 
		$$ = CriaNoExpressao(expressaoID); 
		$$->valores.simbolo = MAIOR_OU_IGUAL_QUE; 
	}
	| IGUAL { 
		$$ = CriaNoExpressao(expressaoID); 
		$$->valores.simbolo = IGUAL; 
	}
	| DIFERENTE { 
		$$ = CriaNoExpressao(expressaoID); 
		$$->valores.simbolo = DIFERENTE; 
	};	  

	somaExpressao : somaExpressao soma termo{ 
		$$ = CriaNoExpressao(expressaoOperacao);
		$$->nosFilhos[0] = $1;
		$$->nosFilhos[1] = $3;
		$$->valores.simbolo = $2->valores.simbolo; 
	} 
	| termo { $$ = $1; };

	soma : ADICAO { 
		$$ = CriaNoExpressao(expressaoID); 
		$$->valores.simbolo = ADICAO; 
	}
	| SUBTRACAO {
		$$ = CriaNoExpressao(expressaoID); 
		$$->valores.simbolo = SUBTRACAO;
	};			
	
	termo : termo mult fator {
		$$ = CriaNoExpressao(expressaoOperacao);
		$$->nosFilhos[0] = $1;
		$$->nosFilhos[1] = $3;
		$$->valores.simbolo = $2->valores.simbolo; 
	} 
	| fator { $$ = $1; };

	mult : MULTIPLICACAO { 
		$$ = CriaNoExpressao(expressaoID); 
		$$->valores.simbolo = MULTIPLICACAO;
	}
	| DIVISAO {
		$$ = CriaNoExpressao(expressaoID); 
		$$->valores.simbolo = DIVISAO;
	};

	fator : ABRE_PARENTESES expressao FECHA_PARENTESES { $$ = $1; }
			| var { $$ = $1; }
			| ativacao { $$ = $1; }
			| NUM { 
				$$ = CriaNoExpressao(expressaoNumero);
				$$->valores.valor = atoi(tokenNumero);
				$$->tipoPrimitivo = Integer;
			};

	ativacao : ID { 
		if(flagID == true)
		{
			IniciaPilha(&pilhaFuncao);
			flagID = false;
		}
		PushPilha(&pilhaFuncao, CopiarString(tokenID));
		numeroLinhaCorrente = numeroLinha;
	}	
	ABRE_PARENTESES argumentos FECHA_PARENTESES { 
		$$ = CriaNoStatement(statementChamada);
		$$->nosFilhos[1] = $4; 
		$$->valores.nome = PopPilha(&pilhaFuncao);
		$$->numeroLinha = numeroLinhaCorrente;
	};

	argumentos : listaArgumentos { $$ = $1; } 
				 | { $$ = NULL; };

	listaArgumentos : listaArgumentos VIRGULA expressao { 
		YYSTYPE aux = $1;

		if(aux != NULL){
			while(aux->nosIrmaos != NULL)
				aux = aux->nosIrmaos;
			aux->nosIrmaos = $3;
			$$ = $1;
		}
		else $$ = $3;
	} 
	| parametro { $$ = $1; } 
	| expressao { $$ = $1; };

%%

int yyerror(char *error_msg) {
	char* nomeToken = RecebeNomeToken(yychar);

	if(yychar == ID || yychar == NUM) { fprintf(stdout,"ERRO SINTÁTICO %s | LINHA : %d\n", nomeToken, numeroLinha); }
	else{ fprintf(stdout,"ERRO SINTÁTICO %s (%s) | LINHA: %d\n", nomeToken, yytext, numeroLinha); }

	erro = true; free(nomeToken);

	return -1;
}

static int yylex(void) { 
	return RecebeToken(); 
}

no *parse(void) { 
	yyparse(); 
	return arvoreRetornar; 
}

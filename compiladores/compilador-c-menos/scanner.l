%{
	#include "Global.h"
	char tokenID[TAMANHO_MAXIMO_TOKEN], tokenNumero[TAMANHO_MAXIMO_TOKEN], tokenString[TAMANHO_MAXIMO_TOKEN];
%}

digito [0-9]
letra [a-zA-Z]
identificador {letra}+
novaLinha \n
numero {digito}+
espaco [ \t]+

%%
"="      { return ATRIBUICAO; }
"]"      { return FECHA_COLCHETES; }
"}"      { return FECHA_CHAVES; }
","      { return VIRGULA; }
")"      { return FECHA_PARENTESES; }
"!="     { return DIFERENTE; }
"else"   { return ELSE; }
"=="     { return IGUAL;}
">"      { return MAIOR_QUE; }
">="     { return MAIOR_OU_IGUAL_QUE; }
"if"     { return IF; }
"int"    { return INT; }
"<"      { return MENOR_QUE; }
"<="     { return MENOR_OU_IGUAL_QUE; }
"-"      { return SUBTRACAO;}
"["      { return ABRE_COLCHETES; }
"{"      { return ABRE_CHAVES; }
"("      { return ABRE_PARENTESES; }
"+"      { return ADICAO; }
"return" { return RETURN; }
";"      { return PONTO_E_VIRGULA; }
"/"      { return DIVISAO; }
"*"      { return MULTIPLICACAO; }
"void"   { return VOID; }
"while"  { return WHILE; }

{identificador} { 
	strncpy(tokenID, yytext, TAMANHO_MAXIMO_TOKEN);
	return ID; 
}
{novaLinha} { numeroLinha++; }
{numero} { 
	strncpy(tokenNumero, yytext, TAMANHO_MAXIMO_TOKEN); 
	return NUM;
}
{espaco} {}

. { 
	printf("ERRO LÉXICO: %s | LINHA: %d\n", yytext, numeroLinha);
	erro = true;
	return ERROR; 
}

<<EOF>> { return EOF;}
%%

tipoToken RecebeToken(void) {
static bool flagPrimeiro = 1;
tipoToken token;
if (flagPrimeiro) {
	flagPrimeiro = 0;
	numeroLinha++;
	yyin = arquivoEntrada;
	yyout = stdout;
}
token = yylex();
strncpy(tokenString, yytext, TAMANHO_MAXIMO_TOKEN);
return token;
}

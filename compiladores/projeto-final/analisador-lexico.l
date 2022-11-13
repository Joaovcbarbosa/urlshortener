%{

#include <stdlib.h>
#include <stdio.h>
#define OPEN_BRACKETS 100
#define CLOSE_BRACKETS 101
#define OPEN_BRACES 102
#define CLOSE_BRACES 103
#define OPEN_PARENTHESES 104
#define CLOSE_PARENTHESES 105
#define OPEN_COMMENT 106
#define CLOSE_COMMENT 107
#define ASSIGN 108
#define DIFFERENT 109
#define EQUAL 110
#define GREATER 111
#define GREATER_EQUAL 112
#define LESS 113
#define LESS_EQUAL 114
#define DIVIDED 115
#define TIMES 116
#define MINUS 117
#define PLUS 118
#define NUM 119
#define IF 120
#define ELSE  121
#define INT 122
#define VOID 123
#define WHILE 124
#define RETURN 125
#define ID 126
#define COMMA 127
#define SEMICOLON 128
#define NEW_LINE 129
#define SPACE 130
#define INVALID 131
%}

digit [0-9]
letter [a-zA-Z]
identifier {letter}({letter}|{digit})*
newLine \n
number {digit}+
space [ \t]+

%%

"["      return OPEN_BRACKETS;
"]"      return CLOSE_BRACKETS;
"{"      return OPEN_BRACES;
"}"      return CLOSE_BRACES;
"("      return OPEN_PARENTHESES;
")"      return CLOSE_PARENTHESES;
"/*"     return OPEN_COMMENT;
"*/"     return CLOSE_COMMENT;
"="      return ASSIGN;
"!="     return DIFFERENT;
"=="     return EQUAL;
">"      return GREATER;
">="     return GREATER_EQUAL;
"<"      return LESS;
"<="     return LESS_EQUAL;
"/"      return DIVIDED;
"*"      return TIMES;
"-"      return MINUS;
"+"      return PLUS;
"if"     return IF;
"else"   return ELSE;
"int"    return INT;
"void"   return VOID;
"while"  return WHILE;
"return" return RETURN;
","      return COMMA;
";"      return SEMICOLON;
"FIM"      return EOF;
{identifier} return ID;
{newLine} return NEW_LINE;
{number} return NUM;
{space} return SPACE;
<<EOF>> return EOF;

%%

int main(int argc, char *argv[])
{
  int token, i, buf[100];
  FILE *f_in;
 
  for (i=0;i<=99;i++) buf[i] = 0;
 

  if (argc == 2)
  {
    if(f_in = fopen(argv[1],"r"))  yyin = f_in;
    else  perror(argv[0]);
  }
  else  yyin = stdin;
  
  i = 0;
  while ((token=yylex())!=EOF)
  {
    buf[i] = token;
    i++;
  }

  i = 0;
  while (buf[i] != 0)
  {
    switch(buf[i])
    {
        case OPEN_BRACKETS: printf("[ -> ABRE COLCHETES\n"); break;
        case CLOSE_BRACKETS: printf("] -> FECHA COLCHETES\n"); break;
        case OPEN_BRACES: printf("{ -> ABRE CHAVES\n"); break;
        case CLOSE_BRACES: printf("} -> FECHA CHAVES\n"); break;
        case OPEN_PARENTHESES: printf("( -> ABRE PARENTESES\n"); break;
        case CLOSE_PARENTHESES: printf(") -> ABRE PARENTESES\n"); break;
        case OPEN_COMMENT: printf("/* -> ABRE COMENTARIO\n"); break;
        case CLOSE_COMMENT: printf("*/ -> FECHA COMENTARIO\n"); break;
        case ASSIGN: printf("= -> ATRIBUICAO\n"); break;
        case DIFFERENT: printf("!= -> DIFERENTE DE\n"); break;
        case EQUAL: printf("== -> IGUAL A\n"); break;
        case GREATER: printf("> -> MAIOR QUE\n"); break;
        case GREATER_EQUAL: printf(">= -> MAIOR OU IGUAL QUE\n"); break;
        case LESS: printf("< -> MENOR QUE\n"); break;
        case LESS_EQUAL: printf("<= -> MENOR OU IGUAL QUE\n"); break;
        case DIVIDED: printf("/ -> DIVIDIDO POR\n"); break;
        case TIMES: printf("* -> VEZES\n"); break;
        case MINUS: printf("- -> MENOS\n"); break;
        case PLUS: printf("+ -> MAIS\n"); break;
        case NUM: printf("NUMERO\n"); break;
        case IF: printf("if -> SE\n"); break;
        case ELSE: printf("else -> SENAO\n"); break;
        case INT: printf("PALAVRA RESERVADA\n"); break;
        case VOID: printf("PALAVRA RESERVADA\n"); break;
        case WHILE: printf("PALAVRA RESERVADA\n"); break;
        case RETURN: printf("PALAVRA RESERVADA\n"); break;
        case ID: printf("IDENTIFICADOR\n"); break;
        case COMMA: printf(", -> VIRGULA\n"); break;
        case SEMICOLON: printf("; -> PONTO E VIRGULA\n"); break;
        //case NEW_LINE: printf("NOVA LINHA\n"); break;
        case SPACE: printf("ESPACO\n"); break;
        case INVALID: printf("INVALIDO\n"); break;
    }
    i++;
  }
  return(0);
}

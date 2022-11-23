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
  int token, i, j, len, buffer[100000], comment;
  char lexemas[100000][60];
  FILE *inputFile;
  
  comment = 0; 
  for (i=0;i<=99999;i++) buffer[i] = 0; 

  if (argc == 2){
    if(inputFile = fopen(argv[1],"r"))  yyin = inputFile;
    else  perror(argv[0]);
  }
  else  yyin = stdin;
  
  i = 0;
  while ((token=yylex())!=EOF)
  {
    if(token == OPEN_COMMENT)
      comment = 1;
    
    if(token == CLOSE_COMMENT){
      comment = 0;
      continue;
    }

    if(comment == 0){
      buffer[i] = token;
      len = strlen(yytext);
      j = 0;
      for(j; j < len; j++)
        lexemas[i][j] = yytext[j];   

      i++;
    }
  }

  i = 0;
  while (buffer[i] != 0)
  {
    switch(buffer[i])
    {
        case OPEN_BRACKETS: printf("%s -> ABRE COLCHETES\n", lexemas[i]); break;
        case CLOSE_BRACKETS: printf("%s -> FECHA COLCHETES\n", lexemas[i]); break;
        case OPEN_BRACES: printf("%s -> ABRE CHAVES\n", lexemas[i]); break;
        case CLOSE_BRACES: printf("%s -> FECHA CHAVES\n", lexemas[i]); break;
        case OPEN_PARENTHESES: printf("%s -> ABRE PARENTESES\n", lexemas[i]); break;
        case CLOSE_PARENTHESES: printf("%s -> ABRE PARENTESES\n", lexemas[i]); break;
        case OPEN_COMMENT: printf("%s -> ABRE comment\n", lexemas[i]); break;
        case CLOSE_COMMENT: printf("%s -> FECHA comment\n", lexemas[i]); break;
        case ASSIGN: printf("%s -> ATRIBUICAO\n", lexemas[i]); break;
        case DIFFERENT: printf("%s -> DIFERENTE DE\n", lexemas[i]); break;
        case EQUAL: printf("%s -> IGUAL A\n", lexemas[i]); break;
        case GREATER: printf("%s -> MAIOR QUE\n", lexemas[i]); break;
        case GREATER_EQUAL: printf("%s -> MAIOR OU IGUAL QUE\n", lexemas[i]); break;
        case LESS: printf("%s -> MENOR QUE\n", lexemas[i]); break;
        case LESS_EQUAL: printf("%s -> MENOR OU IGUAL QUE\n", lexemas[i]); break;
        case DIVIDED: printf("%s -> DIVIDIDO POR\n", lexemas[i]); break;
        case TIMES: printf("%s -> VEZES\n", lexemas[i]); break;
        case MINUS: printf("%s -> MENOS\n", lexemas[i]); break;
        case PLUS: printf("%s -> MAIS\n", lexemas[i]); break;
        case NUM: printf("%s -> NUMERO\n", lexemas[i]); break;
        case IF: printf("%s -> PALAVRA RESERVADA\n", lexemas[i]); break;
        case ELSE: printf("%s -> PALAVRA RESERVADA\n", lexemas[i]); break;
        case INT: printf("%s -> PALAVRA RESERVADA\n", lexemas[i]); break;
        case VOID: printf("%s -> PALAVRA RESERVADA\n", lexemas[i]); break;
        case WHILE: printf("%s -> PALAVRA RESERVADA\n", lexemas[i]); break;
        case RETURN: printf("%s -> PALAVRA RESERVADA\n", lexemas[i]); break;
        case ID: printf("%s -> IDENTIFICADOR\n", lexemas[i]); break;
        case COMMA: printf("%s -> VIRGULA\n", lexemas[i]); break;
        case SEMICOLON: printf("%s -> PONTO E VIRGULA\n", lexemas[i]); break;
        case NEW_LINE: printf("NOVA LINHA\n"); break;
        //case SPACE: printf("ESPACO\n"); break;
        case INVALID: printf("%s -> INVALIDO\n", lexemas[i]); break;
    }
    i++;
  }
  return(0);
}

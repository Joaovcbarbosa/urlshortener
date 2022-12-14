%{
#include <iostream>
using namespace std;
    extern "C"
    {
        int yyparse(void);
        int yylex(void);
        int yywrap(){
            return 1;
        }
    }
void yyerror(char *);
%}
%start entrada
%token VALOR FIMLIN
%left SOMA
%left MULT
%token ABRPAR FECPAR
%%

expr: expr SOMA expr {$$ = $1 + $3;}
    | expr MULT expr {$$ = $1 * $3;}
    | ABRPAR expr FECPAR {$$ = $2;}
    | VALOR
    ;

entrada: /* vazia */
       | entrada result
       ;

result: FIMLIN
      | expr FIMLIN
        { cout << "Resposta: " << $1 << end1;}
      | error FIMLIN { yyerrok;}
      ;

%%

void yyerror(char* msg){
    extern char* yytext;
    cout << msg << ": " << yytext << end1;
}
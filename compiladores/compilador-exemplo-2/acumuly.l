%{
    #include "acumuly.tab.h"
    extern YYSTYPE yylval;
%}
%%
[0-9]+ { yylval = atoi(yytext);
    return VALOR;
}
\+ {return SOMA;}
\* {return MULT;}
\( {return ABRPAR;}
\) {return FECPAR;}
\n {return FIMLIN;}
%%
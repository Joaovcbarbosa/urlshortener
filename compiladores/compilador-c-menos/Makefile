compiler:
	flex scanner.l
	bison -d parse.y && gcc -c lex.yy.c
	gcc AnalisadorSemantico.c Global.c lex.yy.o Main.c parse.tab.c TabelaSimbolos.c -o exe -lfl
	
remove:
	rm exe
	rm *.o
	rm *.tab.c
	rm *.tab.h
	rm *.yy.c
	rm arquivoPreProcessado.txt
	rm arquivoSaida.txt

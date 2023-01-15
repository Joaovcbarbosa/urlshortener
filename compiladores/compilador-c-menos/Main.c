#include "Global.h"
#include "PreProcessamento.c"

FILE *arquivoEntrada, *arquivoSaida;

int main(int argc, char** argv) {
    FILE *arquivoSaida = fopen("arquivoSaida.txt", "w");

	PreProcessamento(argv[1]);	
    AnaliseSintatica("arquivoPreProcessado.txt", arquivoSaida);
    TabelaDeSimbolos(arquivoSaida);
    AnaliseSemantica(arquivoSaida);

    return 0;
}

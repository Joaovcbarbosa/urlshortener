#include "Global.h"

static int tamanhoTabArvoreSintatica = 0;

void EscreveArquivo(FILE *arquivoSaida, char *str) {
    fprintf(arquivoSaida, "%s", str);
}

char *CopiarString(char *str) { 
    char *t = malloc(strlen(str) + 1);
    strcpy(t, str);    
    return t;
}

char *RecebeNomeToken(tipoToken t) {
    char *nome = (char*) malloc(sizeof(char) * TAMANHO_MAXIMO_TOKEN);

    switch(t) 
    {
        case ATRIBUICAO: strcpy(nome, "ATRIBUICAO"); break;
        case FECHA_COLCHETES: strcpy(nome, "FECHA_COLCHETES"); break;
        case FECHA_CHAVES: strcpy(nome, "FECHA_CHAVES"); break;
        case COMENT: strcpy(nome, "COMENT"); break;
        case VIRGULA: strcpy(nome, "VIRGULA"); break;
        case FECHA_PARENTESES: strcpy(nome, "FECHA_PARENTESES"); break;
        case DIFERENTE: strcpy(nome, "DIFERENTE"); break;
        case ELSE:  strcpy(nome, "ELSE"); break;
        case IGUAL: strcpy(nome, "IGUAL"); break;
        case MAIOR_QUE: strcpy(nome, "MAIOR_QUE"); break;
        case MAIOR_OU_IGUAL_QUE: strcpy(nome, "MAIOR_OU_IGUAL_QUE"); break;
        case ID: strcpy(nome, "ID"); break;
        case IF: strcpy(nome, "IF"); break;
        case INT: strcpy(nome, "INT"); break;
        case MENOR_QUE: strcpy(nome, "MENOR_QUE"); break;
        case MENOR_OU_IGUAL_QUE: strcpy(nome, "MENOR_OU_IGUAL_QUE"); break;
        case SUBTRACAO: strcpy(nome, "SUBTRACAO"); break;
        case novaLinha: strcpy(nome, "novaLinha"); break;
        case NUM: strcpy(nome, "NUM"); break;
        case ABRE_COLCHETES: strcpy(nome, "ABRE_COLCHETES"); break;
        case ABRE_CHAVES: strcpy(nome, "ABRE_CHAVES"); break;
        case ABRE_PARENTESES: strcpy(nome, "ABRE_PARENTESES"); break;
        case ADICAO: strcpy(nome, "ADICAO"); break;
        case RETURN: strcpy(nome, "RETURN"); break;
        case PONTO_E_VIRGULA: strcpy(nome, "PONTO_E_VIRGULA"); break;
        case DIVISAO: strcpy(nome, "DIVISAO"); break;
        case espaco: strcpy(nome, "espaco"); break;
        case MULTIPLICACAO: strcpy(nome, "MULTIPLICACAO"); break;
        case VOID: strcpy(nome, "VOID"); break;
        case WHILE: strcpy(nome, "WHILE"); break;
        default: strcpy(nome, "INVALIDO"); break;
    }
            
    return nome;
}

char *RecebeNomeTipo(TipoPrimitivo t) {
    switch(t)
    {
        case Integer: return "int"; break;
        case Void: return "void"; break;
        case Array: return "array"; break;
        default: return "bool"; break;
    }
}

void IniciaPilha(tipoPilha *stack) {
    stack = (tipoPilha*)malloc(sizeof(tipoPilha*));
    stack->top = NULL;
    stack->tamanho = 0;
}

void PushPilha(tipoPilha *stack, char* nome) {
    pilha *i = (pilha*) malloc(sizeof(pilha*));
    i->proximo = stack->top;
    i->nome = strdup(nome);
    stack->top = i;
    stack->tamanho++;
}

char *PopPilha(tipoPilha *stack) {
    pilha *old_top;
    char *nome = NULL;
    if(stack->tamanho == 0)
        return NULL;
    nome = strdup(stack->top->nome);
    old_top = stack->top;
    stack->top = old_top->proximo;
    free(old_top);    
    stack->tamanho--;
    return nome;
}

no *IniciaNo(TipoNo tipoNo) {
    no *node = (no*) malloc(sizeof(no));
    for(int i=0; i<TAMANHO_MAXIMO_NOS_FILHOS; i++)
        node->nosFilhos[i] = NULL;
    node->nosIrmaos = NULL;
    node->numeroLinha = numeroLinha;
    node->tipoNo = tipoNo;
}

no *CriaNoDeclaracao(TipoDeclaracao tipo) { 
    no *node = IniciaNo(noDeclaracao);    
    node->tipo.declaracao = tipo;
    return node;
}

no *CriaNoStatement(TipoStatement tipo) { 
    no *node = IniciaNo(noStatement);    
    node->tipo.declaracao = tipo;
    return node;
}

no *CriaNoExpressao(TipoExpressao tipo) { 
    no *node = IniciaNo(noExpressao);    
    node->tipo.declaracao = tipo;;
    return node;
}

void ImprimeArvoreSintatica(no *arvore, FILE *arquivoSaida) { 
    tamanhoTabArvoreSintatica += TAMANHO_TAB;
    while(arvore != NULL) 
    {
        for(int i=0; i<tamanhoTabArvoreSintatica; i++)
            EscreveArquivo(arquivoSaida, " ");
        if(arvore->tipoNo == noExpressao) 
        { 
            switch (arvore->tipo.expressao)
            {
                case expressaoID:
                    if(strcmp(arvore->valores.nome,"void") == 0) {
                        EscreveArquivo(arquivoSaida, "Void\n");
                    } 
					else {
                        sprintf(tokenString, "Id: %s\n",arvore->valores.nome);
                        EscreveArquivo(arquivoSaida, tokenString);
                    }
                    break;
                default:
                    EscreveArquivo(arquivoSaida, "Expressão inválida!\n");
                    break;
                case expressaoNumero:
                    sprintf(tokenString, "Num: %d\n", arvore->valores.valor);
                    EscreveArquivo(arquivoSaida, tokenString);
                    break;
                case expressaoOperacao:  
                    sprintf(tokenString, "Operador: %s\n", RecebeNomeToken(arvore->valores.simbolo));
                    EscreveArquivo(arquivoSaida, tokenString);
                    break;
            }
        }
        else if(arvore->tipoNo == noStatement) 
        { 
            switch (arvore->tipo.statement) 
            {
                case statementIf: EscreveArquivo(arquivoSaida, "If\n"); break;
                case statementWhile: EscreveArquivo(arquivoSaida, "While\n"); break;
                case statementAtribuicao: EscreveArquivo(arquivoSaida, "Atribuição\n"); break;
                case statementReturn: EscreveArquivo(arquivoSaida, "Retorno\n"); break;
                case statementChamada:
                    sprintf(tokenString, "Chamada de Função: %s\n", arvore->valores.nome);
                    EscreveArquivo(arquivoSaida, tokenString);
                    break;
                default: EscreveArquivo(arquivoSaida, "Statement inválido!\n"); break;
            }
        }
        else if (arvore->tipoNo == noDeclaracao) {
            switch(arvore->tipo.declaracao)
            {
                case declaracaoTipo:
                    if (arvore->tipoPrimitivo == Integer)
                        EscreveArquivo(arquivoSaida, "TipoPrimitivo int\n");
                    else if(arvore->tipoPrimitivo == Array) 
                        EscreveArquivo(arquivoSaida, "TipoPrimitivo int[]\n");
                    else
                        EscreveArquivo(arquivoSaida, "TipoPrimitivo void\n");
                    break;
                case declaracaoFuncao:
                    sprintf(tokenString, "Função: %s\n",arvore->valores.nome);
                    EscreveArquivo(arquivoSaida, tokenString);
                    break;
                case declaracaoVariavel:
                    sprintf(tokenString, "Variável: %s\n",arvore->valores.nome);
                    EscreveArquivo(arquivoSaida, tokenString);
                    break;         
                default:
                    EscreveArquivo(arquivoSaida, "Declaração inválida!\n");
                    break;
            } 
        } else 
            EscreveArquivo(arquivoSaida, "TipoPrimitivo desconhecido!\n");
        

        bzero(tokenString, TAMANHO_MAXIMO_TOKEN);

        for(int j=0; j<TAMANHO_MAXIMO_NOS_FILHOS; j++)
            ImprimeArvoreSintatica(arvore->nosFilhos[j], arquivoSaida);

        arvore = arvore->nosIrmaos;
    }

    tamanhoTabArvoreSintatica -= TAMANHO_TAB;
}

void AnaliseSintatica(char *nomeArquivoEntrada, FILE *arquivoSaida) {
    arquivoEntrada = fopen(nomeArquivoEntrada, "r");    
    arvoreSintatica = parse();
    if(!erro) {
        EscreveArquivo(arquivoSaida, "\n\nÁrvore Sintática:\n\n");
        ImprimeArvoreSintatica(arvoreSintatica, arquivoSaida);
    }
}

void TabelaDeSimbolos(FILE *arquivoSaida) {
    if(!erro) {
        EscreveArquivo(arquivoSaida, "\n\nTabela de Símbolos\n\n");
        IniciaTabelaDeSimbolos(arvoreSintatica, arquivoSaida);
    }
}

void AnaliseSemantica(FILE *arquivoSaida) {
    if(!erro) {
        VerificaTipoNo(arvoreSintatica, arquivoSaida);
    }
}


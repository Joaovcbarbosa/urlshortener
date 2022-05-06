#include <stdio.h>
#include <stdlib.h>

typedef struct no No;
struct no {
	int valor;
    int indice;
	No *proximo;
	No *anterior;
};

No *inicio;
No *fim;
int tamanho;

void iniciar() {
	inicio = NULL;
	fim = NULL;
	tamanho = 0;
}

No *alocarMemoria(int valor, int indice) {
	No *novo = (No*)malloc(sizeof(No));
	novo->valor = valor;
    novo->indice  = indice;
	novo->anterior = NULL;
	novo->proximo = NULL;
	return novo;
}

void remover(int indice) {

	No *atual;
	atual = inicio;
    int aux = 0;
	while(aux == 0){
		if(atual->indice != indice)
		    atual=atual->proximo;
        else aux = 1;
	}

    atual->anterior->proximo = atual->proximo;
	tamanho--;

}


void inserir(int valor, int indice) {
	No *novo = alocarMemoria(valor, indice);   

	if(inicio==NULL){
		inicio=novo;		
	}else{
		No *atual; 
		atual = fim;
		novo->anterior = atual;
		atual->proximo = novo;		
	}
    fim=novo;	
	tamanho++;
}

void imprimir() {
	No *atual;
	atual = inicio;
	while(atual){		
        printf("%d ",atual->valor);
		atual=atual->proximo;
	}
}

int main() {
	iniciar();
	int i;
	for(i=0 ;i<5 ; i++){
		inserir(i+5, i);
	}
	imprimir();
    printf("\n");
    remover(1);
    imprimir();
}

/*
Vitor Galioti Martini
135543
Problema 2
Intercalação de vetores
 
*/
#include<stdio.h>
#include<stdlib.h>

//Estrutura que guarda o valor e de que qual vetor ele veio
typedef struct no No;
struct no {
    int valor;
    int indice;
};

//Heap com o vetor dos elementos
struct Heap{
    int quantidadeOcupada;
    No *vetor;
};
typedef struct Heap Heap;

//Reconstroi o heap de baixo para cima
void heapifyBaixoCima(Heap *heap, int indiceMenor){
    int esquerda, direita, menor;
    No aux;
    esquerda = indiceMenor * 2 + 1;
    direita = indiceMenor * 2 + 2;
 
    if(esquerda < 0 || esquerda >= heap-> quantidadeOcupada) esquerda = -1;
    if( direita < 0 || direita >= heap-> quantidadeOcupada) direita = -1;   
    if(esquerda != -1 && heap->vetor[esquerda].valor < heap->vetor[indiceMenor].valor) menor = esquerda;
    else menor = indiceMenor;
    if(direita != -1 && heap->vetor[direita].valor < heap->vetor[menor].valor) menor = direita;
    
    if(menor != indiceMenor){ 
        aux = heap->vetor[menor];
        heap->vetor[menor] = heap->vetor[indiceMenor];
        heap->vetor[indiceMenor] = aux;
 
        heapifyBaixoCima(heap, menor);
    }
}

//Reconstroi o heap de cima para baixo
void heapifyCimaBaixo(Heap *heap, int indice){
    No aux;
    int indiceMenor = (indice - 1) / 2;

    if(heap->vetor[indiceMenor].valor > heap->vetor[indice].valor){
        aux = heap->vetor[indiceMenor];
        heap->vetor[indiceMenor] = heap->vetor[indice];
        heap->vetor[indice] = aux;
        heapifyCimaBaixo(heap,indiceMenor);
    }
}

//Insere o elemento e reconstroi o heap de cima para baixo
void inserir(Heap *heap, int valor, int indice){    
    heap->vetor[heap->quantidadeOcupada].valor = valor;
    heap->vetor[heap->quantidadeOcupada].indice = indice;
    heapifyCimaBaixo(heap, heap->quantidadeOcupada);
    heap->quantidadeOcupada++;
}

//Inicia o heap
Heap *iniciar(int quantidadeMaxima){
    Heap *heap = (Heap * ) malloc(sizeof(Heap));
    heap->quantidadeOcupada = 0;
    heap->vetor = (No *) malloc(quantidadeMaxima*sizeof(No)); 

    return heap;
}

int main(){

    int k, iteracoes, i, j, n, qtdElementos = 0;
    unsigned long long resultado = 0;

    //Recebe entradas do usuário
    scanf("%d %d", &k, &iteracoes);
 
    //Cria os K vetores e os vetores auxiliares
    int **vetor = (int**)malloc(sizeof(int*) * k);
    int vetorIndices[k]; 
    int nVetores[k]; 
 
    for(i = 0; i < k; i++){

        scanf("%d", &n);
        
        vetor[i] = (int*)calloc(n, sizeof(int));
 
        for(j = 0; j < n; j++)
            scanf("%d", &vetor[i][j]);
            
        vetorIndices[i] = 0; //Vetor que verifica quais indices ja foram somados
        nVetores[i] = n; //Vetor que guarda a quantidade de elementos de cada posição do vetor principal
        qtdElementos += n;
    }      

    //Inicia o Heap
    Heap *heap = iniciar(qtdElementos);
  
    for(i = 0; i < k; i++)
        for(j = 0; j < nVetores[i]; j++)
             inserir(heap, vetor[i][j], i);    //Cria o heap intercalando os vetores
    
    iteracoes = iteracoes - 1;
    j = 0;

    //Percorre os elementos
    for(i = 0; i < qtdElementos; i++){
        //Caso chegamos no iesimo elemento
        if(i >= iteracoes){
            //Caso o índice dele ainda não foi contado
            if(vetorIndices[heap->vetor[0].indice] == 0){
                resultado += heap->vetor[0].valor;
                vetorIndices[heap->vetor[0].indice] = 1;  
                j++;              
            }         
        }

        //Caso já foi percorrido todos os índices, encerra o laço
        if(j == k) 
            i = qtdElementos;

        //Remove o valor e recalcula heap
        heap->quantidadeOcupada--;
        heap->vetor[0].valor = heap->vetor[heap->quantidadeOcupada].valor;        
        heap->vetor[0].indice = heap->vetor[heap->quantidadeOcupada].indice;        
        heapifyBaixoCima(heap, 0);    
    }
       
    printf("%llu", resultado);
}
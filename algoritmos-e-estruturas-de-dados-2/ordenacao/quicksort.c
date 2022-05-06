#include <stdio.h>
#include <stdlib.h>
/**<
Vitor Galioti Martini
RA: 135543
AED II Noturno - Regina
Judge 01 para 21/02
Ordena��o Interna - QuickSort
 */
 
//Procedimento para particionar o vetor
int particionar(int *vetor, int inicio, int fim)
{
    //Define vari�veis locais
    int pivo, aux, i, j;
 
    //i recebe 1 - inicio, e j recebe o pr�prio in�cio
    i = inicio - 1;
    j = inicio;
    //pivo recebe o �ltimo elemento (regra adotada)
    pivo = vetor[fim];
 
    //enquanto j, que ser� a vari�vel que analisar� cada elemento do vetor, for menor que o fim
    while(j < fim)
    {
        //se a vari�vel no indice j for menor que o pivo adotado
        if(vetor[j] <= pivo)
        {
            //se o i+1 != j, quer dizer que h� um elemento maior que o pivo entre i e j
            if(i+1 != j)
            {
                //troca a posi��o do elemento i+1 e j
                aux = vetor[i+1];
                vetor[i+1] = vetor[j];
                vetor[j] = aux;
            }
            i++;
        }
        j++;
    }
 
    //troca a posicao do i+1 com a posicao final (piv�)
    aux = vetor[i+1];
    vetor[i+1] = vetor[fim];
    vetor[fim] = aux;
 
    //retorna a posi��o do piv�
    return i+1;
}
 
 
//Procedimento para organizar o vetor em ordem crescente
void ordenar(int *vetor, int inicio, int fim, int qtdElementos)
{
    int pivo, i;
    if(inicio < fim)
    {
        //Chama o procedimento de particionar o vetor
        pivo = particionar(vetor, inicio, fim);
 
        //Printa saida
        for(i = 0; i < qtdElementos; i++)
            printf("%d ", vetor[i]);
        printf("\n");
 
        //Chama o procedimento de ordenar para o primeiro vetor
        ordenar(vetor, inicio, pivo-1, qtdElementos);
 
        //Chama o procedimento de ordenar para o segundo vetor
        ordenar(vetor, pivo+1, fim, qtdElementos);
    }
}
 
int main()
{
    //Recebe as entradas
    int qtdElementos, i;
    scanf("%d", &qtdElementos);
 
    //Cria o vetor
    int vetor[qtdElementos];
 
    //Recebe valor do vetor
    for(i = 0; i < qtdElementos; i++)
        scanf("%d", &vetor[i]);
 
    //Chama o procedimento de ordenar o vetor (QuickSort)
    ordenar(vetor, 0, qtdElementos-1, qtdElementos);
}
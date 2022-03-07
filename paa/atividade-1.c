#include <stdio.h>
#include <stdlib.h>

/*
Vitor Galioti Martini
135543
*/

//Calcula a média arredondando o valor sempre para cima
int CalcularTetoMedia(float soma){

    float media = soma / 30.0;
    int retorno;

    if(fmod(media, 1) != 0.0)
        retorno = media + 1;
    else
        retorno = media;

    return retorno;
}

//Conta os dias
int ContarDias(int qtdInicial, int qtdMeta, float soma, int *dias){

    //Variáveis locais
    int i, j, retorno, media;
    i = 0;
    j = 0;
    media = 0;
    retorno = 0;

    //Enquanto a meta não foi batida
    while(qtdInicial < qtdMeta){
        media = CalcularTetoMedia(soma); //Calcula a média
        soma -= dias[i];  //Substrai o valor do dia atual na suma
        soma += media; //Soma o valor obtido na soma total
        dias[i] = media; // Define que o dia atual tem o valor encontrado
        qtdInicial += dias[i]; //Soma o valor na quantidade
        
        //Incrementa contadores
        retorno++; 
        i++;
        if(i == 30) //Caso chegou no final do vetor, volta para o início
            i = 0;
            
    }
    return retorno;
}

int main()
{
    // Variáveis locais
    int qtdInicial, qtdMeta, dias[30], i;
    float soma = 0.0;

    // Recebe os valores
    scanf("%d", &qtdInicial);
    scanf("%d", &qtdMeta);

    //Monta o vetor
    for(i = 0; i < 30; i++){
        scanf("%d", &dias[i]);
        soma += dias[i];
    }
    
    printf("%i", ContarDias(qtdInicial, qtdMeta, soma, dias));
}


# Vitor Galioti Martini
# 135543     

def blockChain(N, C, r, s):
    # A lógica implementada é semelhante a demonstrada no exercício 2 da lista 3    

    # Inicia a tabela
    A = [[0 for x in range(C + 1)] for y in range(N + 1)]
 
    for i in range(N + 1):
        for x in range(C + 1):
            if i == 0 or x == 0: # Caso base
                A[i][x] = 0
            elif x < s[i-1]: # Caso a capacidade do bloco seja menor que o tamanho da n-ésima transação
                A[i][x] = A[i-1][x]
            else:
                A[i][x] = max(A[i-1][x], r[i-1] + A[i-1][x-s[i-1]])  # Retorna o máximo entre as duas opções: a n-ésima transação está inclusa, ou não está inclusa 
   
    print(A[N][C]) 
 
def entrada():
       
       # Recebe a entrada
        entrada = list(map(int, input().split()))
        
        N = entrada[0]
        C = entrada[1]
        r = [0 for i in range(N)]
        s = [0 for i in range(N)]

        # Preenche os vetores r (taxa) e s (tamanho)
        for i in range(N):
                entrada = list(map(int, input().split()))
                r[i] = entrada[0]
                s[i] = entrada[1]

        blockChain(N, C, r, s)            

entrada()
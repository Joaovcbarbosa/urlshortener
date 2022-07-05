import sys 

result = []
tabela = []
melhores = []
parar = False 

def gerar_resultado(a, n):
    global parar 
    result.clear()
    b = []
    valor = 1
    i = 0
    while i < n:   
        b.append(a[i])
        valor = valor * tabela[a[i]][a[0 if i == n-1 else i+1]]
        i += 1

    b.append(a[0])

    if valor > 1:
        melhores.append([b, valor])
        parar = True
        

def swap(lista, i, j):
    aux = lista[i]
    lista[i] = lista[j]
    lista[j] = aux 

def permutacao(a, n, tamanho):
    if (tamanho == 1):
        gerar_resultado(a, n)
        return
    
    for i in range(tamanho):
        permutacao(a, n, tamanho-1)
        swap(a, 0 if tamanho%2 == 1 else i, tamanho-1)
    
def K_permutacao(a, n, k, tamanho):
    if (tamanho == n - k + 1):
        gerar_resultado(a + n - k, k)
        return

    for i in range(tamanho):
        K_permutacao(a, n, k, tamanho-1)
        swap(a, 0 if tamanho%2 == 1 else i, tamanho-1)
    
def combinacao(a, n, p, k, tamanho, inicio):
    escolhido = [0] * (tamanho + 1)
    for i in range(tamanho): escolhido[i] = p[i]
    if (tamanho == k):
        permutacao(p, k, k)
    else:
        if (inicio < n):
            combinacao(a, n, escolhido, k, tamanho, inicio + 1)
            escolhido[tamanho] = a[inicio]
            combinacao(a, n, escolhido, k, tamanho + 1, inicio + 1)

def gerar_tabela(n):
    tabela = []

    for i in range(n):         
        linha = []
        j = 0
        flag = 0
        valores = input().split(' ')

        while j < n:
            if i == j:
                linha.append(1)
                flag = 1
            else:
                linha.append(float(valores[j-flag]))
            
            j += 1

        tabela.append(linha)  

    return tabela  
    

def main():
    sys.setrecursionlimit(1000000)
    n = int(input())
    lista = [i for i in range(n)]
    
    global tabela, parar, melhores
    tabela = gerar_tabela(n)
    
    i = 2
    while i <= n:        
        combinacao(lista, n, [], i, 0, 0)
        if parar:
            i = n
            print(melhores)
        i += 1
 
main()

    
import sys 

resultado = []
melhor_valor = -1

def permutacao(vertices, prefixo, n, tamanho, tabela):
    global resultado, melhor_valor
    if (tamanho == 1):
        for j in range(n):
            caminho = str(prefixo) + str(vertices[j])   
            valor = 1

            i = 0
            while i < len(caminho):   
                valor = valor * tabela[int(caminho[i])][int(caminho[0 if i == len(caminho)-1 else i+1])]
                i += 1
            
            if valor > 1 and valor > melhor_valor:
                melhor_valor = valor
                resultado = caminho + caminho[0]    
    else:
        for i in range(n):
            if melhor_valor != -1:
                return
            vertices2 = vertices.copy()
            del vertices2[i]
            permutacao(vertices2, str(prefixo) + str(vertices[i]),  len(vertices2), tamanho - 1, tabela)

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
    vertices = [i for i in range(n)]
    tabela = gerar_tabela(n)

    i = 2
    while i < n:
        permutacao(vertices, "", len(vertices), i, tabela)
        
        if melhor_valor != -1:
            for j in range(len(resultado)):
                print(str(int(resultado[j])+1) + (' ' if j != len(resultado) - 1 else ''), end = '')
            return

        i+=1

    print('impossible')

main()
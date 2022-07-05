from itertools import permutations

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
    n = int(input())
    tabela = gerar_tabela(n)
    p = [0, 1, 2]

    i = 2
    while i <= n:
        l = list(permutations(p, i))
        print(l)
        i += 1


 
main()
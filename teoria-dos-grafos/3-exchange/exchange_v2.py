from copy import deepcopy

tabelas = []

def floyd_warshall(d, n):
  global tabelas 

  for k in range(n):
    for i in range(n):
      for j in range(n):
        d[i][j] = max(d[i][j], d[i][k] * d[k][j])
    tabelas.append(deepcopy(d))
    print_solution(d, n)
  print_tabelas()

def print_tabelas():
  global tabelas

  for tabela in tabelas:
    for linha in tabela:
      print(linha)
    print()

def print_solution(d, n):
  print ("Following matrix shows the shortest distances\
between every pair of vertices")
  for i in range(n):
    for j in range(n):
      print((d[i][j]),end=' ')
      if j == n-1:
        print ()

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
    # n = int(input())
    # d = gerar_tabela(n) 
    
    n = 3
    d = [[1,1.2,0.89],[0.88,1,5.1],[1.1,0.15,1]]
    
    # n = 6
    # d = [
    # [1, 0.0,0.0,0.0,0.0,0.0],
    # [0.0,1,0.0,0.1,0.0,0.0],
    # [0.0,0.0,1,1.0,0.0,0.0],
    # [0.0,5.0,0.0,1,0.0,0.0],
    # [0.0,0.0,0.0,0.0,1,9.0],
    # [0.0,0.0,0.0,0.0,1.0,1]
    # ]

    floyd_warshall(d, n)

main()




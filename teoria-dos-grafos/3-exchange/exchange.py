# https://www.youtube.com/watch?v=8zOqt7uyOwI
tabela_inicial = []

def dist(d, i, j, k):
  global tabela_inicial
  if k == 0:
    return tabela_inicial[i][j]  
  return min(d[i][j][k-1], d[i][k][k-1] + d[k][j][k-1])

def floydWarshall(d, n):

  for k in range(n):
    for i in range(n):
      for j in range(n):
        if i == 2 and j == 1:
          print('')
        d[i][j][k] = dist(d, i, j, k)
  print(d)
  printSolution(d, n)

def printSolution(d, n):
  
  for i in range(n):
    for j in range(n):
      print ((d[i][j][n-1]),end=' ')
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
    global tabela_inicial 
    # n = int(input())
    # tabela_inicial = gerar_tabela(n)
    # tabela_inicial = [[0, 3, 4, 9999],[9999, 0, 9999, 5],[9999, 9999, 0 , 3],[8, 9999, 9999, 0]]
    
    n = 4
    tabela_inicial = [[0, 3, 9999, 7],[8, 0, 2, 9999],[5, 9999, 0 , 1],[2, 9999, 9999, 0]]
    d = [[[0 for k in range(n)] for j in range(n)] for i in range(n)]
    
    floydWarshall(d, n)

main()

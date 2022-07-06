# Python Program for Floyd Warshall Algorithm

# Number of vertices in the graph

V = 0
def floydWarshall(dist):

  print(dist)

  for k in range(V):
    for i in range(V):
      for j in range(V):
        dist[i][j] = min(dist[i][j],
                dist[i][k] + dist[k][j]
                )
  printSolution(dist)

def printSolution(dist):
  print ("Following matrix shows the shortest distances\
between every pair of vertices")
  for i in range(V):
    for j in range(V):
      print ((dist[i][j]),end=' ')
      if j == V-1:
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
    global V
    n = int(input())
    V = n
    dist = gerar_tabela(n)
    floydWarshall(dist)

main()

def floyd_warshall(d, tabela, transacoes, n):
  for t in range(1, n):
    for i in range(n):
      for j in range(n):
        for k in range(n):
          valor_antigo = d[t][i][j]
          valor_novo = d[t-1][i][k] * tabela[k][j]
          if valor_novo > valor_antigo:
            d[t][i][j] = valor_novo
            if i == j:
              if transacoes[i][-1] != k and valor_antigo != -1:
                transacoes[i].append(k)
              if valor_novo > 1:
                transacoes[i].append(transacoes[i][0])
                return transacoes[i]
 
  return False 
 
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
    # tabela = gerar_tabela(n) 
 
    # n = 3
    # tabela = [[1,1.2,0.89],[0.88,1,5.1],[1.1,0.15,1]]
    
    # n = 6
    # tabela = [[1,0.0,0.0,0.0,0.0,0.0],
    # [0.0,1,0.0,0.1,0.0,0.0],
    # [0.0,0.0,1,1.0,0.0,0.0],
    # [0.0,5.0,0.0,1,0.0,0.0],
    # [0.0,0.0,0.0,0.0,1,9.0],
    # [0.0,0.0,0.0,0.0,1.0,1]]
    
    n = 4
    tabela = [[1, 0.1, 2, 0.1],
              [5, 1, 0.1, 0.1],
              [0.1, 0.1, 1, 3],
              [0.1, 4, 0.1, 1]]
 
    d = [[[-1 for j in range(n)] for j in range(n)] for i in range(n)]
    d[0] = tabela
 
    transacoes = [[i] for i in range(n)]
    resultado = floyd_warshall(d, tabela, transacoes, n)
    if resultado == False:
      print('Impossible')
    else:
      for j in range(len(resultado)):
        print(resultado[j]+1, end = ' ')
 
 
main()
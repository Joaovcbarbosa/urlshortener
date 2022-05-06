#Vitor Galioti Martini
#135543

#Função crossover
def crossover():
    #Recebe os parametros
    n = int(input())
    linha = input()
    y = int(linha[0])
    p = float(linha[2:len(linha)])
    individuo_1 = input()
    individuo_2 = input()
    individuo_3 = input()
    
    #Gera os dois individuos filhos
    individuo_4 = individuo_1[0:y] + individuo_2[y:len(individuo_2)]
    individuo_5 = individuo_2[0:y] + individuo_1[y:len(individuo_1)]

    #Faz os cálculos da probabilidade
    probabilidade1 = probabilidade(n, p, individuo_4, individuo_3)
    probabilidade2 = probabilidade(n, p, individuo_5, individuo_3)
    probabilidade_final = 1 - ((1 - probabilidade1) * (1 - probabilidade2)) 
    
    #Retorno da função
    return "{:.7f}".format(probabilidade_final)

#Função probabilidade
def probabilidade(n, p, individuo_crossover, individuo_objetivo):
    probabilidade = 1.0000000
    #Calcula a probabilidade bit a bit
    for i in range(n):
        if individuo_crossover[i] == individuo_objetivo[i]:
            probabilidade = probabilidade * (1 - p)
        else:
            probabilidade = probabilidade * p

    return probabilidade

#main
t = int(input())
respostas = []

#enquanto há entradas, executa o crossover
while t > 0:
    respostas.append(crossover())
    t -= 1

#printa a resposta
for resposta in respostas:
    print(resposta)
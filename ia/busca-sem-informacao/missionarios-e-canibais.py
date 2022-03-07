# Vitor Galioti Martini - 135543

class Estado:

    # Função construtora
    def __init__(self, canibais, missionarios, pai, somar):
        self.canibais = canibais  # qtd de canibais na margem esquerda
        self.missionarios = missionarios  # qtd de missionarios na margem esquerda
        self.pai = pai  # recebe o estado pai, isto é, o estado que gerou o atual
        self.somar = somar  # variável booleana que indica se no próximo caminho devemos somar ou subtrair canibais/missonários

    # Função que verifica se chegou ao fim
    def fim(self):
        # O fim é quando não existem nem canibais nem missionários do lado esquerdo do rio
        if (self.canibais == 0) and (self.missionarios == 0):
            return True
        else:
            return False

    # Função que valida as operações, devem existir um total de 3 missionários e 3 canibais e nunca a quantidade de
    # canibais em uma margem pode ser maior que a de missionários
    def validacao(self):

        if self.canibais < 0 or self.missionarios < 0 or self.canibais > 3 or self.missionarios > 3:
            return False

        if (self.canibais <= self.missionarios or self.missionarios == 0) and (
                abs(self.canibais - 3) <= abs(self.missionarios - 3) or self.missionarios == 3):
            return True
        else:
            return False


# Define quais são os próximos estados, a partir do atual
def proximos_estados(estado_atual):
    proximos_estados = []

    # Caso o estado atual seja somar = false, vamos substrair pessoas da margem esquerda
    if estado_atual.somar == False:
        # 1 canibal da esquerda para direita
        novo_estado = Estado(estado_atual.canibais - 1, estado_atual.missionarios, estado_atual, True)
        if novo_estado.validacao():
            proximos_estados.append(novo_estado)

        # 2 canibais da esquerda para direita
        novo_estado = Estado(estado_atual.canibais - 2, estado_atual.missionarios, estado_atual, True)
        if novo_estado.validacao():
            proximos_estados.append(novo_estado)

        # 1 missionario da esquerda para direita
        novo_estado = Estado(estado_atual.canibais, estado_atual.missionarios - 1, estado_atual, True)
        if novo_estado.validacao():
            proximos_estados.append(novo_estado)

        # 2 missionarios da esquerda para direita
        novo_estado = Estado(estado_atual.canibais, estado_atual.missionarios - 2, estado_atual, True)
        if novo_estado.validacao():
            proximos_estados.append(novo_estado)

        # 1 missionario e 1 canibal da esquerda para direita
        novo_estado = Estado(estado_atual.canibais - 1, estado_atual.missionarios - 1, estado_atual, True)
        if novo_estado.validacao():
            proximos_estados.append(novo_estado)

    # Caso contrário vamos somar:
    else:
        # 1 canibal da direita para esquerda
        novo_estado = Estado(estado_atual.canibais + 1, estado_atual.missionarios, estado_atual, False)
        if novo_estado.validacao():
            proximos_estados.append(novo_estado)

        # 2 canibais da direita para esquerda
        novo_estado = Estado(estado_atual.canibais + 2, estado_atual.missionarios, estado_atual, False)
        if novo_estado.validacao():
            proximos_estados.append(novo_estado)

        # 1 missionario da direita para esquerda
        novo_estado = Estado(estado_atual.canibais, estado_atual.missionarios + 1, estado_atual, False)
        if novo_estado.validacao():
            proximos_estados.append(novo_estado)

        # 2 canibais da direita para esquerda
        novo_estado = Estado(estado_atual.canibais, estado_atual.missionarios + 2, estado_atual, False)
        if novo_estado.validacao():
            proximos_estados.append(novo_estado)

        # 1 missionario e 1 canibal da direita para esquerda
        novo_estado = Estado(estado_atual.canibais + 1, estado_atual.missionarios + 1, estado_atual, False)
        if novo_estado.validacao():
            proximos_estados.append(novo_estado)

    return proximos_estados


# Mostra o percurso feito:
def print_percurso(estado_atual):
    percurso = []

    # Enquanto o estado atual (que é o último) tiver pai:
    while estado_atual.pai != None:
        # Adiciona na lista de caminhos a string que representa o caminho:
        percurso.append('Esquerda: ' + str(estado_atual.canibais) + ' canibais e ' + str(estado_atual.missionarios) + ' missionários / '
                        'Direita: ' + str(abs(estado_atual.canibais - 3)) + ' canibais e ' + str(abs(estado_atual.missionarios - 3)) + ' missionários')

        # Vai para o próximo estado
        estado_atual = estado_atual.pai

    # Adiciona o estado inicial, que não tem estado pai
    percurso.append('Esquerda: ' + str(estado_atual.canibais) + ' canibais e ' + str(estado_atual.missionarios) + ' missionários / '
                    'Direita: ' + str(abs(estado_atual.canibais - 3)) + ' canibais e ' + str(abs(estado_atual.missionarios - 3)) + ' missionários')

    # Printa o percurso do estado inicial ao final:
    i = len(percurso) - 1
    while i >= 0:
        print(percurso[i])
        i -= 1

# Busca em profundidade
def busca_profundidade():

    #Define variáveis
    estados = []
    estados.append(Estado(3, 3, None, False))
    explorados = []

    # Enquanto houve estados
    while estados:

        # Tira da fila
        estado = estados.pop(0)

        # Verifica se o estado é o estado final
        if estado.fim():
            return estado

        # Se não, adiciona o estado na lista de já explorados
        explorados.append(estado)
        # Gera os estados filhos do atual
        proximos = proximos_estados(estado)

        # Para cada estado gerado, adiciona na fila caso ainda não foi explorado
        for p in proximos:
            if p not in explorados:
                estados.append(p)


# Inicia a busca pelo estado final e printa o percurso encontrado:
estado = busca_profundidade()
print_percurso(estado)

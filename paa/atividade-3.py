# Vitor Galioti Martini
# 135543
 
# 0 -> casa não ocupada
# 1  -> peão
# 2  -> cavalo
resultado = []
 
def iniciar_tabuleiro():
        
        tabuleiro = [0 for i in range(64)]
        posicoes_peoes = []
 
        # Recebe as entradas 
        entrada = list(map(int, input().split()))
 
        # Popula o tabuleiro com as peças
        for i in range(entrada[0] + 1):
                posicao = entrada[1+i] - 1
                
                if i == entrada[0]:
                        peca = 2
                        posicao_cavalo = posicao
                else:
                        peca = 1
                        posicoes_peoes.append(posicao)
 
                tabuleiro[posicao] = peca
 
        return tabuleiro, posicoes_peoes, posicao_cavalo
 
def print_tabuleiro(tabuleiro):
        print("")
        for i in range(64):
                print(str(tabuleiro[i]) + " ", end = '')
                if (i+1) % 8 == 0:
                        print("")
                        
def movimentos_cavalo(posicao_cavalo):
 
        cavalo_candidatos_movimento = []
 
        # Identificadores das colunas
        primeira_coluna = [0, 8, 16, 24, 32, 40, 48, 56]
        segunda_coluna = [1, 9, 17, 25, 33, 41, 49, 57]
        ultima_coluna = [7, 15, 23, 31, 39, 47, 55, 63]
        peultima_coluna = [6, 14, 22, 30, 38, 46, 54, 62]
 
        # Verifica quais movimentos o cavalo pode fazer a partir da posição atual dele
        if posicao_cavalo > 9 and posicao_cavalo < 64 and posicao_cavalo not in primeira_coluna and posicao_cavalo not in segunda_coluna:
                cavalo_candidatos_movimento.append(posicao_cavalo - 10)
 
        if posicao_cavalo < 55 and posicao_cavalo >= 0 and posicao_cavalo not in ultima_coluna and posicao_cavalo not in peultima_coluna:
                cavalo_candidatos_movimento.append(posicao_cavalo + 10)
 
        if posicao_cavalo < 62 and posicao_cavalo > 7 and posicao_cavalo not in ultima_coluna and posicao_cavalo not in peultima_coluna:
                cavalo_candidatos_movimento.append(posicao_cavalo - 6)
 
        if posicao_cavalo < 56 and posicao_cavalo >= 0 and posicao_cavalo not in primeira_coluna and posicao_cavalo not in segunda_coluna:
                cavalo_candidatos_movimento.append(posicao_cavalo + 6)
 
        if posicao_cavalo < 64 and posicao_cavalo > 14 and posicao_cavalo not in primeira_coluna: 
                cavalo_candidatos_movimento.append(posicao_cavalo - 17)
 
        if posicao_cavalo < 47 and posicao_cavalo >= 0 and posicao_cavalo not in ultima_coluna:
                cavalo_candidatos_movimento.append(posicao_cavalo + 17)
 
        if posicao_cavalo < 64 and posicao_cavalo > 14 and posicao_cavalo not in ultima_coluna:
                cavalo_candidatos_movimento.append(posicao_cavalo - 15)
                        
        if posicao_cavalo < 48 and posicao_cavalo > 0 and posicao_cavalo not in primeira_coluna:
                cavalo_candidatos_movimento.append(posicao_cavalo + 15)
 
        return cavalo_candidatos_movimento
                                        
def fazer_jogada(tabuleiro, posicoes_peoes, posicao_cavalo, candidato_movimento_cavalo):
 
        # A casa atual do cavalo passa a ser desocupada
        tabuleiro[posicao_cavalo] = 0
 
        # Verifica se ele capturou um peão
        if tabuleiro[candidato_movimento_cavalo] == 1:
                posicoes_peoes.remove(candidato_movimento_cavalo)
 
        # Move o cavalo para a nova posição
        tabuleiro[candidato_movimento_cavalo] = 2
 
        # Percorre cada peão
        for i in range(len(posicoes_peoes)):
                # Condições de parada: 
                # - Peão passou da ultima linha
                # - Peão vai capturar o cavalo
                # - Peão vai para a última linha e o cavalo está mais de duas linhas atrás, ou seja, será impossível captura-lo antes dele vencer o jogo
                if posicoes_peoes[i] + 8 > 63 or tabuleiro[candidato_movimento_cavalo] == posicoes_peoes[i] or (posicoes_peoes[i] + 8 > 55 and candidato_movimento_cavalo < 40):
                        return -1
 
                # Movimenta os peões
                tabuleiro[posicoes_peoes[i]] = 0
                tabuleiro[posicoes_peoes[i] + 8] = 1
                posicoes_peoes[i] = posicoes_peoes[i] + 8
 
        # Retorna a posição do cavalo
        return candidato_movimento_cavalo
                                                
def backtraking(k, tabuleiro, posicoes_peoes, posicao_cavalo):
 
        k += 1
        candidato_movimento_cavalo = movimentos_cavalo(posicao_cavalo)
 
        # Para cada possível movimento do cavalo
        for i in range(len(candidato_movimento_cavalo)):      
 
                # Gera cópia do estado atual                          
                tabuleiro_aux = tabuleiro.copy()
                posicoes_peoes_aux = posicoes_peoes.copy()
 
                # Faz a jogada
                nova_posicao_cavalo = fazer_jogada(tabuleiro_aux, posicoes_peoes_aux, posicao_cavalo, candidato_movimento_cavalo[i])       
 
                # Caso depois da jogada acabaram-se os peões, então chegou em uma solução                 
                if len(posicoes_peoes_aux) == 0:
 
                        # Guarda sempre a solução que necessita de menos jogadas
                        if len(resultado) > 0:
                                if resultado[0] > k:
                                        resultado[0] = k
                        else:
                                resultado.append(k)
 
                        return None
 
                # Caso a posição atual do cavalo seja válida, continua a jogada.
                # Caso seja inválida (-1) então o jogo acabou de alguma forma e o cavalo perdeu, então não chama a recursão
                if nova_posicao_cavalo != -1:
                        backtraking(k, tabuleiro_aux, posicoes_peoes_aux, nova_posicao_cavalo)
 
                               
def jogar():
        k = 0
        tabuleiro, posicoes_peoes, posicao_cavalo = iniciar_tabuleiro()   
        backtraking(k, tabuleiro, posicoes_peoes, posicao_cavalo)
 
        # Saída
        if len(resultado) == 0:
                print("impossible")
        else:
                print(min(resultado))
 
jogar()
from Metodos import metodos as met
import numpy as np
import random as rd


""" ------------- FUNÇÕES AUXILIARES ------------- """


"""
Descrição: Função responsável por atualizar a matriz de incidência ponderada com os novos valores dos arcos.
Entrada: Dicionário com as informações da rede; Matriz de incidência ponderada.
Saída: Indiretamente a matriz atualizada.
"""
def atualizaMatriz(rssf, matriz):
    #Percorrendo os sensores da rede.
    for i in range(1, rssf["tam"] + 1):
        #Percorrendo os vizinhos desse sensor.
        for vizinho in rssf[i].vizinhos:
            #Se o vizinho não for a estação rádio-base, atualiza o valor da aresta.
            if vizinho != "ERB":
                matriz[i][vizinho] = rssf[i].vizinhos[vizinho] + (((2500 - rssf[i].bateriaViz[vizinho]) / 25) * 1000)

"""
Descrição: Função que simula o envio de uma mensagem de um sensor até a estação rádio-base. Quando um sensor recebe uma mensagem ele reenvia ela.
Entrada: Dicionário com as informações da rede; Sensores que irão enviar a mensagem.
Saída: Lista com todos os sensores que conseguiram enviar a mensagem.
"""
def enviaMensagem(rssf, sensores):
    mensagem = [] # Lista com os sensores que enviaram a mensagem

    """ Iniciando o processo de envio das mensagens. """
    #Percorrendo os sensores que irão enviar as mensagens.
    for sensor in sensores:
        i = 0 #Indice do elemento atual na lista do menor caminho.
        #Percorrendo os sensores que estão no menor caminho.
        for caminho in rssf[sensor].menorCaminho:
            #Um elemento só poderá receber ou enviar uma mensagem se ele tiver sua bateria maior que 0 e for diferente da estação rádio-base (0)
            if caminho != 0 and rssf[caminho].bateria > 0:
                #Se o elemento atual do caminho for diferente do elemento inicial, então ele também gasta bateria para receber.
                if caminho != sensor:
                    rssf[caminho].bateria = rssf[caminho].bateria - 0.00164
                else:
                    #Elemento teve sucesso no envio da mensagem
                    mensagem.append(sensor)
                #Verificando para quem o sensor vai enviar a mensagem.
                if rssf[sensor].menorCaminho[i + 1] == 0:
                    #Enviando para a ERB.
                    rssf[caminho].bateria = rssf[caminho].bateria - (0.025 * (0.1 + (0.0001 * rssf[caminho].vizinhos["ERB"])))
                else:
                    #Enviando para o próximo sensor do menor caminho.
                    dist = rssf[caminho].vizinhos[rssf[sensor].menorCaminho[i + 1]] #Pegando a distância do sensor atual até o próximo sensor do menor caminho.
                    rssf[caminho].bateria = rssf[caminho].bateria - (0.025 * (0.1 + (0.0001 * dist)))
            #Se a bateria do sensor é menor que zero, não tem como continuar o processo de envio deste caminho.
            elif caminho != 0 and rssf[caminho].bateria < 0:
                break
            i += 1
    return mensagem

"""
Descrição: Função que simula o envio de uma mensagem de todos os sensores até a estação rádio-base. Quando um sensor recebe uma mensagem ele reenvia ela.
Entrada: Dicionário com as informações da rede.
Saída: Lista com todos os sensores que conseguiram enviar a mensagem.
"""
def todosEnviam(rssf):
    mensagem = [] # Lista com os sensores que enviaram a mensagem

    """ Iniciando o processo de envio das mensagens. """
    #Percorrendo os sensores que irão enviar as mensagens.
    for sensor in rssf:
        if sensor != "tam" and sensor != "ERB":
            i = 0 #Indice do elemento atual na lista do menor caminho.
            #Percorrendo os sensores que estão no menor caminho.
            for caminho in rssf[sensor].menorCaminho:
                #Um elemento só poderá receber ou enviar uma mensagem se ele tiver sua bateria maior que 0 e for diferente da estação rádio-base (0)
                if caminho != 0 and rssf[caminho].bateria > 0:
                    #Se o elemento atual do caminho for diferente do elemento inicial, então ele também gasta bateria para receber.
                    if caminho != sensor:
                        rssf[caminho].bateria = rssf[caminho].bateria - 0.00164
                    else:
                        #Elemento teve sucesso no envio da mensagem
                        mensagem.append(sensor)
                    #Verificando para quem o sensor vai enviar a mensagem.
                    if rssf[sensor].menorCaminho[i + 1] == 0:
                        #Enviando para a ERB.
                        rssf[caminho].bateria = rssf[caminho].bateria - (0.025 * (0.1 + (0.0001 * rssf[caminho].vizinhos["ERB"])))
                    else:
                        #Enviando para o próximo sensor do menor caminho.
                        dist = rssf[caminho].vizinhos[rssf[sensor].menorCaminho[i + 1]] #Pegando a distância do sensor atual até o próximo sensor do menor caminho.
                        rssf[caminho].bateria = rssf[caminho].bateria - (0.025 * (0.1 + (0.0001 * dist)))
                #Se a bateria do sensor é menor que zero, não tem como continuar o processo de envio deste caminho.
                elif caminho != 0 and rssf[caminho].bateria < 0:
                    break
                i += 1
    return mensagem


""" ------------- MENOR CAMINHO ------------- """


"""
Descrição: Função responsável por simular os ciclos dos sensores na rede na modelagem de distância com o método de menor caminho.
Entrada: A matriz de adjacência ponderada inicial; Dicionário com as informações da rede.
Saída: Ciclo no qual a estação rádio-base identificou uma morte.
"""
def startMC(matriz, rssf):
    """ Variáveis principais """
    ciclo = 0 #Ciclo
    condicao = 1 #Condição de parada dos ciclos -> ERB identificou uma morte
    var_10 = 10 #Variável que irá informar quando recalcular as distâncias dos vizinhos.
    var_20 = 20 #Variável que irá informar quando todos os sensores irão enviar uma mensagem para ERB.
    qnt = int(rssf["tam"] * 0.25) #Quantidade de sensores que irão mandar mensagem por ciclo.
    firstDead = 0 #Variável que irá nos informar quando ocorreu a primeira morte.

    #Calculando os menores caminhos de cada sensor.
    for sensor in range(1, rssf["tam"] + 1):
        rssf[sensor].menorCaminho = met.dijkstra(matriz, sensor, 0)
        print(rssf[sensor].menorCaminho)

    """ Iniciando os ciclos """
    while condicao:
        sensores = [] #Lista que conterá os sensores que irão enviar a mensagem
        mensagem = [] #Lista que conterá quais sensores conseguiram enviar suas mensagens
        ciclo += 1
        #A cada 10 ciclos, todos os sensores deverão informar os seus vizinhos suas novas baterias
        if ciclo == var_10:
            #Atualizando as baterias.
            for sensor in range(1, rssf["tam"] + 1):
                rssf[sensor].infVizinhos(rssf)
            #Atualizando a matriz.
            atualizaMatriz(rssf, matriz)
            #Atualizando os menores caminhos.
            for sensor in range(1, rssf["tam"] + 1):
                rssf[sensor].menorCaminho = met.dijkstra(matriz, sensor, 0)
            var_10 += 10
        #A cada 20 ciclos, todos os sensores deverão enviar uma mensagem para a ERB.
        if ciclo == var_20:
            mensagem = todosEnviam(rssf)
            #Se a quantidade de sensores que conseguiram enviar uma mensagem for menor do que a quantidade total de sensores, então um sensor morreu e a ERB identificou.
            if len(mensagem) != rssf["tam"]:
                condicao = 0
            var_20 += 20
        #Se não acontecer nenhum dos dois anteriores, sensores aleatórios irão enviar uma mensagem.
        elif ciclo != var_10:
            #Gerando os sensores, sem repetir.
            while len(sensores) < qnt:
                aleatorio = rd.randint(1, rssf["tam"])
                if aleatorio not in sensores:
                    sensores.append(aleatorio)
            #Enviando a mensagem.
            mensagem = enviaMensagem(rssf, sensores)
            #Se a quantidade de sensores que conseguiram enviar suas mensagens for menor do que a quantidade estabelecida, a primeira morte aconteceu.
            if len(mensagem) < qnt and firstDead == 0:
                firstDead = ciclo
        """for s in rssf:
            if s != "tam" and s != "ERB":
                print(rssf[s].bateria)
        print()"""
    print(ciclo, firstDead)
    return ciclo


""" ------------- ÁRVORE GERADORA MÍNIMA ------------- """


"""
Descrição: Função responsável por chamar o Algoritmo de Kruskal para gerar a árvore mínima.
Entrada: Matriz de adjacência ponderada; Dicionário com as informações da rede.
Saída: Árvore mínima em matriz; Dicionário com as incidências.
"""
def atualizaArvore(matriz, rssf):
    """ Variáveis principais """
    arvore = met.kruskal(matriz, rssf) #Montando a árvore.
    listaAdj = {} #Dicionário das incidências.

    """ Montando o dicionário """
    for i in range(len(arvore)):
        listaAdj[i] = []
        for j in range(len(arvore)):
            if arvore[i][j] == 1:
                listaAdj[i].append(j)
    return arvore, listaAdj


"""
Descrição: Função responsável por simular os ciclos dos sensores na rede na modelagem de distância com o método árvore mínima.
Entrada: A matriz de adjacência ponderada inicial; Dicionário com as informações da rede.
Saída: Ciclo no qual a estação rádio-base identificou uma morte.
"""
def startAG(matriz, rssf):
    """ Variáveis principais """
    ciclo = 0 #Ciclo
    condicao = 1 #Condição de parada dos ciclos -> ERB identificou uma morte
    var_10 = 10 #Variável que irá informar quando recalcular as distâncias dos vizinhos.
    var_20 = 20 #Variável que irá informar quando todos os sensores irão enviar uma mensagem para ERB.
    qnt = int(rssf["tam"] * 0.25) #Quantidade de sensores que irão mandar mensagem por ciclo.
    firstDead = 0 #Variável que irá nos informar quando ocorreu a primeira morte.
    arvore, listaAdj = atualizaArvore(matriz, rssf) #Matriz representando o grafo em uma árvore mínima; Dicionário com a incidência de cada vértice.

    #Calculando o caminho de cada sensor.
    for sensor in range(1, rssf["tam"] + 1):
        rssf[sensor].menorCaminho = met.dfs(listaAdj, sensor, 0)

    """ Iniciando os ciclos """
    while condicao:
        sensores = [] #Lista que conterá os sensores que irão enviar a mensagem
        mensagem = [] #Lista que conterá quais sensores conseguiram enviar suas mensagens
        ciclo += 1
        #A cada 10 ciclos, todos os sensores deverão informar os seus vizinhos suas novas baterias
        if ciclo == var_10:
            #Atualizando as baterias.
            for sensor in range(1, rssf["tam"] + 1):
                rssf[sensor].infVizinhos(rssf)
            #Atualizando a matriz.
            atualizaMatriz(rssf, matriz)
            #Atualizando a árvore e a lista de adjacência.
            arvore, listaAdj = atualizaArvore(matriz, rssf)
            #Atualizando os caminhos.
            for sensor in range(1, rssf["tam"] + 1):
                rssf[sensor].menorCaminho = met.dfs(listaAdj, sensor, 0)
            var_10 += 10
        #A cada 20 ciclos, todos os sensores deverão enviar uma mensagem para a ERB.
        if ciclo == var_20:
            mensagem = todosEnviam(rssf)
            #Se a quantidade de sensores que conseguiram enviar uma mensagem for menor do que a quantidade total de sensores, então um sensor morreu e a ERB identificou.
            if len(mensagem) != rssf["tam"]:
                condicao = 0
            var_20 += 20
        #Se não acontecer nenhum dos dois anteriores, sensores aleatórios irão enviar uma mensagem.
        elif ciclo != var_10:
            #Gerando os sensores, sem repetir.
            while len(sensores) < qnt:
                aleatorio = rd.randint(1, rssf["tam"])
                if aleatorio not in sensores:
                    sensores.append(aleatorio)
            #Enviando a mensagem.
            mensagem = enviaMensagem(rssf, sensores)
            #Se a quantidade de sensores que conseguiram enviar suas mensagens for menor do que a quantidade estabelecida, a primeira morte aconteceu.
            if len(mensagem) < qnt and firstDead == 0:
                firstDead = ciclo
    print(ciclo, firstDead)
    return ciclo

import math
import numpy as np
import random as rd

#Classe responsável por representar os sensores.
class Sensor():
    def __init__(self, identidade, x, y):
        self.__identidade = identidade #Nome do sensor, numérico.
        self.__x = x #Coordenada x do sensor.
        self.__y = y #Coordenada y do sensor.
        self.__alcance = 200 #Alcance do sensor.
        self.__vizinhos = {} #Dicionário de vizinhos do sensor, cada chave é a distância até o sensor.
        self.__bateriaViz = {} #Dicionário das baterias dos vizinhos.
        self.__bateria = 2500 #Bateria do sensor.
        self.__menorCaminho = [] #Lista com o menor caminho.

    @property
    def identidade(self):
        return self.__identidade

    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y
    
    @property
    def alcance(self):
        return self.__alcance
    
    @property
    def vizinhos(self):
        return self.__vizinhos
    
    @property
    def bateriaViz(self):
        return self.__bateriaViz

    @property
    def bateria(self):
        return self.__bateria
    
    @bateria.setter
    def bateria(self, nValor):
        self.__bateria = nValor
    
    @property
    def menorCaminho(self):
        return self.__menorCaminho
    
    @menorCaminho.setter
    def menorCaminho(self, mCaminho):
        self.__menorCaminho = mCaminho

    """
    Descrição: Função do sensor, responsável por calcular os seus vizinhos.
    Entrada: Dicionário com as informações da rede.
    Saída: Nada.
    """
    def calcVizinhos(self, rssf):
        #Calculando a distância até a estação rádio-base usando teorema de pitágoras (c² = a² + b²).
        dist = math.sqrt(((self.x - rssf["ERB"][0])**2) + ((self.y - rssf["ERB"][1])**2))
        #Verificando se está no alcance so sensor.
        if dist <= self.alcance:
            self.__vizinhos["ERB"] = dist

        #Percorrendo os sensores.
        for chave in range(1, rssf["tam"] + 1):
            if chave != self.identidade:
                #Calculando a distância até a estação rádio-base usando teorema de pitágoras (c² = a² + b²).
                dist = math.sqrt(((self.x - rssf[chave].x)**2) + ((self.y - rssf[chave].y)**2))
                #Verificando se está no alcance so sensor.
                if dist <= self.alcance:
                    self.__vizinhos[chave] = dist
                    self.__bateriaViz[chave] = 2500
    
    """
    Descrição: Função do sensor, responsável por simular o envio de uma mensagem para os vizinhos informando a bateria.
    Entrada: Dicionário com as informações da rede.
    Saída: Nada.
    """
    def infVizinhos(self, rssf):
        #Percorrendo os vizinhos.
        for vizinho in self.vizinhos:
            #O sensor só poderá enviar uma mensagem se o destino não for a ERB, e sua bateria for maior que 0.
            if vizinho != "ERB" and self.bateria > 0:
                self.bateria = self.bateria - 5
                #Atualizando a bateria no sensor vizinho.
                if rssf[vizinho].bateria > 0:
                    rssf[vizinho].bateriaViz[self.identidade] = self.bateria
                    rssf[vizinho].bateria = rssf[vizinho].bateria - 2

"""
Descrição: Função responsável por ler o dataset e gerar um dicionário com as informações da rede.
Entrada: Nada.
Saída: Dicionário onde tam é a chave para o tamanho, ERB é a chave para um tupla com as coordenadas da estação rádio-base, o resto são números (iniciando do 1)
    que guardam objetos dos sensores.
"""
def leCoordenadas():
    """ Variáveis principais """
    rssf = {} #Dicionário da rede
    arquivo = "C:\\Users\\Usuario\\Documents\\01 - Universidade\\3 - Periodo\\CMAC03 - Algoritmos em Grafos\\Trabalho\\Coordenadas\\Rede 100.txt" #Caminho
    sensor = 0 #Auxiliar

    """ Lendo o dataset """
    with open(arquivo) as arq:
        rssf["tam"] = int(arq.readline()) #Adicionando o tamanho ao dicionário.
        linhas = arq.readlines()
    
    """ Preenchendo o resto do dicionário """
    for linha in linhas:
        #Se o sensor for igual à zero, significa que estamos lendo os dados da estação rádio-base.
        if sensor == 0:
            rssf["ERB"] = tuple(float(val) for val in linha.strip().split(','))
        else:
            rssf[sensor] = Sensor(sensor, float(linha.strip().split(',')[0]), float(linha.strip().split(',')[1]))
        sensor += 1
    
    return rssf

"""
Descrição: Algoritmo de menor caminho de Dijkstra.
Entrada: Matriz de incidência ponderada; Vértice de origem; Vértice de destino.
Saída: Lista com o menor caminho do vértice de origem até o de destino.
"""
def dijkstra(matriz, vOrigem, vDestino):
    """ Variáveis principais """
    custo = {} #Dicionário que representa os custos.
    rota = {} #Dicionário com a rota de menor caminho.
    A = [i for i in range(len(matriz))] #Vértices em aberto.
    F = [] #Vértices fechados.
    menorC = [] #Lista com o menor caminho.

    #Inicializando os dicionários.
    for i in range(len(matriz)):
        if i == vOrigem:
            custo[i] = 0
            rota[i] = vOrigem
        else:
            custo[i] = -1
            rota[i] = 0

    """ Iniciando o processo de descobrimento do menor caminho """
    while A:
        v = A[0] #Vértice com o menor custo em aberto.
        #Processo para descobrir qual é o vértice com menor custo em aberto.
        for i in A:
            if custo[v] == -1 or (custo[i] != -1 and custo[i] < custo[v]):
                v = i
        F.append(v)
        A.remove(v)
        N = [] #Adjacentes de v em aberto
        #Processo para descobrir esses adjacentes.
        for i in range(len(matriz)):
            if matriz[v][i] > 0 and i not in F:
                N.append(i)
        #Setando os custos em relação a v e seus adjacentes
        for u in N:
            if custo[v] + matriz[v][u] < custo[u] or custo[u] == -1:
                custo[u] = custo[v] + matriz[v][u]
                rota[u] = v
    
    """ Montando o menor caminho """
    menor = vDestino
    while menor != vOrigem:
        menorC.append(menor)
        menor = rota[menor]
    menorC.append(menor)
    menorC.reverse()
    return menorC

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
                matriz[i][vizinho] = rssf[i].vizinhos[vizinho] + (((2500 - rssf[vizinho].bateria) / 25) * 1000)

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
        #Percorrendo os sensores que estão no menor caminho.
        for caminho in rssf[sensor].menorCaminho:
            #Um elemento só poderá receber ou enviar uma mensagem se ele tiver sua bateria maior que 0 e for diferente da estação rádio-base (0)
            if caminho != 0 and rssf[caminho].bateria > 0:
                #Se o elemento atual do caminho for diferente do elemento inicial, então ele também gasta bateria para receber.
                if caminho != sensor:
                    rssf[caminho].bateria = rssf[caminho].bateria - 2
                else:
                    #Elemento teve sucesso no envio da mensagem
                    mensagem.append(sensor)
                rssf[caminho].bateria = rssf[caminho].bateria - 5
            #Se a bateria do sensor é menor que zero, não tem como continuar o processo de envio deste caminho.
            elif caminho != 0 and rssf[caminho].bateria < 0:
                break
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
            #Percorrendo os sensores que estão no menor caminho.
            for caminho in rssf[sensor].menorCaminho:
                #Um elemento só poderá receber ou enviar uma mensagem se ele tiver sua bateria maior que 0 e for diferente da estação rádio-base (0)
                if caminho != 0 and rssf[caminho].bateria > 0:
                    #Se o elemento atual do caminho for diferente do elemento inicial, então ele também gasta bateria para receber.
                    if caminho != sensor:
                        rssf[caminho].bateria = rssf[caminho].bateria - 2
                    else:
                        #Elemento teve sucesso no envio da mensagem
                        mensagem.append(sensor)
                    rssf[caminho].bateria = rssf[caminho].bateria - 5
                #Se a bateria do sensor é menor que zero, não tem como continuar o processo de envio deste caminho.
                elif caminho != 0 and rssf[caminho].bateria < 0:
                    break
    return mensagem

"""
Descrição: Função responsável por simular os ciclos dos sensores na rede.
Entrada: A matriz de adjacência ponderada inicial; Dicionário com as informações da rede.
Saída: Ciclo no qual a estação rádio-base identificou uma morte.
"""
def start(matriz, rssf):
    """ Variáveis principais """
    ciclo = 0 #Ciclo
    condicao = 1 #Condição de parada dos ciclos -> ERB identificou uma morte
    var_10 = 10 #Variável que irá informar quando recalcular as distâncias dos vizinhos.
    var_20 = 20 #Variável que irá informar quando todos os sensores irão enviar uma mensagem para ERB.
    qnt = int(rssf["tam"] * 0.25) #Quantidade de sensores que irão mandar mensagem por ciclo.
    firstDead = 0 #Variável que irá nos informar quando ocorreu a primeira morte.

    #Calculando os menores caminhos de cada sensor.
    for sensor in range(1, rssf["tam"] + 1):
        rssf[sensor].menorCaminho = dijkstra(matriz, sensor, 0)

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
                rssf[sensor].menorCaminho = dijkstra(matriz, sensor, 0)
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

"""
Descrição: Função principal, responsável por montar a matriz de incidência ponderada inicial, e por chamar as funções de leitura do dataset e início do ciclo.
Entrada: Nada.
Saída: Nada.
"""
def main():
    rssf = leCoordenadas() #Dicionário com as informações da rede.

    """ Imprimindo informações --> Remover quando estiver finalizado. """
    print(f"Tamanho: {rssf["tam"]}")
    print(f"Estação rádio-base: {rssf["ERB"]}")
    for i in range(1, rssf["tam"] + 1):
        print(f"{rssf[i].identidade} - X: {rssf[i].x}, Y: {rssf[i].y}")
    
    """ Montando a matriz inicial. """
    matriz = np.zeros((rssf["tam"] + 1, rssf["tam"] + 1), dtype="float64")

    for i in range(1, rssf["tam"] + 1):
        rssf[i].calcVizinhos(rssf)
        for vizinho in rssf[i].vizinhos:
            if vizinho == "ERB":
                matriz[i][0] = rssf[i].vizinhos[vizinho]
            else:
                matriz[i][vizinho] = rssf[i].vizinhos[vizinho] + (((2500 - rssf[vizinho].bateria) / 25) * 1000)
    
    #Chamando a função que irá iniciar os ciclos.
    start(matriz, rssf)

if __name__ == "__main__":
    main()
    
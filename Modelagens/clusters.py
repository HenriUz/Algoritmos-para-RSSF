import numpy as np
import random as rd
import math
from sklearn.cluster import KMeans
from Metodos import metodos as met


""" ------------- CLASSES ------------- """


#Class que vai representar um cluster
class Cluster():
    def __init__(self, identidade, x, y):
        self.__identidade = identidade
        self.__x = x
        self.__y = y
        self.__alcance = 400
        self.__bateria = 2500
        self.__clustersViz = {}
        self.__bateriaClu = {}
        self.__sensoresViz = {}
        self.__bateriaSen = {}
        self.__menorCaminho = []
    
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
    def bateria(self):
        return self.__bateria
    
    @bateria.setter
    def bateria(self, valor):
        self.__bateria = valor
    
    @property
    def clustersViz(self):
        return self.__clustersViz
    
    @property
    def bateriaClu(self):
        return self.__bateriaClu
    
    @property
    def sensoresViz(self):
        return self.__sensoresViz
    
    @property
    def bateriaSen(self):
        return self.__bateriaSen
    
    @property
    def menorCaminho(self):
        return self.__menorCaminho
    
    @menorCaminho.setter
    def menorCaminho(self, mCaminho):
        self.__menorCaminho = mCaminho

    def calcVizinhos(self, rssf, vizinhos, clusters):
        #Calculando a distância até a estação rádio-base usando teorema de pitágoras (c² = a² + b²).
        dist = math.sqrt(((self.x - rssf["ERB"][0])**2) + ((self.y - rssf["ERB"][1])**2))
        #Verificando se está no alcance so sensor.
        if dist <= self.alcance:
            self.__clustersViz["ERB"] = dist

        #Calculando a distância até seus sensores vizinhos.
        vizinhos.remove(self.identidade - 1)
        for sensores in vizinhos:
            self.__sensoresViz[sensores + 1] = math.sqrt(((self.x - rssf[sensores + 1].x)**2) + ((self.y - rssf[sensores + 1].y)**2))
            self.__bateriaSen[sensores + 1] = self.bateria
        
        #Calculando a distância até seus clusters vizinhos.
        for cluster in clusters:
            if cluster != self.identidade:
                dist = math.sqrt(((self.x - rssf[cluster].x)**2) + ((self.y - rssf[cluster].y)**2))
                if dist <= self.alcance:
                    self.__clustersViz[cluster] = dist
                    self.__bateriaClu[cluster] = self.bateria

    def informaVizinhos(self, rssf):
        for cluster in self.clustersViz:
            if cluster != "ERB" and self.bateria > 0:
                self.bateria = self.bateria - (0.025 * (0.1 + (0.0001 * self.clustersViz[cluster])))
                if rssf[cluster].bateria > 0:
                    rssf[cluster].bateria = rssf[cluster].bateria - 0.00164
                    rssf[cluster].bateriaClu[self.identidade] = self.bateria


class Sensor():
    def __init__(self, identidade, x, y, cluster):
        self.__identidade = identidade
        self.__x = x
        self.__y = y
        self.__alcance = 300
        self.__bateria = 2500
        self.__cluster = cluster
        self.__bateriaClu = 2500
    
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
    def bateria(self):
        return self.__bateria
    
    @bateria.setter
    def bateria(self, valor):
        self.__bateria = valor
    
    @property
    def cluster(self):
        return self.__cluster
    
    @property
    def bateriaClu(self):
        return self.__bateriaClu
    
    @bateriaClu.setter
    def bateriaClu(self, valor):
        self.__bateriaClu = valor
    
    def informaCluster(self, rssf):
        if self.bateria > 0:
            dist = math.sqrt((self.x - rssf[self.cluster].x) ** 2 + (self.y - rssf[self.cluster].y) ** 2)
            self.bateria = self.bateria - (0.025 * (0.1 + (0.0001 * dist)))
            if rssf[self.cluster].bateria > 0:
                rssf[self.cluster].bateria = rssf[self.cluster].bateria - 0.00164
                rssf[self.cluster].bateriaSen[self.identidade] = self.bateria


""" ------------- FUNÇÕES AUXILIARES ------------- """ 


"""
Descrição: Função que com base nos sensores da rssf, cria regiões de clusters.
Entrada: Dicionário com as informações da rede.
Saída: Lista com os índices dos sensores que se tornarão clusters; Dicionário com os sensores de cada região (as chaves vão de 0 até o número de regiões - 1).
"""
def montaKMeans(rssf):
    sensores = [] #Lista que armazena as coordenadas (x, y) de cada sensor. O índice da lista é a identidade do sensor - 1.
    for i in rssf:
        if i != "tam" and i != "ERB":
            sensores.append([rssf[i][0], rssf[i][1]])
    sensores = np.array(sensores)

    """ Montando as regiões de cluster """
    km = KMeans(n_clusters=int(rssf["tam"] * 0.2), init="k-means++", random_state=0)
    label = km.fit_predict(sensores)
    regioes = dict([i, []] for i in range(int(rssf["tam"] * 0.2)))
    for i in range(len(label)):
        regioes[label[i]].append(i)
    
    """plt.figure(figsize=(8, 6))
    plt.scatter(sensores[:, 0], sensores[:, 1], c=label, cmap='viridis', s=50, alpha=0.7)
    plt.title('Clusters de Sensores usando K-Means')
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.colorbar(label='Cluster')
    plt.show()"""

    return encontraCluster(rssf, regioes, sensores)


"""
Descrição: Função que com base nas regiões e coordenadas dos sensores, identifica qual sensor da região se qualifica como cluster (está no alcance de todos os outros).
Entrada: Dicionário com as informações da rede; Dicionário com os sensores de cada região; Lista com as coordenadas de cada sensor.
Saída: Lista com os sensores qualificados para clusters de cada região; Dicionário com os sensores de cada região.
"""
def encontraCluster(rssf, regioes, sensores):
    clusters = [] #Lista de clusters qualificados.
    
    """ Calculando os clusters qualificados O(n³) """
    #Percorrendo as regiões.
    for regiao in regioes:
        nClusters = [] #Lista de sensores não qualificados da região.
        #Percorrendo os sensores da região.
        for s1 in regioes[regiao]:
            #Percorrendo os sensores da região para calcular a distância entre os dois.
            for s2 in regioes[regiao]:
                #Calculando a distância entre os dois.
                distancia = (math.sqrt((sensores[s1][0] - sensores[s2][0])**2 + (sensores[s1][1] - sensores[s2][1])**2))
                if distancia > 300 and s2 not in nClusters:
                    nClusters.append(s2)
        clusters.append(list(set(regioes[regiao]) - set(nClusters))[0] + 1)
    return clusters, regioes


"""
Descrição: Função responsável por atualizar a matriz de incidência ponderada com os novos valores dos arcos.
Entrada: Dicionário com as informações da rede; Matriz de incidência ponderada; Lista com os clusters.
Saída: Indiretamente a matriz atualizada.
"""
def atualizaMatriz(rssf, matriz, clusters):
    #Percorrendo os sensores da rede.
    for i in clusters:
        #Percorrendo os vizinhos desse sensor.
        for vizinho in rssf[i].clustersViz:
            #Se o vizinho não for a estação rádio-base, atualiza o valor da aresta.
            if vizinho != "ERB":
                matriz[i][vizinho] = rssf[i].clustersViz[vizinho] + (((2500 - rssf[i].bateriaClu[vizinho]) / 25) * 1000)


"""
Descrição: Função que simula o envio de uma mensagem de um sensor até a estação rádio-base. Os sensores enviam primeiro, e depois os clusters enviam.
Entrada: Dicionário com as informações da rede; Sensores/Clusters que irão enviar a mensagem.
Saída: Lista com todos os sensores que conseguiram enviar a mensagem.
"""
def enviaMensagem(rssf, envia, tipo):
    mensagem = [] # Lista com os sensores que enviaram a mensagem.
    clusters = [] # Lista com os clusters presentes na lista envia.

    """ Iniciando o processo de envio das mensagens. """
    #Percorrendo os sensores que irão enviar as mensagens.
    for sensor in envia:
        #Identificando o sensor pelo seu alcance. Se for cluster adiciona na lista, se não for envia a mensagem.
        if rssf[sensor].alcance == 400:
            clusters.append(sensor)
        else:
            if rssf[sensor].bateria > 0:
                #Calculando a nova bateria do sensor.
                dist = math.sqrt((rssf[sensor].x - rssf[rssf[sensor].cluster].x) ** 2 + (rssf[sensor].y - rssf[rssf[sensor].cluster].y) ** 2)
                rssf[sensor].bateria = rssf[sensor].bateria - (0.025 * (0.1 + (0.0001 * dist)))
                #Enviou a mensagem com sucesso.
                mensagem.append(sensor)
                #Se o cluster que o sensor envia mensagem tiver bateria maior que 0, ele gasta bateria para receber a mensagem.
                if rssf[rssf[sensor].cluster].bateria > 0:
                    rssf[rssf[sensor].cluster].bateria = rssf[rssf[sensor].cluster].bateria - 0.00164
    
    #Percorrendo os clusters que irão enviar as mensagens.
    for cluster in clusters:
        if rssf[cluster].bateria > 0:
            i = 0 #Indice do elemento atual na lista do menor caminho.
            #Percorrendo os sensores que estão no menor caminho.
            for caminho in rssf[cluster].menorCaminho:
                #Um elemento só poderá receber ou enviar uma mensagem se ele tiver sua bateria maior que 0 e for diferente da estação rádio-base (0)
                if caminho != 0 and rssf[caminho].bateria > 0:
                    #Se o elemento atual do caminho for diferente do elemento inicial, então ele também gasta bateria para receber.
                    if caminho != cluster:
                        rssf[caminho].bateria = rssf[caminho].bateria - 0.00164
                    else:
                        #Elemento inicial teve sucesso no envio da mensagem
                        mensagem.append(cluster)
                    #Verificando para quem o sensor vai enviar a mensagem.
                    if rssf[cluster].menorCaminho[i + 1] == 0:
                        #Enviando para a ERB.
                        if tipo:
                            rssf[caminho].bateria = rssf[caminho].bateria - (0.025 * (0.1 + (0.0001 * rssf[caminho].clustersViz["ERB"])))
                        else:
                            dist = math.sqrt((rssf[caminho].x - rssf["ERB"][0])**2 + (rssf[caminho].y - rssf["ERB"][1])**2)
                            rssf[caminho].bateria = rssf[caminho].bateria - (0.025 * (0.1 + (0.0001 * dist)))
                    else:
                        #Enviando para o sensor do próximo cluster do menor caminho.
                        if tipo:
                            dist = rssf[caminho].clustersViz[rssf[cluster].menorCaminho[i + 1]] #Pegando a distância do cluster atual até o próximo cluster do menor caminho.
                        else:
                            dist = math.sqrt((rssf[caminho].x - rssf[rssf[cluster].menorCaminho[i + 1]].x)**2 + (rssf[caminho].y - rssf[rssf[cluster].menorCaminho[i + 1]].y)**2)
                        rssf[caminho].bateria = rssf[caminho].bateria - (0.025 * (0.1 + (0.0001 * dist)))
                #Se a bateria do sensor é menor que zero, não tem como continuar o processo de envio deste caminho.
                elif caminho != 0 and rssf[caminho].bateria < 0:
                    break
                i+=1

    return mensagem


"""
Descrição: Função que simula o envio de uma mensagem de todos os sensores até a estação rádio-base. Os sensores enviam primeiro, e depois os clusters enviam.
Entrada: Dicionário com as informações da rede; Lista com os clusters; Lista com os sensores.
Saída: Lista com todos os sensores que conseguiram enviar a mensagem.
"""
def todosEnviam(rssf, clusters, sensores, tipo):
    mensagem = [] # Lista com os sensores que enviaram a mensagem

    """ Iniciando o processo de envio das mensagens. """
    #Percorrendo os sensores que irão enviar as mensagens.
    for sensor in sensores:
        if rssf[sensor].bateria > 0:
            #Calculando a nova bateria do sensor.
            dist = math.sqrt((rssf[sensor].x - rssf[rssf[sensor].cluster].x) ** 2 + (rssf[sensor].y - rssf[rssf[sensor].cluster].y) ** 2)
            rssf[sensor].bateria = rssf[sensor].bateria - (0.025 * (0.1 + (0.0001 * dist)))
            #Enviou a mensagem com sucesso.
            mensagem.append(sensor)
            #Se o cluster que o sensor envia mensagem tiver bateria maior que 0, ele gasta bateria para receber a mensagem.
            if rssf[rssf[sensor].cluster].bateria > 0:
                rssf[rssf[sensor].cluster].bateria = rssf[rssf[sensor].cluster].bateria - 0.00164
    
    #Percorrendo os clusters que irão enviar as mensagens.
    for cluster in clusters:
        if rssf[cluster].bateria > 0:
            i = 0 #Indice do elemento atual na lista do menor caminho.
            #Percorrendo os sensores que estão no menor caminho.
            for caminho in rssf[cluster].menorCaminho:
                #Um elemento só poderá receber ou enviar uma mensagem se ele tiver sua bateria maior que 0 e for diferente da estação rádio-base (0)
                if caminho != 0 and rssf[caminho].bateria > 0:
                    #Se o elemento atual do caminho for diferente do elemento inicial, então ele também gasta bateria para receber.
                    if caminho != cluster:
                        rssf[caminho].bateria = rssf[caminho].bateria - 0.00164
                    else:
                        #Elemento inicial teve sucesso no envio da mensagem
                        mensagem.append(cluster)
                    #Verificando para quem o sensor vai enviar a mensagem.
                    if rssf[cluster].menorCaminho[i + 1] == 0:
                        #Enviando para a ERB.
                        if tipo:
                            rssf[caminho].bateria = rssf[caminho].bateria - (0.025 * (0.1 + (0.0001 * rssf[caminho].clustersViz["ERB"]))) #Pegando a distância do sensor atual até o próximo sensor do menor caminho.
                        else:
                            dist = math.sqrt((rssf[caminho].x - rssf["ERB"][0])**2 + (rssf[caminho].y - rssf["ERB"][1])**2)
                            rssf[caminho].bateria = rssf[caminho].bateria - (0.025 * (0.1 + (0.0001 * dist)))
                    else:
                        #Enviando para o próximo sensor do menor caminho.
                        if tipo:
                            dist = rssf[caminho].clustersViz[rssf[cluster].menorCaminho[i + 1]] #Pegando a distância do sensor atual até o próximo sensor do menor caminho.
                        else:
                            dist = math.sqrt((rssf[caminho].x - rssf[rssf[cluster].menorCaminho[i + 1]].x)**2 + (rssf[caminho].y - rssf[rssf[cluster].menorCaminho[i + 1]].y)**2)
                        rssf[caminho].bateria = rssf[caminho].bateria - (0.025 * (0.1 + (0.0001 * dist)))
                #Se a bateria do sensor é menor que zero, não tem como continuar o processo de envio deste caminho.
                elif caminho != 0 and rssf[caminho].bateria < 0:
                    break
                i+=1
    return mensagem


""" ------------- MENOR CAMINHO ------------- """


"""
Descrição: Função responsável por simular os ciclos dos sensores na rede na modelagem de clusters com o método de menor caminho.
Entrada: A matriz de adjacência ponderada inicial; Dicionário com as informações da rede; Lista com os clusters.
Saída: Ciclo no qual a estação rádio-base identificou uma morte.
"""
def startMC(matriz, rssf, clusters):
    """ Variáveis principais """
    ciclo = 0 #Ciclo
    condicao = 1 #Condição de parada dos ciclos -> ERB identificou uma morte
    var_10 = 10 #Variável que irá informar quando recalcular as distâncias dos vizinhos.
    var_20 = 20 #Variável que irá informar quando todos os sensores irão enviar uma mensagem para ERB.
    qnt = int(rssf["tam"] * 0.25) #Quantidade de sensores que irão mandar mensagem por ciclo.
    firstDead = 0 #Variável que irá nos informar quando ocorreu a primeira morte.
    sensores = list(set([i for i in range(1, rssf["tam"] + 1)]) - set(clusters)) #Todos os sensores que não são clusters.

    #Calculando os menores caminhos de cada sensor.
    for cluster in clusters:
        rssf[cluster].menorCaminho = met.dijkstra(matriz, cluster, 0)
    
    while condicao:
        envia = [] #Lista que conterá os sensores que irão enviar a mensagem
        mensagem = [] #Lista que conterá quais sensores conseguiram enviar suas mensagens
        ciclo += 1
        #A cada 10 ciclos, todos os sensores deverão informar os seus vizinhos suas novas baterias
        if ciclo == var_10:
            #Atualizando as baterias.
            for sensor in sensores:
                rssf[sensor].informaCluster(rssf)
            for cluster in clusters:
                rssf[cluster].informaVizinhos(rssf)
            #Atualizando a matriz.
            atualizaMatriz(rssf, matriz, clusters)
            #Atualizando os menores caminhos.
            for cluster in clusters:
                rssf[cluster].menorCaminho = met.dijkstra(matriz, cluster, 0)
            var_10 += 10
        #A cada 20 ciclos, todos os sensores deverão enviar uma mensagem para a ERB.
        if ciclo == var_20:
            mensagem = todosEnviam(rssf, clusters, sensores, True)
            #Se a quantidade de sensores que conseguiram enviar uma mensagem for menor do que a quantidade total de sensores, então um sensor morreu e a ERB identificou.
            if len(mensagem) != rssf["tam"]:
                condicao = 0
            var_20 += 20
        #Se não acontecer nenhum dos dois anteriores, sensores aleatórios irão enviar uma mensagem.
        elif ciclo != var_10:
            #Gerando os sensores, sem repetir.
            while len(envia) < qnt:
                aleatorio = rd.randint(1, rssf["tam"])
                if aleatorio not in envia:
                    envia.append(aleatorio)
            #Enviando a mensagem.
            mensagem = enviaMensagem(rssf, envia, True)
            #Se a quantidade de sensores que conseguiram enviar suas mensagens for menor do que a quantidade estabelecida, a primeira morte aconteceu.
            if len(mensagem) < qnt and firstDead == 0:
                firstDead = ciclo
    print(ciclo, firstDead)
    return ciclo


""" ------------- MENOR CAMINHO COM SALTO ------------- """


"""
Descrição: Função responsável por simular os ciclos dos sensores na rede na modelagem de clusters com o método de menor caminho com salto.
Entrada: A matriz de adjacência ponderada inicial; Dicionário com as informações da rede; Lista com os clusters.
Saída: Ciclo no qual a estação rádio-base identificou uma morte.
"""
def startMS(matriz, rssf, clusters):
    """ Variáveis principais """
    ciclo = 0 #Ciclo
    condicao = 1 #Condição de parada dos ciclos -> ERB identificou uma morte
    var_10 = 10 #Variável que irá informar quando recalcular as distâncias dos vizinhos.
    var_20 = 20 #Variável que irá informar quando todos os sensores irão enviar uma mensagem para ERB.
    qnt = int(rssf["tam"] * 0.25) #Quantidade de sensores que irão mandar mensagem por ciclo.
    firstDead = 0 #Variável que irá nos informar quando ocorreu a primeira morte.
    sensores = list(set([i for i in range(1, rssf["tam"] + 1)]) - set(clusters)) #Todos os sensores que não são clusters.

    #Calculando os menores caminhos de cada sensor.
    for cluster in clusters:
        menorCaminho = met.dijkstra(matriz, cluster, 0)
        rssf[cluster].menorCaminho = menorCaminho[0::2]
        if rssf[cluster].menorCaminho[(len(rssf[cluster].menorCaminho) - 1)] != menorCaminho[len(menorCaminho) - 1]:
            rssf[cluster].menorCaminho.append(menorCaminho[len(menorCaminho) - 1])
    while condicao:
        envia = [] #Lista que conterá os sensores que irão enviar a mensagem
        mensagem = [] #Lista que conterá quais sensores conseguiram enviar suas mensagens
        ciclo += 1
        #A cada 10 ciclos, todos os sensores deverão informar os seus vizinhos suas novas baterias
        if ciclo == var_10:
            #Atualizando as baterias.
            for sensor in sensores:
                rssf[sensor].informaCluster(rssf)
            for cluster in clusters:
                rssf[cluster].informaVizinhos(rssf)
            #Atualizando a matriz.
            atualizaMatriz(rssf, matriz, clusters)
            #Atualizando os menores caminhos.
            for cluster in clusters:
                menorCaminho = met.dijkstra(matriz, cluster, 0)
                rssf[cluster].menorCaminho = menorCaminho[0::2]
                if rssf[cluster].menorCaminho[(len(rssf[cluster].menorCaminho) - 1)] != menorCaminho[len(menorCaminho) - 1]:
                    rssf[cluster].menorCaminho.append(menorCaminho[len(menorCaminho) - 1])
            var_10 += 10
        #A cada 20 ciclos, todos os sensores deverão enviar uma mensagem para a ERB.
        if ciclo == var_20:
            mensagem = todosEnviam(rssf, clusters, sensores, False)
            #Se a quantidade de sensores que conseguiram enviar uma mensagem for menor do que a quantidade total de sensores, então um sensor morreu e a ERB identificou.
            if len(mensagem) != rssf["tam"]:
                condicao = 0
            var_20 += 20
        #Se não acontecer nenhum dos dois anteriores, sensores aleatórios irão enviar uma mensagem.
        elif ciclo != var_10:
            #Gerando os sensores, sem repetir.
            while len(envia) < qnt:
                aleatorio = rd.randint(1, rssf["tam"])
                if aleatorio not in envia:
                    envia.append(aleatorio)
            #Enviando a mensagem.
            mensagem = enviaMensagem(rssf, envia, False)
            #Se a quantidade de sensores que conseguiram enviar suas mensagens for menor do que a quantidade estabelecida, a primeira morte aconteceu.
            if len(mensagem) < qnt and firstDead == 0:
                firstDead = ciclo
    print(ciclo, firstDead)
    return ciclo


""" ------------- ÁRVORE GERADORA MÍNIMA ------------- """


"""
Descrição: Função responsável por chamar o Algoritmo de Kruskal para gerar a árvore mínima.
Entrada: Matriz de adjacência ponderada; Dicionário com as informações da rede.
Saída: Árvore mínima em matriz; Dicionário com as incidências.
"""
def atualizaArvore(matriz, rssf, clusters):
    """ Variáveis principais """
    arvore = met.kruskal(matriz, rssf, len(clusters)) #Montando a árvore.
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
def startAG(matriz, rssf, clusters):
    """ Variáveis principais """
    ciclo = 0 #Ciclo
    condicao = 1 #Condição de parada dos ciclos -> ERB identificou uma morte
    var_10 = 10 #Variável que irá informar quando recalcular as distâncias dos vizinhos.
    var_20 = 20 #Variável que irá informar quando todos os sensores irão enviar uma mensagem para ERB.
    qnt = int(rssf["tam"] * 0.25) #Quantidade de sensores que irão mandar mensagem por ciclo.
    firstDead = 0 #Variável que irá nos informar quando ocorreu a primeira morte.
    arvore, listaAdj = atualizaArvore(matriz, rssf, clusters) #Matriz representando o grafo em uma árvore mínima; Dicionário com a incidência de cada vértice.
    print(listaAdj)
    sensores = list(set([i for i in range(1, rssf["tam"] + 1)]) - set(clusters)) #Todos os sensores que não são clusters.

    #Calculando o caminho de cada sensor.
    for sensor in range(1, rssf["tam"] + 1):
        rssf[sensor].menorCaminho = met.dfs(listaAdj, sensor, 0)

    """ Iniciando os ciclos """
    while condicao:
        envia = [] #Lista que conterá os sensores que irão enviar a mensagem
        mensagem = [] #Lista que conterá quais sensores conseguiram enviar suas mensagens
        ciclo += 1
        #A cada 10 ciclos, todos os sensores deverão informar os seus vizinhos suas novas baterias
        if ciclo == var_10:
            #Atualizando as baterias.
            for sensor in sensores:
                rssf[sensor].informaCluster(rssf)
            for cluster in clusters:
                rssf[cluster].informaVizinhos(rssf)
            #Atualizando a matriz.
            atualizaMatriz(rssf, matriz, clusters)
            #Atualizando a árvore e a lista de adjacência.
            arvore, listaAdj = atualizaArvore(matriz, rssf, clusters)
            #Atualizando os caminhos.
            for cluster in clusters:
                rssf[cluster].menorCaminho = met.dfs(listaAdj, cluster, 0)
            var_10 += 10
        #A cada 20 ciclos, todos os sensores deverão enviar uma mensagem para a ERB.
        if ciclo == var_20:
            mensagem = todosEnviam(rssf, clusters, sensores, True)
            #Se a quantidade de sensores que conseguiram enviar uma mensagem for menor do que a quantidade total de sensores, então um sensor morreu e a ERB identificou.
            if len(mensagem) != rssf["tam"]:
                condicao = 0
            var_20 += 20
        #Se não acontecer nenhum dos dois anteriores, sensores aleatórios irão enviar uma mensagem.
        elif ciclo != var_10:
            #Gerando os sensores, sem repetir.
            while len(envia) < qnt:
                aleatorio = rd.randint(1, rssf["tam"])
                if aleatorio not in envia:
                    envia.append(aleatorio)
            #Enviando a mensagem.
            mensagem = enviaMensagem(rssf, envia, True)
            #Se a quantidade de sensores que conseguiram enviar suas mensagens for menor do que a quantidade estabelecida, a primeira morte aconteceu.
            if len(mensagem) < qnt and firstDead == 0:
                firstDead = ciclo
    print(ciclo, firstDead)
    return ciclo

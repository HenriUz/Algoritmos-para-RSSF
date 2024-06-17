import numpy as np
import math
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


""" ------------- CLASSES ------------- """


#Class que vai representar um cluster
class Cluster():
    def __init__(self, identidade, x, y):
        self.__identidade = identidade
        self.__x = x
        self.__y = y
        self.__alcance = 300
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

    def calcVizinhos(self, rssf, vizinhos):
        #Calculando a distância até a estação rádio-base usando teorema de pitágoras (c² = a² + b²).
        dist = math.sqrt(((self.x - rssf["ERB"][0])**2) + ((self.y - rssf["ERB"][1])**2))
        #Verificando se está no alcance so sensor.
        if dist <= self.alcance:
            self.__clustersViz["ERB"] = dist

        
        vizinhos.remove(self.identidade)
        self.__sensoresViz = vizinhos
        
        

"""
Descrição: Função que com base nos sensores da rssf, cria regiões de clusters.
Entrada: Dicionário com as informações da rede.
Saída: Lista com os índices dos sensores que se tornarão clusters.
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
Saída: Lista com os sensores qualificados para clusters de cada região (o valor representa a identidade - 1); Dicionário com os sensores de cada região.
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
        clusters.append(list(set(regioes[regiao]) - set(nClusters))[0])
    return clusters, regioes


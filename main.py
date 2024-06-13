import math
import numpy as np
import random as rd
from Metodos import metodos as met
from Modelagens import distancia as dist


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
                    self.__bateriaViz[chave] = self.bateria
    
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
                self.bateria = self.bateria - (0.025 * (0.1 + (0.0001 * self.vizinhos[vizinho])))
                #Atualizando a bateria no sensor vizinho.
                if rssf[vizinho].bateria > 0:
                    rssf[vizinho].bateriaViz[self.identidade] = self.bateria
                    rssf[vizinho].bateria = rssf[vizinho].bateria - 0.00164

"""
Descrição: Função responsável por ler o dataset e gerar um dicionário com as informações da rede.
Entrada: Nada.
Saída: Dicionário onde tam é a chave para o tamanho, ERB é a chave para um tupla com as coordenadas da estação rádio-base, o resto são números (iniciando do 1)
    que guardam objetos dos sensores.
"""
def leCoordenadas():
    """ Variáveis principais """
    rssf = {} #Dicionário da rede
    arquivo = "C:\\Users\\Usuario\\Documents\\01 - Universidade\\3 - Periodo\\CMAC03 - Algoritmos em Grafos\\Trabalho\\Coordenadas\\Rede 50.txt" #Caminho
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
                matriz[i][vizinho] = rssf[i].vizinhos[vizinho]
    
    #Chamando a função que irá iniciar os ciclos.
    print("\nModelagens: 1 - Distância; 2 - Clusters")
    print("Métodos: 1 - Menor Caminho; 2 - Menor Caminho com Salto; 3 - Árvore Geradora Mínima")
    #resp = input("Digite qual modelagem e método você deseja executar (Combine a modelagem com o método, ex.: 11, 12, 13): ")
    resp = "11"
    if resp == "11":
        dist.startMC(matriz, rssf)
    elif resp == "13":
        dist.startAG(matriz, rssf)

if __name__ == "__main__":
    main()
    

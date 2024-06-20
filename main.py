import numpy as np
from Metodos import metodos as met
from Modelagens import distancia as dist, clusters as clu


"""
Descrição: Função responsável por ler o dataset e gerar um dicionário com as informações da rede.
Entrada: Nada.
Saída: Dicionário onde tam é a chave para o tamanho, ERB é a chave para um tupla com as coordenadas da estação rádio-base, o resto são números (iniciando do 1)
    que guardam as coordenadas dos sensores.
"""
def leCoordenadas(resp):
    """ Variáveis principais """
    rssf = {} #Dicionário da rede
    arquivo = f"Rede {resp}.txt" #Caminho
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
            #rssf[sensor] = Sensor(sensor, float(linha.strip().split(',')[0]), float(linha.strip().split(',')[1]))
            rssf[sensor] = (float(linha.strip().split(',')[0]), float(linha.strip().split(',')[1]))
        sensor += 1
    
    return rssf

"""
Descrição: Função principal, responsável por montar a matriz de incidência ponderada inicial, e por chamar as funções de leitura do dataset e início do ciclo.
Entrada: Nada.
Saída: Nada.
"""
def main():
    resp = input("Qual dataset você deseja ler? ")
    rssf = leCoordenadas(resp) #Dicionário com as informações da rede.

    """ Montando a matriz inicial. """
    matriz = np.zeros((rssf["tam"] + 1, rssf["tam"] + 1), dtype="float64")

    print("\nModelagens: 1 - Distância; 2 - Clusters")
    resp = int(input("Sua resposta: "))
    if resp == 1:
        """ Atualizando os elementos do dicionário para serem objetos da classe Sensor """
        for sensor in range(1, rssf["tam"] + 1):
            rssf[sensor] = dist.Sensor(sensor, rssf[sensor][0], rssf[sensor][1])

        """ Calculando os vizinhos de cada sensor e atualizando a matriz """
        for i in range(1, rssf["tam"] + 1):
            rssf[i].calcVizinhos(rssf)
            for vizinho in rssf[i].vizinhos:
                if vizinho == "ERB":
                    matriz[i][0] = rssf[i].vizinhos[vizinho]
                else:
                    matriz[i][vizinho] = rssf[i].vizinhos[vizinho]

        """ Chamando os métodos """
        print("Métodos: 1 - Menor Caminho; 2 - Menor Caminho com Salto; 3 - Árvore Geradora Mínima")
        resp = int(input("Sua resposta: "))
        if resp == 1:
            print(dist.startMC(matriz, rssf))
        elif resp == 2:
            print(dist.startMS(matriz, rssf))
        else:
            print(dist.startAG(matriz, rssf))
    else:
        """ Montando as regiões de cada cluster e informando qual sensor será o cluster. """
        clusters, regioes = clu.montaKMeans(rssf)

        """ Atualizando o dicionário com as informações da rede, para ele começar a guardar os objetos. """
        #Percorrendo as regiões.
        for regiao in regioes:
            #Como as chaves do dicionário regiões começam de 0 até o número de regiões - 1, usamos ele para acessar o cluster correspondente na lista de cluster.
            rssf[clusters[regiao]] = clu.Cluster(clusters[regiao], rssf[clusters[regiao]][0], rssf[clusters[regiao]][1]) #Montando objeto cluster.
            #Percorrendo os sensores dessa região.
            for sensor in regioes[regiao]:
                #O cluster também está nessa lista, por isso temos que verificar.
                if sensor != clusters[regiao] - 1:
                    rssf[sensor + 1] = clu.Sensor(sensor + 1,rssf[sensor + 1][0],rssf[sensor + 1][1], clusters[regiao]) #Montando objeto sensor.
        
        """ Atualizando os vizinhos de cada cluster e atualizando a matriz. """
        for cluster in range(len(clusters)):
            rssf[clusters[cluster]].calcVizinhos(rssf, regioes[cluster], clusters)
            for vizC in rssf[clusters[cluster]].clustersViz:
                if vizC == "ERB":
                    matriz[clusters[cluster]][0] = rssf[clusters[cluster]].clustersViz[vizC]
                else:
                    matriz[clusters[cluster]][vizC] = rssf[clusters[cluster]].clustersViz[vizC]

        """ Chamando os métodos """
        print("Métodos: 1 - Menor Caminho; 2 - Menor Caminho com Salto; 3 - Árvore Geradora Mínima")
        resp = int(input("Sua resposta: "))
        if resp == 1:
            print(clu.startMC(matriz, rssf, clusters))
        elif resp == 2:
            print(clu.startMS(matriz, rssf, clusters))
        else:
            print(clu.startAG(matriz, rssf, clusters))


if __name__ == "__main__":
    main()

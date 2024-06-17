import numpy as np
from Metodos import metodos as met
from Modelagens import distancia as dist, clusters as clu


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
    rssf = leCoordenadas() #Dicionário com as informações da rede.
    
    """ Imprimindo informações --> Remover quando estiver finalizado. """
    #print(f"Tamanho: {rssf["tam"]}")
    #print(f"Estação rádio-base: {rssf["ERB"]}")
    #for i in range(1, rssf["tam"] + 1):
    #    print(f"{rssf[i].identidade} - X: {rssf[i].x}, Y: {rssf[i].y}")

    print("\nModelagens: 1 - Distância; 2 - Clusters")
    resp = int(input("Sua resposta: "))
    if resp == 1:
        """ Atualizando os elementos do dicionário para serem objetos da classe Sensor """
        for sensor in range(1, rssf["tam"] + 1):
            rssf[sensor] = dist.Sensor(sensor, rssf[sensor][0], rssf[sensor][1])
        
        """ Montando a matriz inicial. """
        matriz = np.zeros((rssf["tam"] + 1, rssf["tam"] + 1), dtype="float64")

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
            dist.startMC(matriz, rssf)
        elif resp == 2:
            dist.startMS(matriz, rssf)
        else:
            dist.startAG(matriz, rssf)
    else:
        #Montando as regiões de cada cluster e informando qual sensor será o cluster.
        clusters, regioes = clu.montaKMeans(rssf)
        print(clusters)
        print(regioes)
        for regiao in regioes:
            x = rssf[clusters[regiao]][0]
            y = rssf[clusters[regiao]][1]
            rssf[clusters[regiao]] = clu.Cluster(clusters[regiao], x, y)
            for sensor in regioes[regiao]:
                if sensor != clusters[regiao] - 1:
                    x = rssf[sensor + 1][0]
                    y = rssf[sensor + 1][1]
                    rssf[sensor + 1] = clu.Sensor(sensor + 1, x, y, clusters[regiao])
        for cluster in range(len(clusters)):
            rssf[clusters[cluster]].calcVizinhos(rssf, regioes[cluster], clusters)
        for cluster in clusters:
            print(f"Cluster {rssf[cluster].identidade} - {rssf[cluster].x} - {rssf[cluster].y}")
            print(rssf[cluster].clustersViz)
            print("Sensores: ")
            for sensor in rssf[cluster].sensoresViz:
                print(f"Sensor {rssf[sensor].identidade} - {rssf[sensor].x} - {rssf[sensor].y} - {rssf[cluster].sensoresViz[sensor]}")
            print()


if __name__ == "__main__":
    main()

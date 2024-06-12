import numpy as np
import copy

def dijkstra(matriz, vOrigem, vDestino):
    #Dicionários de custo e rota até o vértice
    custo = {}
    rota = {}
    for i in range(len(matriz)):
        if i == vOrigem:
            custo[i] = 0
            rota[i] = vOrigem
        else:
            custo[i] = -1
            rota[i] = 0
    #Listas de vértices em aberto e fechado
    A = [i for i in range(len(matriz))]
    F = []
    while A:
        #v é o vértice com o menor custo em aberto
        v = A[0]
        for i in A:
            if custo[v] == -1 or (custo[i] != -1 and custo[i] < custo[v]):
                v = i
        F.append(v)
        A.remove(v)
        #N é uma lista com os adjacentes de v em aberto
        N = []
        for i in range(len(matriz)):
            if matriz[v][i] > 0 and i not in F:
                N.append(i)
        #Setando os custos em relação a v e seus adjacentes
        for u in N:
            if custo[v] + matriz[v][u] < custo[u] or custo[u] == -1:
                custo[u] = custo[v] + matriz[v][u]
                rota[u] = v
    menorC = []
    menor = vDestino
    while menor != vOrigem:
        menorC.append(menor)
        menor = rota[menor]
    menorC.append(menor)
    menorC.reverse()
    print(menorC, custo[vDestino])

def bellmanFord(matriz, vOrigem, vDestino):
    matriz = np.array(matriz)
    custo = dict([i, 1000] for i in range(len(matriz)))
    custo[vOrigem] = 0
    rota = dict([i, 0] for i in range(len(matriz)))
    for loop in range(len(matriz)):
        for i in range(vOrigem, len(matriz)):
            for u in range(len(matriz)):
                if matriz[i][u] != -1:
                    if custo[u] > custo[i] + matriz[i][u]:
                        custo[u] = custo[i] + matriz[i][u]
                        rota[u] = i
    menorC = [vDestino]
    menor = vDestino
    while menor != vOrigem:
        menorC.insert(0, rota[menor])
        menor = rota[menor]
    print(menorC, custo[vDestino])

def floydWarshall(matriz):
    D = copy.deepcopy(matriz)
    n = len(matriz)

    for i in range(len(D)):
        for j in range(len(D)):
            if D[i][j] == -1:
                D[i][j] = 9999

    for k in range(n):
        for v in range(n):
            for u in range(n):
                    D[v][u] = min(D[v][u], D[v][k] + D[k][u])

    print(D)

if __name__ == "__main__":
    matriz = [[0, 3, 8, 4, 0, 10], [3, 0, 0, 6, 0, 0], [8, 0, 0, 0, 7, 0], [4, 6, 0, 0, 1, 3], [0, 0, 7, 1, 0, 1], [10, 0, 0, 3, 1, 0]]
    matriz = np.array(matriz).reshape(6,6)
    dijkstra(matriz, 2, 1)
    bellmanFord(matriz, 2, 1)
    floydWarshall([[-1,6,-1,7,-1], [-1,-1,5,8,-4], [-1,-2,-1,-1,-1], [-1,-1,-3,-1,9], [2,-1,7,-1,-1]])
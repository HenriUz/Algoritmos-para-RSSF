import numpy as np


""" ----------- MENOR CAMINHO ----------- """


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


""" ----------- ÁRVORE GERADORA MÍNIMA ----------- """


"""
Descrição: Identifica qual é o vértice principal do conjunto, para otimizar a busca, é utilizada a compressão de caminho, que faz todos os vértices
apontarem para o vértice principal.
Entrada: Vértice e a lista de vértices principais.
Saída: Vértice principal do vértice informado.
"""
def Find_Set(vertice, verticePrinc):
    #Se o vertice principal for diferente do vértice informado, busca no próximo. (Somente os vértices principais apontam para eles mesmo).
    if verticePrinc[vertice] != vertice:
        #Aplicando a compressão de caminhos. No fim, cada vértice presente em um sub-conjunto irá apontar para o mesmo vértice principal.
        verticePrinc[vertice] = Find_Set(verticePrinc[vertice], verticePrinc)
    return verticePrinc[vertice]

"""
Descrição: Une dois conjuntos com base no valor que cada um deles contém.
Entrada: Os dois vértices que se deseja saber o sub-conjunto, a lista de vértices principais, e a lista de valores.
Saída: Nada
"""
def Union_Set(vertice_1, vertice_2, verticePrinc, valorVertice):
    principal_1 = Find_Set(vertice_1, verticePrinc)
    principal_2 = Find_Set(vertice_2, verticePrinc)
    #Não é necessário verificar se os dois são iguais, pois a kruskal já verifica.
    #Se o sub-conjunto tiver valor menor, ele irá apontar para o outro subconjunto, para evitar que o tamanho fique muito grande.
    if valorVertice[principal_1] < valorVertice[principal_2]:
        verticePrinc[principal_1] = principal_2
    elif valorVertice[principal_1] > valorVertice[principal_2]:
        verticePrinc[principal_2] = principal_1
    else:
        #Se os valores forem iguais, por padrão o sub-conjunto dois irá se unir ao 1, e aumentamos o tamanho de 1.
        verticePrinc[principal_2] = principal_1
        valorVertice[principal_1] += 1
    return

"""
Descrição: Obtém as arestas da árvore geradora mínima partir da matriz de adjacências de um grafo ponderado através do algoritmo de Kruskal.
Entrada: Matriz de adjacência ponderada; Dicionário com as informações da rede; Tamanho da árvore (na modelagem distância é o número de elementos da matriz - 1, na modelagem cluster é 
    a quantidade de clusters).
Saída: Matriz de adjacência da árvore.
"""
def kruskal(matriz, rssf, tamanho):
    #Variáveis principais.
    T = [] #Conjunto de arestas da árvore mínima
    H = [] #Conjunto de todas as arestas ordenadas por peso
    verticePrinc = [] #Cada vértice tem sua posição na lista, o valor dessa posição indica o vértice principal do sub-conjunto que o vértice está.
    valorVertice = [] #Cada vértice tem sua posição na lista, serve para identificar qual sub-conjunto é maior e assim ajudar na união de dois sub-conjuntos.
    arvore = np.zeros((rssf["tam"] + 1, rssf["tam"] + 1), dtype="int64") #Matriz que representa a árvore mínima.

    #Inicializando as variáveis.
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            if matriz[i][j] > 0:
                H.append((i,j,matriz[i][j]))
        #Inicializando verticePrinc e valorVertice aqui, sem ser pythonico para evitar a quantidade de loops desnecessários.
        verticePrinc.append(i) #Inicialmente cada vértice é o principal do seu próprio sub-conjunto
        valorVertice.append(0) #Inicialmente os valores são zeros
    H = sorted(H, key=lambda item: item[2]) #Ordenando as arestas pelo item 2 (o peso)

    #Formando a árvore mínima.
    while len(T) < tamanho:
        for aresta in H:
            #Se o principal de dois vértices forem o mesmo, significa que eles estão no mesmo sub-conjunto, e adicionar uma aresta entre eles formaria ciclo.
            if Find_Set(aresta[0], verticePrinc) != Find_Set(aresta[1], verticePrinc):
                T.append((aresta[0], aresta[1]))
                arvore[aresta[0]][aresta[1]] = 1
                arvore[aresta[1]][aresta[0]] = 1
                Union_Set(aresta[0], aresta[1], verticePrinc, valorVertice) #Unindo os dois sub-conjuntos
    return arvore

"""
Descrição: Função recursiva, responsável por encontrar o caminho de um vértice de origem até o vértice de destino usando a Depth-First Search.
Entrada: Dicionário de adjacências; Vértice de origem; Vértice de destino; Caminho montado (somente na recursão); Dicionário de vértices analisados 
    (somente na recursão).
Saída: O caminho do vértice de destino até o de origem.
"""
def dfs(listaAdj, vOrigem, vDestino, caminho=None, analisado=None):
    """ Variáveis principais """
    if caminho is None:
        caminho = [] #Caminho
    if analisado is None:
        analisado = dict([i, 0] for i in listaAdj)  #Dicionário de vértices analisados (1 - analisado; 0 - não analisado).
    
    caminho.append(vOrigem)
    analisado[vOrigem] = 1
    
    #Vértice de destino encontrado, então retornamos o caminho.
    if vOrigem == vDestino:
        return caminho

    #Percorrendo os vizinhos.
    for vizinho in listaAdj[vOrigem]:
        #Se o vizinho não foi analisado, encontre o caminho do vizinho.
        if analisado[vizinho] == 0:
            result = dfs(listaAdj, vizinho, vDestino, caminho, analisado)
            #Se o caminho foi encontrado, retorna ele.
            if result:
                return result
    
    #Se o caminho não foi encontrado, retira o elemento atual do caminho e retorna nada.
    caminho.pop()
    return []

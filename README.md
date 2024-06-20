# Algoritmos para RSSF
Este repositório contém os algoritmos, em python, que simulam uma rede de sensores sem fio e testam qual é o método mais eficiente.

# Arquivos
`main.py` -> Código em python que lê os datasets e chama o método e modelagem informado.

Metodos:
- `metodos.py` -> Código em python contendo os métodos utilizados (dijkstra, kruskal, ...).

Modelagens:
- `distancia.py` -> Código em python com as funções responsáveis por iniciar os ciclos com as diferentes modelagens, Na modelagem de Distâncias.
- `cluster.py` -> Código em python com as funções responsáveis por iniciar os ciclos com as diferentes modelagens, na modelagem de Clusters

Datasets:
Os datasets que estão sendo usados para a realização dos testes, a primeira linha de cada um indica a quantidade e a segunda é a coordenada da estação rádio-base.

- `Rede 50.txt`
- `Rede 100.txt`
- `Rede 200.txt`
- `Rede 400.txt`

## Resultados:

### Modelagem por Distância
| Ciclos     | Caminho Mínimo | Caminho Mínimo com Salto | Arvore Geradora Mínima |
|------------|----------------|--------------------------|------------------------|
| 50 Motes   | 7140           | 11580                    | 5740                   |
| 100 Motes  | 5260           | 10720                    | 3460                   |
| 200 Motes  | 9280           | 10480                    | 1420                   |
| 400 Motes  | 3880           | 10020                    | 1560                   |

### Modelagem por Cluster
| Ciclos     | Caminho Mínimo | Caminho Mínimo com Salto | Arvore Geradora Mínima |
|------------|----------------|--------------------------|------------------------|
| 50 Motes   | 16460          | 23760                    | 13780                  |
| 100 Motes  | 16440          | 21580                    | 13500                  |
| 200 Motes  | 17760          | 17880                    | 13840                  |
| 400 Motes  | 15740          | 16200                    | 8400                   |

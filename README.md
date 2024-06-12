# Algoritmos para RSSF
Este repositório contém os algoritmos, em python, que simulam uma rede de sensores sem fio e testam qual é o método mais eficiente.

## Arquivos
`main.py` -> Código em python que lê os datasets e chama o método e modelagem informado.

Metodos:
- `metodos.py` -> Código em python contendo os métodos utilizados (dijkstra, kruskal, ...).

Modelagens:
- `distancia.py` -> Código em python com as funções responsáveis por iniciar os ciclos com os diferentes métodos. Na modelagem de distâncias.

Datasets:
Os datasets que estão sendo usados para a realização dos testes, a primeira linha de cada um indica a quantidade e a segunda é a coordenada da estação rádio-base.

- `Rede 50.txt`
- `Rede 100.txt`
- `Rede 200.txt`
- `Rede 400.txt`

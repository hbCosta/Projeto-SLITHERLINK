#!/usr/bin/env python3
# slitherlink.py: Template para implementação do projeto de Inteligência Artificial 2025/2026.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import random, copy
from sys import stdin
from collections import defaultdict

import utils
from utils import *

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class SlitherlinkState:
    state_id = 0


    def __init__(self, board):
        self.board = board
        self.id = SlitherlinkState.state_id
        SlitherlinkState.state_id += 1
    
    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe

class Board:
    """Representação interna de um tabuleiro de Slitherlink."""
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.columns = len(grid[0])

        # Inicializar arestas
        self.edges = {}
        for row in range(self.rows+1):
            for col in range(self.columns):
                self.edges[('h', row, col)] = 0
        for row in range(self.rows):
            for col in range(self.columns + 1):
                self.edges[('v', row, col)] = 0
        

        # Define que céculas com 0 não pode ter arestas 
        for row in range(self.rows):
            for col in range(self.columns):
                if self.grid[row][col] == 0:
                    for edge in self.get_cell_edges(row, col):
                        self.edges[edge] = -1


    def copy(self):
        new_board = Board.__new__(Board)
        new_board.grid = self.grid
        new_board.rows = self.rows
        new_board.columns = self.columns
        new_board.edges = dict(self.edges)
        return new_board


    def adjacent_cell(self, cell:tuple) -> list:
        """Devolve uma lista das células que fazem
        fronteira com a célula enviada no argumento"""
        row, col = cell
        adjacentes = []
        if row > 0:
            adjacentes.append((row-1, col))
        if row < self.rows -1:
            adjacentes.append((row+1, col))
        if col > 0:
            adjacentes.append((row, col-1))
        if col < self.columns -1:
            adjacentes.append((row, col+1))
        return adjacentes

        #TODO
        pass

    def get_cell_edges(self, row:int, column:int) -> list:
        """Devolve os arestas da célula enviada no argumento"""
        arestas = [
            ('h', row, column),
            ('h', row + 1, column),
            ('v', row, column),
            ('v', row, column + 1)
        ]
        return arestas

        #TODO
        pass

    def get_active_edges(self, row:int, column:int) -> list:
        """Devolve o número de arestas ativas"""
        return sum(1 for e in self.get_cell_edges(row, column) if self.edges[e] ==1)


    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        Por exemplo:
            $ python3 pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split()
        """
        grid = [
            [int(val) if val.isdigit() else None for val in line.split()]
            for line in stdin
            if line.strip()
        ]
        return Board(grid)

class Slitherlink(Problem):
    def __init__(self, board: Board, gui=None):
        """O construtor especifica o estado inicial."""
        initial_state = SlitherlinkState(board)
        super().__init__(initial_state)
        self.gui = gui    


    def actions(self, state: SlitherlinkState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        acoes_possiveis = []

        for aresta, valor in state.board.edges.items():
            if valor == 0:
                acoes_possiveis.append((aresta, 1))
                acoes_possiveis.append((aresta, -1))
                return acoes_possiveis

        return acoes_possiveis
         
                    






    def result(self, state: SlitherlinkState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        new_board = state.board.copy()
        aresta, valor = action
        new_board.edges[aresta] = valor
        return SlitherlinkState(new_board)



        

    def goal_test(self, state: SlitherlinkState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    
    # TESTES/DEBUG - a remover quando o projeto estiver implementado
    board = Board.parse_instance()
    print("--- TESTE 1: LEITURA DO TABULEIRO ---\n")
    print(f"Tabuleiro lido: {board.rows} linhas x {board.columns} colunas")
    print("Conteúdo: \n")
    for linha in board.grid:
        print(f"{linha}")

    print("\n--- TESTE 2: CÉLULAS ADJACENTES ---\n")
    print("Vizinhos de (0, 0):", board.adjacent_cell((0, 0)))
    print("Vizinhos de (2, 2):", board.adjacent_cell((2, 2)))

    ultima_linha = board.rows - 1
    ultima_coluna = board.columns - 1
    print("Vizinhos de (ultima_linha, ultima_coluna):", board.adjacent_cell((ultima_linha, ultima_coluna)))
    print("\n")

    print("\n--- TESTE 3: ARESTAS DA CÉLULA ---")
    for aresta in board.get_cell_edges(2, 1):
        print(" ->",aresta)
    
    print("\n--- TESTE 4: ESTADO DAS ARESTAS ---")
    print("Arestas da célula (0,0) ")
    for aresta in board.get_cell_edges(0, 0):
        print(f"  {aresta} -> {board.edges[aresta]}") 

    print("\nArestas da célula (0,2)")
    for aresta in board.get_cell_edges(0, 2):
        print(f"  {aresta} -> {board.edges[aresta]}") 

    print("\nArestas ativas em (0,0):", board.get_active_edges(0, 0))  # deve ser 0
    print("Arestas ativas em (0,2):", board.get_active_edges(0, 2))  # deve ser 0

    print("\n--- TESTE 5: RESULT ---\n")
    problema = Slitherlink(board)
    acoes = problema.actions(problema.initial)
    print(f"Ações possíveis: {acoes}")

    novo_estado = problema.result(problema.initial, acoes[0])
    aresta,valor = acoes[0]
    
    print(f"Aresta {aresta} no estado inicial: {problema.initial.board.edges[aresta]}")  # deve ser 0
    print(f"Aresta {aresta} no novo estado: {novo_estado.board.edges[aresta]}")           # deve ser 1

    # Garante que o estado inicial não foi alterado
    print(f"Estado inicial não foi modificado: {problema.initial.board.edges[aresta] == 0}")  # deve ser True
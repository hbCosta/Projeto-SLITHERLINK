#!/usr/bin/python3
# slitherlink.py: Template para implementação do projeto de Inteligência Artificial 2025/2026.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 76:
# 106372 Diogo Geria
# 119449 Humberto Costa

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


class Board:
    """Representação interna de um tabuleiro de Slitherlink."""
    
    def __init__(self, grid):

        self.grid = grid
        self.rows = len(grid)
        self.columns = len(grid[0])
        
        self.edges = {}
        for row in range(self.rows+1):
            for col in range(self.columns):
                self.edges[('h', row, col)] = 0
        for row in range(self.rows):
            for col in range(self.columns + 1):
                self.edges[('v', row, col)] = 0
                
                
        for row in range(self.rows):
            for col in range(self.columns):
                if self.grid[row][col] == 0:
                    for edge in self.get_cell_edges(row, col):
                        self.edges[edge] = -1
                        
        self.apply_basic_inference()
                        
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


    def get_cell_edges(self, row:int, column:int) -> list:
        """Devolve os arestas da célula enviada no argumento"""
        arestas = [
            ('h', row, column),
            ('v', row, column+1),
            ('h', row+1, column),
            ('v', row, column)
        ]
        return arestas

    def get_active_edges(self, row:int, column:int) -> list:
        """Devolve o número de arestas ativas"""
        return sum(1 for e in self.get_cell_edges(row, column) if self.edges[e] ==1)
    
    
                            
    def get_vertex_edges(self, vertex: tuple) -> list:
        """Devolve as arestas que tocam num determinado vértice, para depois se avaliar o grau"""

        row, col = vertex
        edges = []
    
        
        if col > 0:
            edges.append(('h', row, col - 1))
    
        
        if col < self.columns:
            edges.append(('h', row, col))
    
       
        if row > 0:
            edges.append(('v', row - 1, col))
    
       
        if row < self.rows:
            edges.append(('v', row, col))
    
        return edges
    
    
    def edge_cells(self, edge):
        """Devolve as células tocadas por uma aresta."""

        kind, row, col = edge
    
        cells = []
    
        if kind == 'h':
    
            if row > 0:
                cells.append((row - 1, col))
    
            if row < self.rows:
                cells.append((row, col))
    
        else:  
    
            if col > 0:
                cells.append((row, col - 1))
    
            if col < self.columns:
                cells.append((row, col))
    
        return cells
    
    
    def edge_vertices(self, edge):
        """Devolve os dois vértices de uma aresta."""

        kind, row, col = edge
    
        if kind == 'h':
    
            return [
                (row, col),
                (row, col + 1)
            ]
    
        return [
            (row, col),
            (row + 1, col)
        ]
    
    
    def apply_local_inference(self, changed_edges):
        """Aplica inferência apenas na zona afetada."""

        cells_to_check = set()
        vertices_to_check = set()

        for edge in changed_edges:
    
            cells_to_check.update(
                self.edge_cells(edge)
            )
    
            vertices_to_check.update(
                self.edge_vertices(edge)
            )
    
        while cells_to_check or vertices_to_check:
    
    
            while cells_to_check:
    
                row, col = cells_to_check.pop()
    
                value = self.grid[row][col]
    
                if value is None:
                    continue
    
                edges = self.get_cell_edges(row, col)
    
                active = [
                    e for e in edges
                    if self.edges[e] == 1
                ]
    
                unknown = [
                    e for e in edges
                    if self.edges[e] == 0
                ]
    
             
                if len(active) > value:
                    return False
    
                if len(active) + len(unknown) < value:
                    return False
    
                new_changed = []
    
              
                if len(active) == value:
    
                    for e in unknown:
    
                        self.edges[e] = -1
                        new_changed.append(e)
    
              
                elif len(active) + len(unknown) == value:
    
                    for e in unknown:
    
                        self.edges[e] = 1
                        new_changed.append(e)
    
                
                for e in new_changed:
    
                    cells_to_check.update(
                        self.edge_cells(e)
                    )
    
                    vertices_to_check.update(
                        self.edge_vertices(e)
                    )
    
    
            while vertices_to_check:
    
                vertex = vertices_to_check.pop()
    
                vertex_edges = self.get_vertex_edges(vertex)
    
                active = [
                    e for e in vertex_edges
                    if self.edges[e] == 1
                ]
    
                unknown = [
                    e for e in vertex_edges
                    if self.edges[e] == 0
                ]
    
                # Contradição: ramificação
                if len(active) > 2:
                    return False
    
                # Contradição: ponta solta
                if len(active) == 1 and len(unknown) == 0:
                    return False
    
                new_changed = []
    
                if len(active) == 2:
    
                    for e in unknown:
    
                        self.edges[e] = -1
                        new_changed.append(e)
    
                elif len(active) == 1 and len(unknown) == 1:
    
                    self.edges[unknown[0]] = 1
                    new_changed.append(unknown[0])
    
                elif len(active) == 0 and len(unknown) == 1:
    
                    self.edges[unknown[0]] = -1
                    new_changed.append(unknown[0])
    
                for e in new_changed:
    
                    cells_to_check.update(
                        self.edge_cells(e)
                    )
    
                    vertices_to_check.update(
                        self.edge_vertices(e)
                    )
    
        return True
        
    
    def apply_basic_inference(self):
        """Aplicar algumas inferências para tornarmos a procura mais leve"""
    
        changed = True
    
        while changed:
            changed = False
    
            # Inferência pelas células numeradas
            for row in range(self.rows):
                for col in range(self.columns):
    
                    value = self.grid[row][col]
    
                    if value is None:
                        continue
    
                    edges = self.get_cell_edges(row, col)
    
                    active = [e for e in edges if self.edges[e] == 1]
                    unknown = [e for e in edges if self.edges[e] == 0]
                    
                    if len(active) > value: 
                        return False 
                    
                    if len(active) + len(unknown) < value:
                        return False

            
                    if len(active) == value:
                        for e in unknown:
                            self.edges[e] = -1
                            changed = True
    
                 
                    elif len(active) + len(unknown) == value:
                        for e in unknown:
                            self.edges[e] = 1
                            changed = True
    
            # Inferência pelos vértices - porque não podem haver interrupções/ramificações
            for row in range(self.rows + 1):
                for col in range(self.columns + 1):
    
                    vertex_edges = self.get_vertex_edges((row, col))
    
                    active = [e for e in vertex_edges if self.edges[e] == 1]
                    unknown = [e for e in vertex_edges if self.edges[e] == 0]
                    
                    if len(active) > 2:
                        return False
                    
                    if len(active) == 1 and len(unknown) == 0:
                        return False
    
                    
                    if len(active) == 2:
                        for e in unknown:
                            self.edges[e] = -1
                            changed = True
    
                   
                    elif len(active) == 1 and len(unknown) == 1:
                        self.edges[unknown[0]] = 1
                        changed = True
    
                   
                    elif len(active) == 0 and len(unknown) == 1:
                        self.edges[unknown[0]] = -1
                        changed = True
                        
        return True
    
    
                        
    
    def has_single_loop(self):
        active_edges = [e for e, value in self.edges.items() if value == 1]
    
        if not active_edges:
            return False
    
        def edge_vertices(edge):
            kind, row, col = edge
    
            if kind == 'h':
                return (row, col), (row, col + 1)
    
            return (row, col), (row + 1, col)
    
        graph = {}
    
        for edge in active_edges:
            v1, v2 = edge_vertices(edge)
    
            if v1 not in graph:
                graph[v1] = []
    
            if v2 not in graph:
                graph[v2] = []
    
            graph[v1].append(v2)
            graph[v2].append(v1)
    
        for vertex in graph:
            if len(graph[vertex]) != 2:
                return False
    
        start = list(graph.keys())[0]
        visited = set()
        stack = [start]
    
        while stack:
            vertex = stack.pop()
    
            if vertex in visited:
                continue
    
            visited.add(vertex)
    
            for neighbor in graph[vertex]:
                if neighbor not in visited:
                    stack.append(neighbor)
    
        return len(visited) == len(graph)
    
        
    def print_instance(self):
        """Imprime o tabuleiro no formato de output pedido."""

        for row in range(self.rows):
    
            line = []
    
            for col in range(self.columns):
    
                edges = self.get_cell_edges(row, col)
    
                values = []
    
                for e in edges:
    
                    if self.edges[e] == 1:
                        values.append("1")
    
                    else:
                        values.append("0")
    
                line.append("".join(values))
    
            print(" ".join(line))
            


    @staticmethod
    def parse_instance():
        
        grid = [
            [int(val) if val.isdigit() else None for val in line.split()]
            for line in stdin
            if line.strip()
        ]
        return Board(grid)

    
def combinations_k(items, k):
    """Devolve todas as combinações de tamanho k da lista items."""

    if k == 0:
        return [[]]

    if len(items) < k:
        return []

    first = items[0]
    rest = items[1:]

    with_first = combinations_k(rest, k - 1)
    with_first = [[first] + comb for comb in with_first]

    without_first = combinations_k(rest, k)

    return with_first + without_first


class Slitherlink(Problem):
    def __init__(self, board: Board, gui=None):
        initial_state = SlitherlinkState(board)
        super().__init__(initial_state)
        self.gui = gui
        
        
    def valid_action(self, board, action):
        """Testa se uma ação gera imediatamente um estado inválido."""
    
        new_board = board.copy()
    
        changed_edges = []
    
        for edge, value in action.items():
    
            if new_board.edges[edge] != 0 and new_board.edges[edge] != value:
                return False
    
            new_board.edges[edge] = value
            changed_edges.append(edge)
    
        return new_board.apply_local_inference(changed_edges)
    

    def actions(self, state: SlitherlinkState):
        """Gera ações a partir da célula numerada mais restritiva."""

        board = state.board
        best_actions = None
    
        for row in range(board.rows):
            for col in range(board.columns):
    
                value = board.grid[row][col]
    
                if value is None:
                    continue
    
                edges = board.get_cell_edges(row, col)
    
                active = [
                    e for e in edges
                    if board.edges[e] == 1
                ]
    
                unknown = [
                    e for e in edges
                    if board.edges[e] == 0
                ]
    
                missing = value - len(active)
    
                # Estado impossível
                if missing < 0:
                    return []
    
                if missing > len(unknown):
                    return []
    
                # Nada para decidir nesta célula
                if len(unknown) == 0:
                    continue
    
                cell_actions = []
    
                for chosen_edges in combinations_k(unknown, missing):
    
                    action = {}
    
                    for e in unknown:
                        if e in chosen_edges:
                            action[e] = 1
                        else:
                            action[e] = -1
    
                    if self.valid_action(board, action):
                        cell_actions.append(action)
    
                
                if (
                    cell_actions and
                    (
                        best_actions is None or
                        len(cell_actions) < len(best_actions)
                    )
                ):
                    best_actions = cell_actions
    
        if best_actions is not None:
            return best_actions
    
        
        for edge, value in board.edges.items():
    
            if value == 0:
    
                actions = [
                    {edge: 1},
                    {edge: -1}
                ]
    
                return [
                    action
                    for action in actions
                    if self.valid_action(board, action)
                ]
    
        return []
        
    
    def result(self, state: SlitherlinkState, action):
        """Aplica uma ação e devolve o novo estado."""

        new_board = state.board.copy()
    
        changed_edges = []
    
        for edge, value in action.items():
    
            new_board.edges[edge] = value
            changed_edges.append(edge)
    
        new_board.apply_local_inference(changed_edges)
    
        return SlitherlinkState(new_board)
        

    def goal_test(self, state: SlitherlinkState):
        board = state.board
    
    
        for row in range(board.rows):
            for col in range(board.columns):
    
                value = board.grid[row][col]
    
                if value is not None:
                    if board.get_active_edges(row, col) != value:
                        return False
    
    
        for row in range(board.rows + 1):
            for col in range(board.columns + 1):
    
                vertex_edges = board.get_vertex_edges((row, col))
                active = [e for e in vertex_edges if board.edges[e] == 1]
    
                if len(active) not in [0, 2]:
                    return False
    
       
        active_edges = [e for e, value in board.edges.items() if value == 1]
    
        if len(active_edges) == 0:
            return False
    
        # Verificar se as arestas ativas formam um único ciclo
        return board.has_single_loop()
    
    

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
    

    # Ler tabuleiro
    board = Board.parse_instance()

    # Criar problema
    problem = Slitherlink(board)

    # Resolver
    goal_node = depth_first_tree_search(problem)

    # Verificar se encontrou solução
    if goal_node is not None:

        # Imprimir solução
        goal_node.state.board.print_instance()

    else:
        print("No solution found")






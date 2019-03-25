import argparse
import numpy as np
import operator
from random import randint 
from node import Node

class Game:

	def __init__(self, dimension):
		self.final_board = self.initial_config(dimension)
		self.dimension = dimension
		self.board = self.shuffle(self.final_board.copy())

	def initial_config(self, dimension):
		line = []
		cont = 1
		for i in range(0, dimension):
			line.append(np.arange(cont, dimension+cont))
			cont += dimension
		line[dimension-1][dimension-1] = 0
		m = np.matrix(line)

		return m

	def move_up(self, m):
		i, j = np.where(m == 0)
		if (i!=0):
			m[i,j] = m[i-1,j]
			m[i-1,j] = 0
		return m

	def move_down(self, m):
		i, j = np.where(m == 0)
		if (i!=dimension-1):
			m[i,j] = m[i+1,j]
			m[i+1,j] = 0
		return m
		
	def move_left(self, m):
		i, j = np.where(m == 0)
		if (j!=0):
			m[i,j] = m[i,j-1]
			m[i,j-1] = 0
		return m

	def move_right(self, m):
		i, j = np.where(m == 0)
		if (j!=dimension-1):
			m[i,j] = m[i,j+1]
			m[i,j+1] = 0
		return m

	def shuffle(self, m):
		for i in range(0,25):
			func = randint(0,3)
			if(func==0):
				m = self.move_up(m)
			elif(func==1):
				m = self.move_down(m)
			elif(func==2):
				m = self.move_left(m)
			elif(func==3):
				m = self.move_right(m)
		return m

	def read_solution(self, node):
		stack = []
		while node.father != None:
			stack.append(node.value)
			node = node.father
		stack.append(node.value)

		while stack:
			print(stack.pop())
		
	def verify_node(self, actual_node):
		return np.array_equal(actual_node, self.final_board)

	#Busca em profundidade com recursão
	"""
	def DFS(self, node, level):
		
		if self.verify_node(node.value):
			return node
			
		node_up = self.move_up(node.value.copy())
		node_down = self.move_down(node.value.copy())
		node_right = self.move_right(node.value.copy())
		node_left = self.move_left(node.value.copy())
		
		if (not np.array_equal(node_up, node.value)):
			node.insert_up(node_up, node, node.level+1)
			return self.DFS(node.up, node.level+1)
		if (not np.array_equal(node_down, node.value)):
			node.insert_down(node_down, node, node.level+1)
			return self.DFS(node.down, node.level+1)
		if (not np.array_equal(node_right, node.value)):
			node.insert_right(node_right, node, node.level+1)
			return self.DFS(node.right, node.level+1)
		if (not np.array_equal(node_left, node.value)):
			node.insert_left(node_left, node, node.level+1)
			return self.DFS(node.left, node.level+1)
	"""	

	#Busca em profundidade
	def DFS(self, node, level):
		
		to_visit = [node]

		while to_visit:
			node = to_visit.pop(0)

			if self.verify_node(node.value):
				return node

			node_up = self.move_up(node.value.copy())
			node_down = self.move_down(node.value.copy())
			node_right = self.move_right(node.value.copy())
			node_left = self.move_left(node.value.copy())
			
			if (not np.array_equal(node_up, node.value)):
				node.insert_up(node_up, node, node.level+1)
				to_visit.insert(0, node.up)
			if (not np.array_equal(node_down, node.value)):
				node.insert_down(node_down, node, node.level+1)
				to_visit.insert(0, node.down)
			if (not np.array_equal(node_right, node.value)):
				node.insert_right(node_right, node, node.level+1)
				to_visit.insert(0, node.right)
			if (not np.array_equal(node_left, node.value)):
				node.insert_left(node_left, node, node.level+1)
				to_visit.insert(0, node.left)

	#Busca em aprofundamento iterativo
	def IDDS(self, node_root, level):
		
		to_visit = [node_root]

		while to_visit:
			node = to_visit.pop(0)
		
			if self.verify_node(node.value):
				return node

			if node.level < level: 
				node_up = self.move_up(node.value.copy())
				node_down = self.move_down(node.value.copy())
				node_right = self.move_right(node.value.copy())
				node_left = self.move_left(node.value.copy())
				
				if (not np.array_equal(node_up, node.value)):
					node.insert_up(node_up, node, node.level+1)
					to_visit.insert(0, node.up)
				if (not np.array_equal(node_down, node.value)):
					node.insert_down(node_down, node, node.level+1)
					to_visit.insert(0, node.down)
				if (not np.array_equal(node_right, node.value)):
					node.insert_right(node_right, node, node.level+1)
					to_visit.insert(0, node.right)
				if (not np.array_equal(node_left, node.value)):
					node.insert_left(node_left, node, node.level+1)
					to_visit.insert(0, node.left)
	
		return self.IDDS(node_root, level + 1)


	#Busca em amplitude
	def BFS(self, node, level):

		to_visit = [node]
		while to_visit:
			node = to_visit.pop(0)
			
			if self.verify_node(node.value):
				return node
			
			node_up = self.move_up(node.value.copy())
			node_down = self.move_down(node.value.copy())
			node_right = self.move_right(node.value.copy())
			node_left = self.move_left(node.value.copy())
			
			if (not np.array_equal(node_up, node.value)):
				node.insert_up(node_up, node, node.level+1)
				to_visit.append(node.up)
			if (not np.array_equal(node_down, node.value)):
				node.insert_down(node_down, node, node.level+1)
				to_visit.append(node.down)
			if (not np.array_equal(node_right, node.value)):
				node.insert_right(node_right, node, node.level+1)
				to_visit.append(node.right)
			if (not np.array_equal(node_left, node.value)):
				node.insert_left(node_left, node, node.level+1)
				to_visit.append(node.left)
			
	def out_of_place_heuristic(self, m):
		#Heuritica que indica quantas peças estão fora de lugar
		out_place = m == self.final_board #False where is out place
		return np.size(out_place) - np.count_nonzero(out_place) #return the sum of False values

	def manhattan_distance_heuristic(self, m):
		distance = 0
		
		for i in range(0, dimension):
			for j in range(0, dimension):
				num = m[i,j]
				if num != 0:
					i_final, j_final = np.where(self.final_board == num)
					distance += abs(i-i_final) + abs(j-j_final)
			
		return int(distance)
	
	def calculate_heuristic(self, node, heuristic):
		#Heuristica 1 para peças fora do lugar e heurística 2 para distancia de manhattan
		if heuristic==1:
			h = self.out_of_place_heuristic(node.value)
		elif heuristic==2:
			h = self.manhattan_distance_heuristic(node.value)
		
		return h

	def A_star(self, node, level, heuristic=1):
		#Heuristica 1 para peças fora do lugar e heurística 2 para distancia de manhattan
		#g = node.level
		#h = funcao heuristica
		#f = g+h
		open_nodes = [[node, node.level + self.calculate_heuristic(node, heuristic)]]
	
		while open_nodes:
			open_nodes = sorted(open_nodes, key=operator.itemgetter(1)) #order by f_score
			node, f_score = open_nodes.pop(0) 
			
			if self.verify_node(node.value):
				return node
			
			#Esse if verifica se os nodos já estão abertos
			if node.up == None and node.down == None and node.right == None and node.left == None: 
				node_up = self.move_up(node.value.copy())
				node_down = self.move_down(node.value.copy())
				node_right = self.move_right(node.value.copy())
				node_left = self.move_left(node.value.copy())
				
				if (not np.array_equal(node_up, node.value)):
					node.insert_up(node_up, node, node.level+1)
					h = self.calculate_heuristic(node.up, heuristic)
					open_nodes.append([node.up, node.level+1 + h])
				if (not np.array_equal(node_down, node.value)):
					node.insert_down(node_down, node, node.level+1)
					h = self.calculate_heuristic(node.down, heuristic)
					open_nodes.append([node.down, node.level+1 + h])
				if (not np.array_equal(node_right, node.value)):
					node.insert_right(node_right, node, node.level+1)
					h = self.calculate_heuristic(node.right, heuristic)
					open_nodes.append([node.right, node.level+1 + h])
				if (not np.array_equal(node_left, node.value)):
					node.insert_left(node_left, node, node.level+1)
					h = self.calculate_heuristic(node.left, heuristic)
					open_nodes.append([node.left, node.level+1 + h])
				
			

if __name__ == '__main__':
	#Le a dimensao (nxn) do jogo
	ap = argparse.ArgumentParser()
	ap.add_argument('-d', "--dimensao", required=True, help="Informe o valor da matriz quadrado para o jogo")
	args = vars(ap.parse_args())	
	dimension = int(args["dimensao"])
	game = Game(dimension)


	print(game.board)
	print()
	board = game.board.copy()
	root = Node(game.board)
	#print(game.out_of_place_heuristic(root.value))
	print(game.manhattan_distance_heuristic(root.value))
	print("BFS")
	final = game.BFS(root,0)
	print(final.level)
	game.read_solution(final)
	#print("DFS")
	game.bord = board
	root = Node(game.board)
	print("DFI")
	final_DFI = game.IDDS(root, 0)
	print(final_DFI.level)
	game.read_solution(final_DFI)
	

	print("A* - pecas fora do lugar")
	game.bord = board
	root = Node(game.board)
	final = game.A_star(root, 1)
	print(final.level)
	game.read_solution(final)
	print("A* - distancia")
	game.bord = board
	root = Node(game.board)
	final = game.A_star(root, 2)
	print(final.level)
	game.read_solution(final)

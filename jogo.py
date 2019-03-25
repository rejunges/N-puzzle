import argparse
import numpy as np
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
		for i in range(0,5):
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
	def DFS(self, node, nivel):
		
		if self.verify_node(node.value):
			return node
			
		node_up = self.move_up(node.value.copy())
		node_down = self.move_down(node.value.copy())
		node_right = self.move_right(node.value.copy())
		node_left = self.move_left(node.value.copy())
		
		if (not np.array_equal(node_up, node.value)):
			node.insert_up(node_up, node, node.nivel+1)
			return self.DFS(node.up, node.nivel+1)
		if (not np.array_equal(node_down, node.value)):
			node.insert_down(node_down, node, node.nivel+1)
			return self.DFS(node.down, node.nivel+1)
		if (not np.array_equal(node_right, node.value)):
			node.insert_right(node_right, node, node.nivel+1)
			return self.DFS(node.right, node.nivel+1)
		if (not np.array_equal(node_left, node.value)):
			node.insert_left(node_left, node, node.nivel+1)
			return self.DFS(node.left, node.nivel+1)
	"""	

	#Busca em profundidade
	def DFS(self, node, nivel):
		
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
				node.insert_up(node_up, node, node.nivel+1)
				to_visit.insert(0, node.up)
			if (not np.array_equal(node_down, node.value)):
				node.insert_down(node_down, node, node.nivel+1)
				to_visit.insert(0, node.down)
			if (not np.array_equal(node_right, node.value)):
				node.insert_right(node_right, node, node.nivel+1)
				to_visit.insert(0, node.right)
			if (not np.array_equal(node_left, node.value)):
				node.insert_left(node_left, node, node.nivel+1)
				to_visit.insert(0, node.left)

	#Busca em aprofundamento iterativo
	def DF_iterative(self, node_root, nivel):
		
		to_visit = [node_root]

		while to_visit:
			node = to_visit.pop(0)
		
			if self.verify_node(node.value):
				return node

			if node.nivel < nivel: 
				node_up = self.move_up(node.value.copy())
				node_down = self.move_down(node.value.copy())
				node_right = self.move_right(node.value.copy())
				node_left = self.move_left(node.value.copy())
				
				if (not np.array_equal(node_up, node.value)):
					node.insert_up(node_up, node, node.nivel+1)
					to_visit.insert(0, node.up)
				if (not np.array_equal(node_down, node.value)):
					node.insert_down(node_down, node, node.nivel+1)
					to_visit.insert(0, node.down)
				if (not np.array_equal(node_right, node.value)):
					node.insert_right(node_right, node, node.nivel+1)
					to_visit.insert(0, node.right)
				if (not np.array_equal(node_left, node.value)):
					node.insert_left(node_left, node, node.nivel+1)
					to_visit.insert(0, node.left)
	
		return self.DF_iterative(node_root, nivel + 1)


	#Busca em amplitude
	def BFS(self, node, nivel):

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
				node.insert_up(node_up, node, node.nivel+1)
				to_visit.append(node.up)
			if (not np.array_equal(node_down, node.value)):
				node.insert_down(node_down, node, node.nivel+1)
				to_visit.append(node.down)
			if (not np.array_equal(node_right, node.value)):
				node.insert_right(node_right, node, node.nivel+1)
				to_visit.append(node.right)
			if (not np.array_equal(node_left, node.value)):
				node.insert_left(node_left, node, node.nivel+1)
				to_visit.append(node.left)
			


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
	print("BFS")
	final = game.BFS(root,0)
	print(final.nivel)
	game.read_solution(final)
	print("DFS")
	game.bord = board
	root = Node(game.board)
	print("DFI")
	final_DFI = game.DF_iterative(root, 0)
	print(final_DFI.nivel)
	game.read_solution(final_DFI)
	

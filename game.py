import argparse
import numpy as np
import operator
import random 
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
		random.seed(30)
		for i in range(0,25):
			func = random.randint(0,3)
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

		cont = 0
		while stack:
			print("Passo " + str(cont) + ":")
			cont +=1
			print(stack.pop())
			print()
		
	def verify_node(self, actual_node):
		return np.array_equal(actual_node, self.final_board)

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
			
	#Heuritica que indica quantas peças estão fora de lugar
	def out_of_place_heuristic(self, m):
		out_place = m == self.final_board 
		return np.size(out_place) - np.count_nonzero(out_place) 

	#Heuritica que indica a distancia de uma peça até seu devido lugar
	def manhattan_distance_heuristic(self, m):
		distance = 0
		
		for i in range(0, dimension):
			for j in range(0, dimension):
				num = m[i,j]
				if num != 0:
					i_final, j_final = np.where(self.final_board == num)
					distance += abs(i-i_final) + abs(j-j_final)
			
		return int(distance)
	
	#Heuristica 1 para peças fora do lugar e heurística 2 para distancia de manhattan
	def calculate_heuristic(self, node, heuristic):
		if heuristic==1:
			h = self.out_of_place_heuristic(node.value)
		elif heuristic==2:
			h = self.manhattan_distance_heuristic(node.value)
		
		return h

	#Heuristica 1 para peças fora do lugar e heurística 2 para distancia de manhattan
	def A_star(self, node, level, heuristic=1):
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
	ap.add_argument('-d', "--dimensao", required=True, help="Informe o valor da matriz quadrada para o jogo")
	ap.add_argument('-b', "--busca", required=True, help="Informe qual busca deseja realizar para o jogo. Valores: (1)BFS, (2)DFS, (3)IDDS, (4)A*-heuristica peças fora do lugar, (5)A*-heuristica distância de Manhattan")
	args = vars(ap.parse_args())	
	dimension = int(args["dimensao"])
	search = int(args["busca"])

	#Cria o jogo com a dimensão informada
	game = Game(dimension)
	root = Node(game.board) #Instacia o primeiro nodo

	if (search == 1):
		print("BFS - Busca em amplitude")
		final = game.BFS(root,0)
		game.read_solution(final)
	elif (search == 2):
		print("DFS - Busca em profundidade")
		final = game.DFS(root,0)
		game.read_solution(final)
	elif (search == 3):
		print("IDDS - Busca em aprofundamento iterativo")
		final = game.IDDS(root, 0)
		game.read_solution(final)
	elif (search == 4):
		print("A* - Heurística número de peças fora do lugar")
		final = game.A_star(root, 1)
		game.read_solution(final)
	elif (search == 5):
		print("A* - Heurística distância de Manhattan")
		final = game.A_star(root, 2)
		game.read_solution(final)

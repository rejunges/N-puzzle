import argparse
import numpy as np
import operator
import random 
import time
import sys
from node import Node

class Game:

	def __init__(self, dimension):
		self.final_board = self.initial_config(dimension)
		self.dimension = dimension
		self.board = self.shuffle(self.final_board.copy())
		self.start_time = time.time()

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
		random.seed(seed)
		for i in range(0,num_shuffle):
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

	def format_time(self):
		hour, minutes, seconds = 0, 0, 0
		end_time = time.time() - self.start_time
		hour = end_time // 3600
		end_time %= 3600
		minutes = end_time // 60
		end_time %= 60
		seconds = end_time
		return hour, minutes, seconds

	def read_solution(self, node, total_nodes):
		print("Total de nodos abertos: " + str(total_nodes))
		print("Nível da solução encontrada: " + str(node.level))
		hour, minutes, seconds = self.format_time()
		print("Tempo de execução: %d"  %hour ,"horas, %d" %minutes, "minutos e %.4f segundos" % seconds)
		print("Caminho para desembaralhar o tabuleiro:")
		print()
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
		
	def acceptable_runtime(self, total_nodes, level):
		
		if time.time()-self.start_time >= 3600:
			print("Total de nodos abertos: " + str(total_nodes))
			print("Parou no nível e não encontrou solução: " + str(level))
			hour, minutes, seconds = self.format_time()
			print("Tempo de execução: %d"  %hour ,"horas, %d" %minutes, "minutos e %.4f segundos" % seconds)
			return False
		return True
	
	def verify_node(self, actual_node):
		return np.array_equal(actual_node, self.final_board)

	#cria o proximo nivel da arvore a partir do nodo pai
	def create_next_level_tree(self, node):
		node_up = self.move_up(node.value.copy())
		node_down = self.move_down(node.value.copy())
		node_right = self.move_right(node.value.copy())
		node_left = self.move_left(node.value.copy())
		
		if (not np.array_equal(node_up, node.value)):
			node.insert_up(node_up, node, node.level+1)
		
		if (not np.array_equal(node_down, node.value)):
			node.insert_down(node_down, node, node.level+1)
		
		if (not np.array_equal(node_right, node.value)):
			node.insert_right(node_right, node, node.level+1)
		
		if (not np.array_equal(node_left, node.value)):
			node.insert_left(node_left, node, node.level+1)
	

	#Busca em profundidade
	def DFS(self, node, level):
		
		to_visit = [node]
		visited = [node.value.tolist()]
		total_nodes = 1

		while to_visit:
			node = to_visit.pop(0)

			if self.verify_node(node.value):
				return node, total_nodes
			if not self.acceptable_runtime(total_nodes, node.level):
				sys.exit()

			self.create_next_level_tree(node)
			nodes = [node.up, node.down, node.right, node.left]
			for n in nodes:
				if (n != None and n.value.tolist() not in visited):
					to_visit.insert(0, n)
					visited.insert(0, n.value.tolist())
					total_nodes += 1
	
	#Busca em aprofundamento iterativo
	def IDS(self, node_root, level):
		
		to_visit = [node_root]
		total_nodes = 1
		visited = {}
		visited_list =[]

		def clean_visited(visited):
			for node in visited:
				del node

		def clean_sibling_branch(visited, level):
			v_items = visited.copy()
			for key, value in v_items.items():
				if key >= level:
					del visited[key]
					for nodes in value:
						del nodes
			return visited

		while True:
			print("Iteracao: " + str(level))
			
			while to_visit:
				node = to_visit.pop(0)
				visited_list.append(node.value.tolist())
				
				visited = clean_sibling_branch(visited, node.level)
				if node.level not in visited:
					visited[node.level] = []
				visited[node.level].append(node)
				
				if self.verify_node(node.value):
					return node, total_nodes
				if not self.acceptable_runtime(total_nodes, node.level):
					sys.exit()
				
				if node.level < level:
					self.create_next_level_tree(node)
					nodes = [node.up, node.down, node.right, node.left]
					for n in nodes:
						if (n != None and n.value.tolist() not in visited_list):
							to_visit.insert(0, n)
							total_nodes += 1
							

			v = []
			for key, nodes in visited.items():
				v.extend(nodes)

			clean_visited(v)
			to_visit = [node_root]
			level +=1
			visited = {}
			visited_list=[]
	
	#Busca em amplitude
	def BFS(self, node, level):

		to_visit = [node]
		total_nodes = 1
		visited = [node.value.tolist()]

		while to_visit:
			node = to_visit.pop(0)

			if self.verify_node(node.value):
				return node, total_nodes
			if not self.acceptable_runtime(total_nodes, node.level):
				sys.exit()
			
			self.create_next_level_tree(node)
			nodes = [node.up, node.down, node.right, node.left]
			for n in nodes:
				if (n != None and n.value.tolist() not in visited):
					to_visit.append(n)
					total_nodes += 1
					visited.append(n.value.tolist())
			
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
		total_nodes = 1
		while open_nodes:
			open_nodes = sorted(open_nodes, key=operator.itemgetter(1)) #order by f_score
			node, f_score = open_nodes.pop(0) 
			
			if self.verify_node(node.value):
				return node, total_nodes
			if not self.acceptable_runtime(total_nodes, node.level):
				sys.exit()
			
			#Esse if verifica se os nodos já estão abertos
			if node.up == None and node.down == None and node.right == None and node.left == None: 
				self.create_next_level_tree(node)
				nodes = [node.up, node.down, node.right, node.left]
				for n in nodes:
					if (n != None):
						h = self.calculate_heuristic(n, heuristic)
						open_nodes.append([n, node.level+1 + h])
						total_nodes += 1
				

if __name__ == '__main__':
	#Le a dimensao (nxn) do jogo
	ap = argparse.ArgumentParser()
	ap.add_argument('-d', "--dimensao", required=True, help="Informe o valor da matriz quadrada para o jogo")
	ap.add_argument('-b', "--busca", required=True, help="Informe qual busca deseja realizar para o jogo. Valores: (1)BFS, (2)DFS, (3)IDS, (4)A*-heuristica peças fora do lugar, (5)A*-heuristica distância de Manhattan")
	ap.add_argument('-s', "--semente", required=False, default = 20, help="Semente para shuffle")
	ap.add_argument('-e', "--embaralhamento", required=False, default = 100, help="Número de embaralhamento na matriz")
	args = vars(ap.parse_args())	
	dimension = int(args["dimensao"])
	search = int(args["busca"])
	seed = int(args["semente"])
	num_shuffle = int(args["embaralhamento"])

	#Cria o jogo com a dimensão informada
	game = Game(dimension)
	root = Node(game.board) #Instacia o primeiro nodo

	if (search == 1):
		print("BFS - Busca em amplitude")
		final, total_nodes = game.BFS(root,0)
		game.read_solution(final, total_nodes)
	elif (search == 2):
		print("DFS - Busca em profundidade")
		final, total_nodes = game.DFS(root,0)
		game.read_solution(final, total_nodes)
	elif (search == 3):
		print("IDS - Busca em aprofundamento iterativo")
		final, total_nodes = game.IDS(root, 0)
		game.read_solution(final, total_nodes)
	elif (search == 4):
		print("A* - Heurística número de peças fora do lugar")
		final, total_nodes = game.A_star(root, 0, 1)
		game.read_solution(final, total_nodes)
	elif (search == 5):
		print("A* - Heurística distância de Manhattan")
		final, total_nodes = game.A_star(root, 0, 2)
		game.read_solution(final, total_nodes)

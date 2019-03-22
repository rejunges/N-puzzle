import argparse
import numpy as np

def initial_config(dimension):
	line = []
	cont = 1
	for i in range(0, dimension):
		line.append(np.arange(cont, dimension+cont))
		cont += dimension
	line[dimension-1][dimension-1] = 0
	m = np.matrix(line)

	return m

def move_up(m):
	i, j = np.where(m == 0)
	if (i!=0):
		m[i,j] = m[i-1,j]
		m[i-1,j] = 0
	return m

def move_down(m):
	i, j = np.where(m == 0)
	if (i!=dimension-1):
		m[i,j] = m[i+1,j]
		m[i+1,j] = 0
	return m
	
def move_left(m):
	i, j = np.where(m == 0)
	if (j!=0):
		m[i,j] = m[i,j-1]
		m[i,j-1] = 0
	return m

def move_right(m):
	i, j = np.where(m == 0)
	if (j!=dimension-1):
		m[i,j] = m[i,j+1]
		m[i,j+1] = 0
	return m


#Le a dimensao (nxn) do jogo
ap = argparse.ArgumentParser()
ap.add_argument('-d', "--dimensao", required=True, help="Informe o valor da matriz quadrado para o jogo")
args = vars(ap.parse_args())	
dimension = int(args["dimensao"])


m = initial_config(dimension)

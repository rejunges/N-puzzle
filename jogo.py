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

#def move_up():


#def move_down():
	#Verify if it is possible 
	
#def move_left():

#def move_right():

#Le a dimensao (nxn) do jogo
ap = argparse.ArgumentParser()
ap.add_argument('-d', "--dimensao", required=True, help="Informe o valor da matriz quadrado para o jogo")
args = vars(ap.parse_args())	
dimension = int(args["dimensao"])


m = initial_config(dimension)
print(m)

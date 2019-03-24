import numpy as np

class Node:

    def __init__(self, value, father = None, nivel = 0):
        self.left = None
        self.right = None
        self.down = None
        self.up = None
        self.father = father
        self.value = value
        self.nivel = nivel
    
    def insert_left(self, value, father, nivel):
        self.left = Node(value, father, nivel)
    
    def insert_right(self, value, father, nivel):
        self.right = Node(value, father, nivel)

    def insert_down(self, value, father, nivel):
        self.down = Node(value, father, nivel)
    
    def insert_up(self, value, father, nivel):
        self.up = Node(value, father, nivel)
    

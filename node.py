import numpy as np

class Node:

    def __init__(self, value, father = None, level = 0):
        self.left = None
        self.right = None
        self.down = None
        self.up = None
        self.father = father
        self.value = value
        self.level = level
    
    def insert_left(self, value, father, level):
        self.left = Node(value, father, level)
    
    def insert_right(self, value, father, level):
        self.right = Node(value, father, level)

    def insert_down(self, value, father, level):
        self.down = Node(value, father, level)
    
    def insert_up(self, value, father, level):
        self.up = Node(value, father, level)
    

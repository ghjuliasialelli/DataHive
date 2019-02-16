# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 18:23:56 2019

@author: Sebastien
"""

class Tree:
    def __init__(self,key,data):
        self.root = Node(key,data,set([key]))
        
    def get_leafs(self):
        return self.root.get_leafs()

    def get_itis(self):
        return self.root.get_itis([])
    
class Node:
    def __init__(self,key,data,parents):
        self.key = key
        self.data = data
        self.children = {}
        self.parents = parents
        
    def insert(self,key,data):
        parents = self.parents.union([key])
        self.children[key] = Node(key,data,parents)
        
    def get_leafs(self):
        if len(self.children) == 0:
            return [self]
        sol = []
        for key in self.children:
            sol += self.children[key].get_leafs()
        return sol

    def get_itis(self,path):
        path  = path + [self.key]
        itis = [[path,self.data]]
        for key in self.children:
            itis += self.children[key].get_itis(path)
        return itis
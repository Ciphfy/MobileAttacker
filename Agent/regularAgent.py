from Centerpoint import * 
import numpy as np

class RegularAgent:
    def __init__(self, no, pos):
        self.no = no
        self.pos = pos
        self.status = 'R'
        self.neighbors = []
        self.update_set = []

    def get_pos(self):
        return self.pos
    
    def get_no(self):
        return self.no
    
    def get_status(self):
        return self.status
    
    def get_neighbors(self):
        return self.neighbors
    
    def get_update_set(self):
        return self.update_set

    def set_pos(self, pos):
        self.pos = pos
    
    def set_status(self, status):
        if (status == 'R' or status == 'C' or status == 'M'): 
            self.status = status
        else:
            self.status = 'R'
            raise Exception('Wrong statues was input')
    
    """input the total adjacent matrix to find neighbors"""
    def find_neighbors(self, graph):
        graph = np.array(graph)
        count = 0
        if self.no >= len(graph):
            raise Exception('Wrong adjacent matrix')
        else:
            for i in graph[self.no]:
                if i!=0:
                    self.neighbors.append(count)
                    count+=1
                else:
                    count+=1

from Centerpoint import * 
import numpy as np

class RegularAgent:
    def __init__(self, no, pos):
        self.no = no
        self.pos = pos
        self.status = 'R'
        self.neighbors = [] #self is considered to be neighbor
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
    
    def find_neighbors(self, graph):
        """input the total adjacent matrix as list to find neighbors.
        Adjacent matrix includes self as a neighbor """
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

    def find_update_set(self, point_set):
        """Malicious agents directly set its next state.
           Cured and Regular ones will receive values from neighbors(self included). 
           Point set contains all agents' position data denoted by 2-D list"""
        if self.status=='M':
            self.m_next_state()
            return
        elif len(self.neighbors)==0:
            raise Exception('No neighbors to hear from')
        else:
            self.update_set =  [point_set[pos] for pos in self.neighbors]

    def m_next_state(self, lower=0, upper=20):
        """Malicious will update its values randomly"""
        x = random.uniform(lower, upper)
        y = random.uniform(lower, upper)
        self.set_pos([x,y])

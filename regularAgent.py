from Centerpoint import *
import numpy as np
from configuration import *

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
            raise Exception('Wrong status was input')
    
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
        """Malicious agents collect nothing.
           Cured and Regular ones will receive values from neighbors(self included). 
           Point set contains all agents' position data denoted by 2-D list"""
        if self.status=='M':
            #self.m_next_state()
            self.update_set.clear()
            return
        elif len(self.neighbors)==0:
            raise Exception('No neighbors to hear from')
        else:
            self.update_set =  [point_set[pos] for pos in self.neighbors]

    def find_update_set_with_flag(self, point_set, attack_last_obj):
        '''Update set constructed in model3(model2 with cured flag)'''
        if self.status=='M':
            #self.m_next_state()
            self.update_set.clear()
            return
        elif len(self.neighbors)==0:
            raise Exception('No neighbors to hear from')
        else:
            self.update_set.clear()
            for i in range(0,len(point_set)):
                if i==attack_last_obj:
                    continue
                else:
                    self.update_set.append(point_set[i])


    def m_next_state(self, lower=0, upper=20, mode='default'):
        """Malicious will update its values randomly"""
        if mode == 'default':
            x = random.uniform(lower, upper)
            y = random.uniform(lower, upper)
            self.set_pos(Point(x,y))
        if mode == 'margin':
            margin = [1,19]
            x = margin[self.no%2]
            y = margin[(self.no+1)%2]
            self.set_pos(Point(x,y))

    def next_state(self, method='centerpoint'):
        """Next step of non-faulty agents"""
        if (method=='centerpoint' and self.status!='M'):
            cp = Centerpoint()
            #self.pos = cp.reduce_then_get_centerpoint(self.update_set)
            #self.pos = cp.brute_force_centerpoint(self.update_set)
            self.pos = cp.reduce_then_get_centerpoint(self.update_set)
            while not self.pos:
                 self.update_set = [Point(p.x + 0.0001 * random.random(), p.y + 0.0001 * random.random()) for p in self.update_set]
                 self.pos = cp.reduce_then_get_centerpoint(self.update_set)
        else:
            return
        
    def check_whether_attacked(self, attack_next_object):
        '''Input attackers' next targets, then change local status according to it.
            Agents attacked will change its pos value to malicious'''
        if self.no not in attack_next_object:
            if self.status == 'M':
                self.status = 'C'
            else:
                self.status = 'R'
        else:
            self.status = 'M'
            self.m_next_state()
        


'''Tool function'''
def attacker_move(n, n_f):
    '''Randomly generate attackers' target. Num of targets = n_f'''
    next_object = []
    i = 0
    while i<n_f:
        a = random.randint(0,n-1)
        if a not in next_object:
            next_object.append(a)
            i +=1
        else:
            continue
    return next_object

def attacker_move_worst(n, n_f, last_obj):
    '''Attackers move to only regular agents(Worst case)'''
    next_object = []
    i =0 
    while i<n_f:
        a = random.randint(0,n-1)
        if a not in next_object and a not in last_obj:
            next_object.append(a)
            i +=1
        else:
            continue
    return next_object

def attacker_static(n, n_f):
    '''Attackers do not move'''
    next_object = [i for i in range(n-n_f, n)]
    return next_object

def plot_then_save(save_path, all_agent, k, x=(0,21), y=(0,21)):
    plt.clf()
    plt.xlim(x)
    plt.ylim(y)
    for i in all_agent:
        if i.status == 'R':
            plot_point(i.pos,color='b')
            plt.annotate('R'+str(i.no+1), (i.pos.x, i.pos.y))
        if i.status == 'C':
            plot_point(i.pos,color='y')
            plt.annotate('C'+str(i.no+1), (i.pos.x, i.pos.y))
        if i.status == 'M':
            plot_point(i.pos,color='r')
            plt.annotate('M'+str(i.no+1), (i.pos.x, i.pos.y))
    '''fig_title = 'Malicious agent is:'
    for i in m_agent:
        fig_title = fig_title + '\x20' +str(i)
    plt.title(fig_title)'''
    plt.savefig(save_path+'%s%d.png' %('round',k+1))





if __name__ == '__main__':
    random.seed(8)
    plot = False #do not draw the process of finding CP
    save_path = 'result\model1\\'
    model = 'model1'
    '''Initialize the graph(Adjacent matrix).'''
    graph_adjacency = graph_14nodes_r22
    '''Initialize the number of attackers'''
    n = len(graph_adjacency) #num of agents
    n_half = n//2
    #state_point = random_point_set(n, 5, 10) #type==Point
    state_point = random_point_set(n_half, 1, 10) + random_point_set(n-n_half, 10,19)
    agent_f_num = 1 #num of attackers
    agent_unf_num = n-agent_f_num #num of non-faulty agents
    agent = [] #agent set. Type==RegularAgent
    
    '''Initialize the agents(Regular and Malicious).'''
    for i in range(0,n):
        if i<agent_unf_num:
            agent.append(RegularAgent(no=i, pos=state_point[i]))
            agent[i].set_status('R')
        else:
            agent.append(RegularAgent(no=i, pos=state_point[i]))
            agent[i].set_status('M')
            #agent[i].m_next_state()
            agent[i].set_pos(Point(18,1))
    
    '''Initialize the configurations of round 1 and figure style''' 
    plt.figure(figsize=(5,5))
    plt.xlim((0,21))
    plt.ylim((0,21))
    attack_last_obj = []
    attack_next_obj = []
    for a in agent:
        if a.status != 'M':
            plot_point(a.pos, color='b')
        else:
            plot_point(a.pos,color='r')
            attack_next_obj.append(a.no) #malicious agent in round k=0
    fig_title = 'Malicious agent is:'
    for i in attack_next_obj:
        fig_title = fig_title + '\x20' +str(i)
    plt.title(fig_title)
    plt.savefig(save_path+'%s.png' %('initial'))
    
    '''Initial the communication topology'''
    for i in range(0,n):
        agent[i].find_neighbors(graph_adjacency)
        agent[i].find_update_set(state_point)
        #print("position of agent:",agent[i].no,"is",agent[i].pos) 
    
    '''Start iterations''' 
    for k in range(0,30): #set iteration times
        pos_t = [] #store the position data in every round. type==Point
        for i in range(0,n): #update local values with updating set 
            agent[i].next_state(method='centerpoint')
            pos_t.append(agent[i].pos)
            #print("next position of agent",agent[i].no,"is",agent[i].pos)
        
        '''plot the result'''
        #agent_r_pos = [r.pos for r in agent if r.status=='R']
        #agent_m_pos = [m.pos for m in agent if m.status=='M']
        #agent_c_pos = [c.pos for c in agent if c.status=='C']
        plot_then_save(save_path, agent, k)
        
        '''Set configurations for next iterations. Attackers make movements'''
        attack_last_obj = attack_next_obj
        #attack_next_obj = attacker_static(n=n, n_f=agent_f_num)
        #attack_next_obj = attacker_move(n=n, n_f=agent_f_num)
        attack_next_obj = attacker_move_worst(n=n, n_f=agent_f_num, last_obj=attack_last_obj)
        
        for a in agent:
            a.check_whether_attacked(attack_next_obj)
        for a in agent:
            a.find_update_set(pos_t)
from regularAgent import *

'''Consider the worst case that all attackers move to new un-faulty agents.
To show this behaviors, different from model1, malicious agents in this case will 
make its own position to malicious value randomly and send it to others concurrently.'''

random.seed(8)
plot = False #do not draw the process of finding CP
save_path = 'result\model2S\\'
model = 'model2'
'''Initialize the graph(Adjacent matrix).'''
graph_adjacency = graph_11nodes_r32
'''Initialize the number of attackers'''
n = len(graph_adjacency) #num of agents

#state_point = random_point_set(n, 5, 10) #type==Point
state_point = random_point_set(n, 3, 5)
state_point[6] = Point(5.5,5)
malicious_state = Point(6,5)
malicious_set = [4,5]
state_point[4] = malicious_state
state_point[5] = malicious_state
agent_f_num = 1 #num of attackers
agent_unf_num = n-agent_f_num #num of non-faulty agents
agent = [] #agent set. Type==RegularAgent

'''Initialize the agents(Regular and Malicious).'''
for i in range(0,n):
    if i not in malicious_set:
        agent.append(RegularAgent(no=i, pos=state_point[i]))
        agent[i].set_status('R')
    else:
        agent.append(RegularAgent(no=i, pos=state_point[i]))
        if i == 5:
            agent[i].set_status('M')
            agent[i].set_pos(malicious_state)
        else:
            agent[i].set_status('C')
            agent[i].set_pos(malicious_state)

'''Initialize the configurations of round 1 and figure style''' 
plt.figure(figsize=(5,5))
plt.xlim((3,7))
plt.ylim((3,7))
attack_last_obj = 4
attack_next_obj = 5
for a in agent:
    if a.status == 'R':
        plot_point(a.pos, color='b')
    elif a.status == 'C':
        plot_point(a.pos, color='y')
    else:
        plot_point(a.pos,color='r')
        
fig_title = 'Malicious agent is switched between 5 and 6'
plt.title(fig_title)
plt.savefig(save_path+'%s.png' %('initial'))

'''Initial the communication topology'''
for i in range(0,n):
    agent[i].find_neighbors(graph_adjacency)
    agent[i].find_update_set(state_point)
    #print("position of agent:",agent[i].no,"is",agent[i].pos) 

'''Start iterations''' 
for k in range(0,50): #set iteration times
    pos_t = [] #store the position data in every round. type==Point
    for i in range(0,n): #update local values with updating set 
        if i==attack_last_obj:
            agent[i].pos = malicious_state
            pos_t.append(agent[i].pos)
        else:
            agent[i].next_state(method='centerpoint')
            pos_t.append(agent[i].pos)
            #print("next position of agent",agent[i].no,"is",agent[i].pos)
        
    '''plot the result'''
    #agent_r_pos = [r.pos for r in agent if r.status=='R']
    #agent_m_pos = [m.pos for m in agent if m.status=='M']
    #agent_c_pos = [c.pos for c in agent if c.status=='C']
    plot_then_save(save_path, agent, k, x=(3,7), y=(3,7))
    
    '''Set configurations for next iterations. Attackers make movements'''
    attack_last_obj = attack_next_obj
    #attack_next_obj = attacker_static(n=n, n_f=agent_f_num)
    #attack_next_obj = attacker_move(n=n, n_f=agent_f_num)
    attack_next_obj = malicious_set[k%2]
    
    for a in agent:
        if a.no == attack_last_obj:
            a.set_status('C')
        elif a.no == attack_next_obj:
            a.set_status('M')
            a.pos = malicious_state
            pos_t[a.no] = a.pos
        '''differences to distinguish model2 and model1'''
    for a in agent:
        a.find_update_set(pos_t)
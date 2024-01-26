from regularAgent import *

random.seed(18)
plot = False #do not draw the process of finding CP
save_path = 'result\model1\\'
model = 'model1'
'''Initialize the graph(Adjacent matrix).'''
graph_adjacency = graph_test2_r22
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
pos_t = []
'''Start iterations''' 
for k in range(0,150): #set iteration times
    pos_t.clear() #store the position data in every round. type==Point
    for i in range(0,n): #update local values with updating set 
        agent[i].next_state(method='centerpoint')
        while not agent[i].pos:
            agent[i].next_state(method='centerpoint')
        pos_t.append(agent[i].pos)
        #print("next position of agent",agent[i].no,"is",agent[i].pos)
    
    '''plot the result'''
    #agent_r_pos = [r.pos for r in agent if r.status=='R']
    #agent_m_pos = [m.pos for m in agent if m.status=='M']
    #agent_c_pos = [c.pos for c in agent if c.status=='C']
    plot_then_save(save_path, agent, k)
    #if k==37:
       # raise Exception('stop')
    
    '''Set configurations for next iterations. Attackers make movements'''
    attack_last_obj = attack_next_obj
    #attack_next_obj = attacker_static(n=n, n_f=agent_f_num)
    #attack_next_obj = attacker_move(n=n, n_f=agent_f_num)
    attack_next_obj = attacker_move_worst(n=n, n_f=agent_f_num, last_obj=attack_last_obj)
    
    for a in agent:
        a.check_whether_attacked(attack_next_obj)
    for a in agent:
        a.find_update_set(pos_t)
import numpy as np
from regularAgent import *

network = [[1,0,1],[0,1,0],[1,1,1]]
#a = np.array([[1,2],[3,4]])
agent_0 = RegularAgent(0,[0,1])
agent_1 = RegularAgent(1,[1,1])
agent_2 = RegularAgent(2,[2,1])
agent_3 = RegularAgent(3,[3,1])

agent_3.find_neighbors(network)
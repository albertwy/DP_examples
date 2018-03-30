# -*- coding: utf-8 -*-

# id of the states, 0 and 15 are terminal states
states = [i for i in range(16)]
#  0* 1  2   3  
#  4  5  6   7
#  8  9  10  11
#  12 13 14  15*

# initial values of states
values = [0  for _ in range(16)]

# Action

#  N
#W    E
#  S

actions = ["n", "e", "s", "w"]

# policy
pi = {}

# 行为对应的状态改变量
# use a dictionary for convenient computation of next state id.
ds_actions = {"n": -4, "e": 1, "s": 4, "w": -1}  

# discount factor
gamma = 1.00

for s in states:
	pi[s] = {}
	for action in ds_actions.keys():
		pi[s][action] = 1.0/4

Q_value = {}
for s in states:
	Q_value[s] = {}
	for action in ds_actions.keys():
		Q_value[s][action] = 0

# 根据当前状态和采取的行为计算下一个状态id以及得到的即时奖励
def nextState(s, a):
	next_state = s
	if (s%4 == 0 and a == "w") or (s<4 and a == "n") or \
		((s+1)%4 == 0 and a == "e") or (s > 11 and a == "s"):
		pass
	else:
		ds = ds_actions[a]
		next_state = s + ds
	return next_state

# reward of a state
def rewardOf(s):
	return 0 if s in [0,15] else -1

# check if a state is terminate state
def isTerminateState(s):
	return s in [0,15]

# get successor states of a given state s
def getSuccessors(s):
	successors = []
	if isTerminateState(s):
		return successors
	for a in actions:
		next_state = nextState(s, a)
		# if s != next_state:
		successors.append(next_state)
	return successors

# update the value of state s
def updateQValue(s):
	sucessors = getSuccessors(s)
	newQValue = {}  # Qvalues[s]
	reward = rewardOf(s)
	assert len(sucessors) == 4 or len(sucessors) == 0
	global Q_value,actions
	for i in xrange(len(sucessors)):
		q_value = [Q_value[sucessors[i]][key] for key in Q_value[sucessors[i]].keys()]
		if len(q_value) == 0:
			tmp = 0
		else:
			tmp = max(q_value)	
		newQValue[actions[i]] = reward + gamma * tmp
	
	return newQValue

# perform one-step iteration
def performOneIteration():
	qvalue = {}
	for s in states:
		qvalue[s] = updateQValue(s)
	global Q_value
	Q_value = qvalue
	printQ(Q_value)

# show some array info of the small grid world
def printQ(v):
	global Q_value
	for key in Q_value.keys():
		print "State : {}  direction:{}".format(key,Q_value[key]) 
	print "\n"
	
	dmap = ["v",">","<","^"]
	for i in xrange(4):
		for j in xrange(4):
			if len(Q_value[4*i+j]) > 0:
				value = [Q_value[4*i+j]["s"],Q_value[4*i+j]["e"],Q_value[4*i+j]["w"],Q_value[4*i+j]["n"]]
				print dmap[value.index(max(value))],
			else:
				print " ",
		print ""
				






def main():
	MAX_TIME = 200
	cur_iterate_times = 0
	while True:
		performOneIteration()
		cur_iterate_times += 1
		if cur_iterate_times > MAX_TIME:
			break
		print " current iterate times : {}".format(cur_iterate_times)
		

		
  
  




if __name__ == '__main__':
	main()

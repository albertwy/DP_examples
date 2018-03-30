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
def updateValue(s):
	sucessors = getSuccessors(s)
	newValue = 0  # values[s]
	reward = rewardOf(s)
	assert len(sucessors) == 4 or len(sucessors) == 0
	global pi,actions
	for i in xrange(len(sucessors)):
		newValue +=  pi[s][actions[i]]* (reward + gamma * values[sucessors[i]])
	return newValue

# perform one-step iteration
def performOneIteration():
	newValues = [0 for _ in range(16)]
	for s in states:
		newValues[s] = updateValue(s)
	global values
	values = newValues
	printValue(values)

# show some array info of the small grid world
def printValue(v):
	for i in range(16):
		print'{0:>6.2f}'.format(v[i],end = ""),
		if (i+1)%4 == 0:
			print("")
	print ""

# get new policy from values through greedy 
def greedy(values):
	global pi,states,actions
	for state in states:
		pi[state] = {}
		successors = getSuccessors(state)
		list_value = [values[successor] for successor in successors]
		if len(list_value) == 0:
			continue
		value = max(list_value)

		tmp = [list_value[i] == value for i in xrange(len(list_value))]
		t = sum(tmp)
		for i in xrange(len(list_value)):
			if list_value[i] == value:
				pi[state][actions[i]] = 1.0/t
			else:			
				pi[state][actions[i]] = 0
	print pi
			
def calcuate_values(v1,v2):
	return sum([(i-j)*(i-j) for i,j in zip(v1,v2)])




def main():
	CUT_VALUE = [0.001,0.001]
	Flag = True  
	cur_iterate_times = 0
	last_step_values = [0  for _ in range(16)]
	time = 0
	while True:
		time += 1
		while True:
			last_value = values
			performOneIteration()
			cur_iterate_times += 1
			if calcuate_values(values,last_value) < CUT_VALUE[0]:
				break
			printValue(values)
			print "Iter time : {} | current iterate times : {}".format(time,cur_iterate_times)

		if calcuate_values(last_step_values,values) < CUT_VALUE[1] :
			break
		last_step_values = values
		greedy(values)
  
  




if __name__ == '__main__':
  main()

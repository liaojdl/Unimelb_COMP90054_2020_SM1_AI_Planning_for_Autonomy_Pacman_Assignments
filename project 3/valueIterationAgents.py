# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util
from learningAgents import ValueEstimationAgent
import collections
import logging
logging.basicConfig(level=logging.DEBUG)

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        # get all possible states (co-ordinates)
        states = self.mdp.getStates()
        # repeat for a defined number of iterations
        for i in range(self.iterations):
            values_iter = util.Counter()
            for state in states:
                if not self.mdp.isTerminal(state):
                    action = self.getAction(state)
                    values_iter[state] = self.computeQValueFromValues(state,action)
            self.values = values_iter
        return True

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # get the next reachable state, probablity pair list
        nextstate_prob_list = self.mdp.getTransitionStatesAndProbs(state,action)
        Q = 0
        # computes Q
        for (next_state,prob) in nextstate_prob_list:
            next_reward = self.mdp.getReward(state,action,next_state)
            # discounted last reward
            last_reward = self.discount*self.values[next_state]
            Q += prob*(next_reward+last_reward)
        return Q
        #util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        best_action = None
        best_Q = -float("inf")
        # available actions
        actions_list = self.mdp.getPossibleActions(state)
        # get action of largest Q
        for action in actions_list: 
            Q = self.computeQValueFromValues(state,action)
            if Q>best_Q :
                best_Q = Q
                best_action = action
        return best_action
        #util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        # get all possible states (co-ordinates)
        states = self.mdp.getStates()
        # number of states
        n_states = len(states)
        # track the state index
        i_state = 0
        # repeat for a defined number of iterations
        values_iter = util.Counter()
        for i in range(self.iterations):
            # asynchronous state update
            state = states[i_state]
            if not self.mdp.isTerminal(state):
                action = self.getAction(state)
                values_iter[state] = self.computeQValueFromValues(state,action)
            self.values = values_iter
            i_state = i_state+1
            # pop back to starting state when all states are updated once
            if i_state==n_states:
                i_state = 0
        return True

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)
    
    def computePredecessors(self, states):
        predecessors = {state: set() for state in states}
        for state in states:
            for action in self.mdp.getPossibleActions(state):
                for (next_state, prob) in self.mdp.getTransitionStatesAndProbs(state, action):
                    if prob > 0:
                        predecessors[next_state].add(state)
        return predecessors

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        # empty priority queue
        myqueue = util.PriorityQueue()
        # get all possible states (co-ordinates)
        states = self.mdp.getStates()
        # compute predecessors
        predecessors = self.computePredecessors(states)
        #logging.debug(predecessors)

        # find abs diff 
        for state in states:
            if not self.mdp.isTerminal(state):
                best_action = self.computeActionFromValues(state)
                best_Q = self.computeQValueFromValues(state, best_action)
                diff = abs(self.values[state] - best_Q)
                myqueue.push(state, -diff)
        
        # do the learning iterations
        values_iter = util.Counter()
        for i in range(self.iterations):
            if myqueue.isEmpty():
                break
            state = myqueue.pop()
            if not self.mdp.isTerminal(state):
                action = self.getAction(state)
                values_iter[state] = self.computeQValueFromValues(state,action)
                self.values = values_iter
            for predecessor in predecessors[state]:
                best_action = self.computeActionFromValues(predecessor)
                best_Q = self.computeQValueFromValues(predecessor, best_action)
                diff = abs(self.values[predecessor] - best_Q)
                if diff > self.theta:
                    myqueue.update(predecessor, -diff)
    
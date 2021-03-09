# search.py
# ---------
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

# COMP90054 AI Planning for Autonomy, Semester 1, 2020
# Project 1 Search
# Jiawei Liao (756560)
# liao2@student.unimelb.edu.au

"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import math
import searchAgents

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    A sample depth first search implementation is provided for you to help you understand how to interact with the problem.
    """
    # LIFO Structure for DFS
    mystack = util.Stack()
    # Starting Node, (x,y), nullaction, cost=0, no path planned
    startNode = (problem.getStartState(), '', 0, [])
    mystack.push(startNode)
    # Records the visited state
    visited = set()
    # Looping over the Fringe to expand nodes until empty
    while mystack :
        # node of interest
        node = mystack.pop()
        state, action, cost, path = node
        # make sure to skip visited node
        if state not in visited :
            visited.add(state)
            # found the goal
            if problem.isGoalState(state) :
                path = path + [(state, action)]
                break
            # get possible next move from currrent state, could be null or up to 4
            succStates = problem.getSuccessors(state)
            # push the possible new state nodes into the stack
            for succState in succStates :
                nextState, succAction, succCost = succState
                newNode = (nextState, succAction, cost + succCost, path + [(state, action)])
                mystack.push(newNode)

    actions = [action[1] for action in path]
    # no need for the first null-action at starting position
    del actions[0]
    return actions

def breadthFirstSearch(problem):
    #FIFO structure
    myqueue = util.Queue()
    startNode = (problem.getStartState(), '', 0, [])
    myqueue.push(startNode)
    visited = set()
    while myqueue :
        Node = myqueue.pop()
        state, action, cost, path = Node
        if state not in visited :
            visited.add(state)
            if problem.isGoalState(state) :
                path = path + [(state, action)]
                break
            succStates = problem.getSuccessors(state)
            for succState in succStates :
                nextState, succAction, succCost = succState
                newNode = (nextState, succAction, cost + succCost, path + [(state, action)])
                myqueue.push(newNode)
    actions = [action[1] for action in path]
    del actions[0]
    return actions


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    "just a testing message"
    # this is equivalent to A* when h=nullheuristic for all states 
    return aStarSearch(problem, heuristic=nullHeuristic)


def manhattanHeuristic(position1, position2):
    "The Manhattan distance heuristic between two points"
    xy1 = position1
    xy2 = position2
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def euclideanHeuristic(position1, position2):
    "The Euclidean distance heuristic between two points"
    xy1 = position1
    xy2 = position2
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

def nullHeuristic(position1, position2):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=manhattanHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    # priority queue to sort states based on f(g state_cost + h heuristic_cost)
    myqueue = util.PriorityQueue()
    # initial Node state
    startNode = (problem.getStartState(), '', 0, [])
    # goal position of maze (x,y)
    goalState = problem.goal
    # heuristic using manhattan distance, initiliase initial value
    hInitial = heuristic(startNode[0], goalState)
    # Best f value, initial value is just h since state cost is 0
    fBest = hInitial
    # push initial state into queue, no iniital state cost
    myqueue.push(startNode,fBest)
    # records the states already visited (can be repeated nodes for A*)
    visited = set()
    #output state#
    outNode = startNode
    # goal found?
    goalFound = False

    # while there are still states to be explored
    while not myqueue.isEmpty() :
        node = myqueue.pop()
        # extract node state parameters
        state, action, cost, path = node
        # g = state cost + heuristic cost
        fFunc = cost + heuristic(state, goalState)
        # skips visited nodes unless a better g exists for it
        if (state not in visited) or (fFunc<fBest) :
            # new unexplored state, can be repeated nodes
            visited.add(state)
            fBest = fFunc
            # stop when finding the goal
            if problem.isGoalState(state) :
                # if goal is found give the final action
                path = path + [(state, action)]
                outNode = (state,action,cost,path)
                goalFound = True
            # get all possible successor states, up to 4
            succStates = problem.getSuccessors(state)
            for succState in succStates :
                nextState, succAction, succCost = succState
                newNode = (nextState, succAction, cost + succCost, path + [(state, action)])
                # update the f function, state cost, actions
                newfFunc = cost + succCost + heuristic(nextState, goalState)
                if (newfFunc < math.inf) :
                    myqueue.update(newNode,newfFunc)

    # path of the outstate
    path = outNode[3]
    # give solution path if it exists
    if goalFound :      
        actions = [action[1] for action in path]
        del actions[0] 
    else :
        # give no action if solution does not exist (goal is walled off)
        print ("Oops, stuck and cannot find your goal!")
        actions = []
    return actions


def aStarSearch_2P(problem, startState, goalState, heuristic=manhattanHeuristic):
    """A modified Astar search function to pick selected startstate
    and selected goalstate + heuristic, used by the part 3 agents
    
    input:
    &param problem, the problem of the game object, a search problem in this case
    &param startState, (x,y) pos of intended start state
    &param goalState, (x,y) pos of intended goal state 
    &param heuristic, the heuristic function intended to use
    
    output:
    &param outNode, the output node of (state,cost,action,path)
    &param actions, the actions to reach goal, [] if cannot compute such"""
    
    # priority queue to sort states based on f(g state_cost + h heuristic_cost)
    myqueue = util.PriorityQueue()
    # initial Node state
    startNode = (startState, '', 0, [])
    # heuristic using manhattan distance, initiliase initial value
    hInitial = heuristic(startNode[0], goalState)
    # Best f value, initial value is just h since state cost is 0
    fBest = hInitial
    # push initial state into queue, no iniital state cost
    myqueue.push(startNode,fBest)
    # records the states already visited (can be repeated nodes for A*)
    visited = set()
    #output state#
    outNode = startNode
    # goal found?
    goalFound = False

    # while there are still states to be explored
    while not myqueue.isEmpty() :
        node = myqueue.pop()
        #print(ode)
        # extract node state parameters
        state, action, cost, path = node
        # print(state)
        # g = state cost + heuristic cost
        fFunc = cost + heuristic(state, goalState)
        # skips visited nodes unless a better g exists for it
        if (state not in visited) or (fFunc<fBest) :
            # new unexplored state, can be repeated nodes
            visited.add(state)
            fBest = fFunc
            # stop when finding the goal
            if (state == goalState) :
                # if goal is found give the final action
                path = path + [(state, action)]
                outNode = (state,action,cost,path)
                goalFound = True
            # get all possible successor states, up to 4
            succStates = problem.getSuccessors(state)
            for succState in succStates :
                nextState, succAction, succCost = succState
                newNode = (nextState, succAction, cost + succCost, path + [(state, action)])
                # update the f function, state cost, actions
                newfFunc = cost + succCost + heuristic(nextState, goalState)
                if (newfFunc < math.inf) :
                    myqueue.update(newNode,newfFunc)

    # path of the outstate
    path = outNode[3]
    # give solution path if it exists
    if goalFound :      
        actions = [action[1] for action in path]
        del actions[0] 
    else :
        # give no action if solution does not exist (goal is walled off)
        print ("Oops, stuck and cannot find your goal!")
        actions = []
    return (outNode,actions)

def aStarSearch_2PDecep(problem, s, t, gr, gf, alpha, heuristic=manhattanHeuristic):
    """A modified Astar search function to pick selected startstate
    and selected goalstate + heuristic, used by the part 3 agents
    
    input:
    &param problem, the problem of the game object, a search problem in this case
    &param s, (x,y) pos of intended start state
    &param t, (x,y) pos of point t of deceptive path planning 
    &param gr, (x,y) pos of real goal
    &param gf, (x,y) pos of fake goal
    &param alpha, a multiplier for the heuristic to talor to deceptoion
    &param heuristic, the heuristic function intended to use
    
    output:
    &param outNode, the output node of (state,cost,action,path)
    &param actions, the actions to reach goal, [] if cannot compute such"""
    
    # priority queue to sort states based on f(g state_cost + h heuristic_cost)
    myqueue = util.PriorityQueue()
    # initial Node state
    startNode = (s, '', 0, [])
    # heuristic using manhattan distance, initiliase initial value
    # h(n,gr) initialised
    hngrInitial = heuristic(s, gr)
    # h(n,gf) initialised
    hngfInitial = heuristic(s, gf)
    # h(n,t) initialised
    hntInitial = heuristic(s, t)
    # Best f value, initial value is just h since state cost is 0
    fBest = hntInitial
    if (hngrInitial<hngfInitial):
        fBest = alpha * hntInitial
    # push initial state into queue, no iniital state cost
    myqueue.push(startNode,fBest)
    # records the states already visited (can be repeated nodes for A*)
    visited = set()
    #output state#
    outNode = startNode
    # goal found?
    goalFound = False

    # while there are still states to be explored
    while not myqueue.isEmpty() :
        node = myqueue.pop()
        # extract node state parameters
        state, action, cost, path = node
        # print(state)
        # g = state cost + heuristic cost

        # h(n,gr)
        hngr = heuristic(state, gr)
        # h(n,gf)
        hngf = heuristic(state, gf)
        # h(n,t)
        hnt = heuristic(state, t)
        if (hngr<hngf):
            hnt = alpha * hnt
        fFunc = cost + hnt
        #print(state)
        #print(fFunc)

        # skips visited nodes
        if (state not in visited):
            # new unexplored state, can be repeated nodes
            visited.add(state)
            fBest = fFunc
            # stop when finding point t
            if (state == t) :
                # if goal is found give the final action
                path = path + [(state, action)]
                outNode = (state,action,cost,path)
                goalFound = True
            # get all possible successor states, up to 4
            succStates = problem.getSuccessors(state)
            for succState in succStates :
                nextState, succAction, succCost = succState
                newNode = (nextState, succAction, cost + succCost, path + [(state, action)])
                # update the f function, state cost, actions
                # h(n,gr)
                hngr = heuristic(nextState, gr)
                # h(n,gf)
                hngf = heuristic(nextState, gf)
                # h(n,t)
                hnt = heuristic(nextState, t)
                if (hngr<hngf):
                    hnt = alpha * hnt
                newfFunc = cost + succCost + hnt
                if (newfFunc < math.inf) :
                    myqueue.update(newNode,newfFunc)

    # path of the outstate
    path = outNode[3]
    # give solution path if it exists
    if goalFound :      
        actions = [action[1] for action in path]
        del actions[0] 
    else :
        # give no action if solution does not exist (goal is walled off)
        print ("Oops, stuck and cannot find your goal!")
        actions = []
    return (outNode,actions)


def hillClimbingProcedureImprove(problem,startNode,heuristic):
    """Enforced Hill Climbing Procedure Improve,
     A buddy function to implement enforced hill
     climbing. performs breadth first search to
     find valleys
     
     input:
    &param problem, the problem of the game object, a search problem in this case
    &param startNode, (x,y), action, cost, path of starting node
    &param heuristic, the heuristic function intended to use
    
    output:
    &param outNode, the output node of (state,cost,action,path)
    """
    # FIFO queue
    myqueue = util.Queue()
    # goal position of maze (x,y)
    goalState = problem.goal
    # heuristic using manhattan distance, initiliase initial value
    hBest = heuristic(startNode[0], goalState)
    # push initial state into queue
    myqueue.push(startNode)
    # records the nodes already visited
    visited = set()

    #output node#
    outNode = startNode

    # While there are still nodes left to be expanded
    while not myqueue.isEmpty() :
        # node of interest
        node = myqueue.pop()
        state, action, cost, path = node
        # skips visited states
        if state not in visited :
            # fresh unexplored state
            visited.add(state)
            # heuristic of current state using manhatten distance
            hCur = heuristic(state, goalState)
            # return the node if its state has better heuristic
            if (hCur < hBest) :
                # if goal is found give the final action
                if problem.isGoalState(state) :
                    # final action to reach goal
                    path = path + [(state, action)]
                # return the better node anyways
                outNode = (state,action,cost,path)
                break
            # get all possible next states
            succStates = problem.getSuccessors(state)
            # update nodes with state cost and path and push into queue
            for succState in succStates :
                nextState, succAction, succCost = succState
                newNode = (nextState, succAction, cost + succCost, path + [(state, action)])
                myqueue.push(newNode)
    
    return outNode


def enforcedHillClimbing(problem, heuristic=manhattanHeuristic):
    """Enforced Hill Climbing algorithm, if cannot find one way to climb
       down the hill, revert back to breadth first search until a new valley
       is found, using the manhatten distance between current position and 
       the goal position as the heuristic
       
    input:
    &param problem, the problem of the game object, a search problem in this case
    &param heuristic, the heuristic function intended to use
    
    output:
    &param actions, the actions to reach goal, [] if cannot compute such
    """

    # starting position of maze (x,y)
    startState = problem.getStartState()
    # Initial State, (x,y), null action, cost=0, no path planned
    startNode = (startState, '', 0, [])
    # goal found?
    goalFound = True
    
    # Keep iterating until solution is found or hill cannot be improved
    while not problem.isGoalState(startNode[0]) :
        newNode = hillClimbingProcedureImprove(problem, startNode, heuristic)
        # if procedure cannot be improved by having the same state returned
        #  the goal cannot be found
        if newNode[0] is startNode[0]:
            goalFound = False
            break
        else:
            startNode = newNode

    path = startNode[3]
    # give solution path if found
    if goalFound :      
        actions = [action[1] for action in path]
        del actions[0] 
    else :
        # give empty actions and a warning message
        print ("Oops, stuck and cannot find your goal!")
        actions = []
    return actions


def idaStarProcedureSearch(problem,node,fBound,heuristic):
    """iterative deepening A* Search procedure improve, a
    buddy function to implement iterative A* Search.
    performs depth-first search within boundary of fBound
    using recursive mechanism
    uses manhatten distance between current state and goal state
    as heuristic

    input:
    &param problem, the problem of the game object, a search problem in this case
    &param node, (x,y), action, cost, path of starting node
    &param fBound, the threshold of f value for the current iteration
    &param heuristic, the heuristic function intended to use
    
    output:
    &param problem, the problem of the game object, a search problem in this case
    &param nextNode, the output node of (state,cost,action,path)
    &param fMin, the minimum f found greater than fBound
    """

    # current node to look at, starts at starting pos for first run
    state, action, cost, path = node
    # goal position of maze (x,y)
    goalState = problem.goal
    # f value, action cost + heuristic cost
    fFunc = cost + heuristic(state, goalState)
    # min f function found greater than fBound, initialise as inf
    fMin = math.inf

    # return the new fBound 
    if (fFunc > fBound) :
        return (problem,node,fFunc)
    # return the found goal 
    if problem.isGoalState(state) :
        return (problem,node,fFunc)
    # get all possible successor states, up to 4
    succStates = problem.getSuccessors(state) 
    for succState in succStates :
        nextState, succAction, succCost = succState
        newNode = (nextState, succAction, cost + succCost, path + [(state, action)])
        problem, nextNode, fNewBound = idaStarProcedureSearch(problem, newNode, fBound,heuristic)
        # return the found goal state and its node
        if problem.isGoalState(nextNode[0]) :
            return (problem, nextNode, fNewBound)
        # find the minimum f greater than fBound
        if (fNewBound < fMin) :
            fMin = fNewBound

    # return the minimum f beyond fBound, as well as the state 
    return (problem,nextNode,fMin)


def idaStarSearch(problem, heuristic=manhattanHeuristic):
    """iterative deepening A* Search ,
    A combination of A* heuristic and iterative deepening 
    Search, where the search depth boundaries is now
    defiend by the heuristic function f = state_cost+heuristic_cost
    
    input:
    &param problem, the problem of the game object, a search problem in this case
    &param heuristic, the heuristic function intended to use
    
    output:
    &param actions, the actions to reach goal, [] if cannot compute such
    """
    
    # starting position of maze (x,y)
    startState = problem.getStartState()
    # Initial Node, (x,y), null action, heuristic=0, no path planned
    startNode = (startState, '', 0, [])
    # goal position of maze (x,y)
    goalState = problem.goal
    # heuristic using manhattan distance, initiliase initial value
    hInitial = heuristic(startNode[0], goalState)
    # f initial is h initial, since g is 0 at start
    fBound = hInitial
    # default output path
    solPath = []

    # keep iterating until we know if solution is found or does not exist
    while True :
        problem, nextNode, fNext = idaStarProcedureSearch(problem,startNode,fBound,heuristic)
        # extract node state parameters
        nextState, nextAction, nextCost, nextPath = nextNode
        # extract path when goal is found
        if problem.isGoalState(nextState) :
            # if goal is found give the final action
            path = nextPath + [(nextState, nextAction)]
            solPath = [action[1] for action in path]
            del solPath[0]
            break
        # update the f Bound for next iteration of depth search
        fBound = fNext

    #print(solPath)
    return solPath
        


                
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ehc = enforcedHillClimbing
ida = idaStarSearch
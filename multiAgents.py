from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """

           
        # Begin your code (Part 1)
        def minimax(state, depth, agentIndex):
            #遞迴終止條件
            if state.isWin() or state.isLose() or depth==0:
                return self.evaluationFunction(state), None
            
            if agentIndex==0:
                bestVal = -float('inf')
                bestAct = None
                for action in state.getLegalActions(agentIndex):
                    nextState = state.getNextState(agentIndex, action)
                    value, _ = minimax(nextState, depth, 1)
                    if value>bestVal:
                        bestVal = value
                        bestAct = action
                return bestVal, bestAct
            else:
                bestVal = float('inf')
                bestAct = None
                for action in state.getLegalActions(agentIndex):
                    nextState = state.getNextState(agentIndex, action)
                    if agentIndex == state.getNumAgents()-1:
                        value, _ = minimax(nextState, depth-1, 0)
                    else:
                        value, _ = minimax(nextState, depth, agentIndex+1) 

                    if value<bestVal:
                        bestVal = value
                        bestAct = action
                return bestVal, bestAct
        return minimax(gameState, self.depth, 0)[1]


        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        def alphabeta(state, depth, agentIndex, alpha, beta):
            if(state.isWin() or state.isLose() or depth==0):
                return self.evaluationFunction(state), None
            
            if agentIndex==0:
                bestVal = -float('inf')
                bestAct = None
                for action in state.getLegalActions(agentIndex):
                    nextState = state.getNextState(agentIndex, action)
                    value, _ = alphabeta(nextState, depth, 1, alpha, beta)

                    if value>bestVal:
                        bestVal = value
                        bestAct = action

                    if bestVal>beta:
                        break

                    alpha = max(bestVal, alpha)
                return bestVal, bestAct
            else:
                bestVal = float('inf')
                bestAct = None
                for action in state.getLegalActions(agentIndex):
                    nextState = state.getNextState(agentIndex, action)
                    if (agentIndex== state.getNumAgents()-1):
                        value, _ = alphabeta(nextState, depth-1, 0, alpha, beta)
                    else:
                        value, _ = alphabeta(nextState, depth, agentIndex+1, alpha, beta)
                    
                    if value<bestVal:
                        bestVal = value
                        bestAct = action
                    
                    if bestVal<alpha:
                        break
                    
                    beta = min(beta, bestVal)
                return bestVal, bestAct
        
        alpha = -float('inf')
        beta = float('inf')
        _ , bestAct = alphabeta(gameState, self.depth, 0, alpha, beta)

        return bestAct            

                    

        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        def expectimax(state, depth, agentIndex):
            if(depth==0 or state.isWin() or state.isLose()):
                return self.evaluationFunction(state), None
            
            if(agentIndex==0):
                bestVal = -float('inf')
                bestAct = None
                for action in state.getLegalActions(agentIndex):
                    nextState = state.getNextState(agentIndex, action)
                    value, _ = expectimax(nextState, depth, 1)
                    if value>bestVal:
                        bestVal = value
                        bestAct = action
                return bestVal, bestAct
            else:
                expectVal = 0
                for action in state.getLegalActions(agentIndex):
                    nextState = state.getNextState(agentIndex, action)
                    if (agentIndex==state.getNumAgents()-1):
                        value,_ = expectimax(nextState, depth-1, 0)
                    else:
                        value,_ = expectimax(nextState, depth, agentIndex+1)
                    expectVal+=value
                expectVal /= len(state.getLegalActions(agentIndex)) 
                return expectVal, None
        
        _, act = expectimax(gameState, self.depth, 0)
        return act

                    
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhost = currentGameState.getGhostStates()

    WEIGHT_FOOD = 10.0
    WEIGHT_GHOST = 10.0
    WEIGHT_EDIBLE_GHOST = 100.0

    value = currentGameState.getScore()

    ghostValue = 0
    for ghost in newGhost:
        distance = manhattanDistance(newPos, newGhost[0].getPosition())
        if distance > 0:
            if ghost.scaredTimer > 0:  
                ghostValue += WEIGHT_EDIBLE_GHOST / distance
            else:  
                ghostValue -= WEIGHT_GHOST / distance
    value += ghostValue

    distancesToFood = [manhattanDistance(newPos, x) for x in newFood.asList()]
    if len(distancesToFood):
        value += WEIGHT_FOOD / min(distancesToFood)

    return value
    # End your code (Part 4)

# python autograder.py -q part4 --no-graphics
# Abbreviation
better = betterEvaluationFunction

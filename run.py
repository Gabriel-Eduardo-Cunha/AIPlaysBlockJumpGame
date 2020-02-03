from NeuralNetworkGameBlockJump import NeuralNetworkPopulation
import random
from blockJumpGame import BlockJumpGame

population = NeuralNetworkPopulation(1, 'gameblockjump', 50, 1, 40)

population.playGame(100, 'ada', True, 30)



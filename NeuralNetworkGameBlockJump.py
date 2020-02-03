import random
from NeuralNetwork import Network
from blockJumpGame import BlockJumpGame

class NeuralNetworkPopulation:
    def __init__(self, numOfSubjects = 1, populationName = 'noName', trainPerGeneration = 100, mutationRate = 0.1, samples = 100,  jsonOrModel = True, loadModel = False):
        self.trainPerGeneration = trainPerGeneration
        self.mutationRate = mutationRate
        self.samples = samples
        self.popName = populationName
        self.numOfSubjects = numOfSubjects
        if jsonOrModel == True:
            jsonOrModel = [True for _ in range(numOfSubjects)]
        
        self.subjects = [0 for x in range(numOfSubjects)]

        for i in range(numOfSubjects):
            self.subjects[i] = Network(jsonOrModel[i], loadModel)
            self.subjects[i].setLearningRate(0.4)

    def randomizeData(self):
        
        for i in range(self.numOfSubjects):
            for _ in range(self.samples):
                
                objectDistance = NeuralNetworkPopulation.randomBinaryArray(0, 200)
                objectWidth = NeuralNetworkPopulation.randomBinaryArray(1, 3)
                gameSpeed =  NeuralNetworkPopulation.randomBinaryArray(20, 100)
                # objectHeight = NeuralNetworkPopulation.randomBinaryArray(75, 150)
                input = objectDistance + objectWidth + gameSpeed
                randomizer = random.randint(0,2)
                if randomizer == 0:
                    output = [0,0]
                    meaning = 'None'
                elif randomizer == 1:
                    output = [1,0]
                    meaning = 'Up'
                else:
                    output = [0,1]
                    meaning = 'Down'
                self.subjects[i].insertData(input, output, meaning)

    def startPop(self):
        self.randomizeData()
        self.trainPop()

    def trainPop(self, attempts = 200):
        for i in range(len(self.subjects)):
            self.subjects[i].train(attempts)
            self.subjects[i].saveModel(self.popName + str(i))

    @staticmethod
    def randomBinaryArray(min, max):
        randomNumber = random.randint(min, max)
        array = list(0 for _ in range(len(bin(max)[2:]) - len(bin(randomNumber)[2:])))
        array.extend(list(int(x) for x in bin(randomNumber)[2:]))
        return array

    @staticmethod
    def DecToBinaryArray(num, arrayRange):
        array = list(0 for _ in range(arrayRange - len(bin(num)[2:])))
        array.extend(list(int(x) for x in bin(num)[2:]))
        return array


    @staticmethod
    def BinaryArrayToDec(array):
        string = '0b'
        for x in array: string += str(x)
        return int(string, 2)

    def mutatePop(self, model):
        for id in range(self.numOfSubjects):
            self.subjects[id] = Network(model)
            if id > 0:
                self.mutate(id)
                self.subjects[id].train(self.trainPerGeneration)
            self.subjects[id].saveModel(self.popName + str(id))
        
        
    def mutate(self, id):
        mutatedData = self.subjects[id].getData()
        for i in range(len(mutatedData['inputs'])):
            if random.randint(0, self.mutationRate ** -1) == 0:
                randomizer = random.randint(0,1)
                if randomizer == 0:
                    mutatedValue = NeuralNetworkPopulation.BinaryArrayToDec(mutatedData['inputs'][i][0:8]) + random.randint(-20,20)
                    if mutatedValue > 255: mutatedValue = 255
                    if mutatedValue < 0: mutatedValue = 0
                    mutatedData['inputs'][i][:8] = NeuralNetworkPopulation.DecToBinaryArray(mutatedValue, 8)
                elif randomizer == 1:
                    mutatedValue = NeuralNetworkPopulation.BinaryArrayToDec(mutatedData['inputs'][i][8:10]) + random.randint(-1,1)
                    if mutatedValue > 3: mutatedValue = 3
                    if mutatedValue < 1: mutatedValue = 1
                    mutatedData['inputs'][i][8:10] = NeuralNetworkPopulation.DecToBinaryArray(mutatedValue, 2)
                elif randomizer == 2:
                    mutatedValue = NeuralNetworkPopulation.BinaryArrayToDec(mutatedData['inputs'][i][10:17]) + random.randint(-5,5)
                    if mutatedValue > 127: mutatedValue = 127
                    if mutatedValue < 0: mutatedValue = 0
                    mutatedData['inputs'][i][10:17] = NeuralNetworkPopulation.DecToBinaryArray(mutatedValue, 7)
        
        for i in range(len(mutatedData['outputs'])):
            if random.randint(0,self.mutationRate ** -1) == 0:
                outputValue = random.randint(0,2)
                if outputValue == 0:
                    mutatedData['outputs'][i] = [0,0]
                    mutatedData['meanings'][i] = 'None'
                elif outputValue == 1:
                    mutatedData['outputs'][i] = [1,0]
                    mutatedData['meanings'][i] = 'Up'
                else:
                    mutatedData['outputs'][i] = [0,1]
                    mutatedData['meanings'][i] = 'Down'
        
        self.subjects[id]._data = mutatedData

    def playGame(self, generationsNumber = 1,startModel = False, renderGame = True, gameFPS = 20):
        if not startModel:
            self.startPop()
        else:
            self.mutatePop(startModel)
            
        betterId = BlockJumpGame.playGames(50, 'aitrain', self.numOfSubjects, gameFPS, self.popName, renderGame)
        self.subjects[betterId].saveModel('betterRobot')

        for generation in range(generationsNumber):
            print('Generation: ' + str(generation))
            self.mutatePop('betterRobot')
            betterId = BlockJumpGame.playGames(10, 'aitrain', self.numOfSubjects, gameFPS, self.popName, renderGame)
            self.subjects[betterId].saveModel('betterRobot')




    def getSubject(self, id):
        return self.subjects[id]
    
    def getAllSubjects(self):
        return self.subjects
    

        

import random,time

class HamiltonianPath:

    def __init__(self,numOfNodes):
        if numOfNodes > 0:
            self.numOfNodes = numOfNodes
        else:
            print("Error")

    def calculateMaxPairs(self):
        self.maxPairs = self.numOfNodes*(self.numOfNodes - 1)//2

    def formHP(self):
        self.hamiltonianPath = []
        while len(self.hamiltonianPath) != self.numOfNodes:
            randomNode = random.randint(1,self.numOfNodes)
            if randomNode not in self.hamiltonianPath:
                self.hamiltonianPath.append(randomNode)

    def generateHPPairs(self):
        self.formHP()

        self.hamiltonianPairs = []
        for x in range (len(self.hamiltonianPath)-1):
            pair = (self.hamiltonianPath[x], self.hamiltonianPath[x+1])
            self.hamiltonianPairs.append(pair)
        
        # print(self.hamiltonianPairs)
        # exit(0)
        self.generatePairs(self.hamiltonianPairs)

        random.shuffle(self.hamiltonianPairs)
        self.pairs = self.hamiltonianPairs
        # print('self.pairs', self.pairs)
        # exit(0)

    def generatePairs(self, pairs = []):
        self.calculateMaxPairs()
        self.pairs = pairs
        if self.numOfNodes >= 10:
            startRange = self.numOfNodes
            endRange = (self.numOfNodes - 10)*3 + 18
            numOfPairs = random.randint(startRange, endRange)
        else:
            numOfPairs = random.randint(self.numOfNodes - 1, self.maxPairs)
        print("Random total of pairs:", numOfPairs)

        while len(self.pairs) != numOfPairs:
            try:
                startNode = random.randint(1, self.numOfNodes)
                endNode = random.randint(1, self.numOfNodes)
                if startNode == endNode:
                    raise ValueError
            except ValueError:
                pass
            else:
                pair = (startNode, endNode)
                invertedPair = (endNode, startNode)
                if pair not in self.pairs and invertedPair not in self.pairs:
                    self.pairs.append(pair)

        print("Pairs:", self.pairs)
        # exit(0)

    def generatePathLink(self):
        self.graphLink = {}
        for x in self.pairs:
            x = str(x)
            splitNode = x.split(', ')
            a = int(splitNode[0][1:])
            b = int(splitNode[1][:-1])
            try:
                if b not in self.graphLink[a]:
                    self.graphLink[a].append(b)
            except KeyError:
                self.graphLink[a] = []
                self.graphLink[a].append(b)
            finally:
                try:
                    if a not in self.graphLink[b]:
                        self.graphLink[b].append(a)
                except KeyError:
                    self.graphLink[b] = []
                    self.graphLink[b].append(a)
                finally:
                    pass

        print("Graph linkage:", self.graphLink)


    def grasp(self):
        solutionList = []
        firstSolution = []
        previousStartNode = []

        tempNode = len(self.pairs)
        startNode = 0

        for start in range(1, len(self.graphLink)):
            if len(self.graphLink[start]) < tempNode:
                tempNode = len(self.graphLink[start])
                startNode = start

        firstSolution.append(startNode)
        previousStartNode.append(startNode)
        firstSearch = self.greedySearch(firstSolution)

        if firstSearch[0] == False:
            solutionList.append(firstSearch[1])

            for y in range(1, 101):
                randomIndex = random.randint(0,len(solutionList)-1)
                randomSolution = solutionList[randomIndex].copy()
                randomPosition = random.randint(1,len(randomSolution)-1)
                randomNum = random.randint(1, 3)
 
                if randomNum == 1: #remove second half
                    randomSolution = randomSolution[:randomPosition]

                elif randomNum == 2: #remove first half
                    randomSolution = randomSolution[randomPosition:]

                else:
                    randomSolution = self.restartSearch()

                newSearch = self.greedySearch(randomSolution)
                newSolution = newSearch[1]

                if newSearch[0]:
                    newBestSolution = newSolution
                    break

                if newSolution not in solutionList:
                    solutionList.append(newSolution)

                newBestSolution = max(solutionList, key = len)

            if len(newBestSolution) == numOfNodes:
                print("\nHamiltonian Path Found!\nHP:", newBestSolution)
                return [True,newBestSolution]

            else:
                print("\nBest Solution Found:", newBestSolution)
                print("\nLength of path:", len(newBestSolution))
                print("\nLength of solution list:",len(solutionList))
                return [False,newBestSolution]

        else:
            print("\nHamiltonian Path Found!\nHP:", firstSearch[1])
            return [True,firstSearch[1]]

    def isHamiltonianPathExist(self):
        time_start = time.clock()
        self.generatePathLink()
        print("Finding Hamiltonian Paths...")
        time.sleep(0.5)
        # print("self.graphLink) != self.numOfNodes:", self.graphLink)
        # print("self.graphLink) != self.numOfNodes:", self.numOfNodes)
        # exit(0)

        if len(self.graphLink) != self.numOfNodes:
            print("The graph is not connected.\nHence, there is no Hamiltoninan Paths.\n")
            time_elapsed = (time.clock() - time_start)
            return [-1, time_elapsed]
        else:
            result = self.grasp()
            time_elapsed = (time.clock() - time_start)
            if result[0]:
                print("Computing time:", round(time_elapsed, 2), "seconds\n")
                return [result[1], time_elapsed]
            else:
                print("Computing time:", round(time_elapsed, 2), "seconds\n")
                return [result[1], time_elapsed]

    def greedySearch(self, solution):
        newLastNode = solution[-1]
        while True:
            lastNode = solution[-1]
            possibleNode = self.graphLink[lastNode]
            random.shuffle(possibleNode)
            if len(solution) == self.numOfNodes:
                return (True, solution)
            else:
                for x in range(0, len(possibleNode)):
                    if possibleNode[x] not in solution:
                        solution.append(possibleNode[x])
                        newLastNode = possibleNode[x]
                        break
                if lastNode == newLastNode:
                    solution.reverse()
                    while True:
                        lastNode = solution[-1]
                        newLastNode = solution[-1]
                        possibleNode = self.graphLink[lastNode]
                        if len(solution) == self.numOfNodes:
                            return (True, solution)
                        else:
                            for x in range(0, len(possibleNode)):
                                if possibleNode[x] not in solution:
                                    solution.append(possibleNode[x])
                                    newLastNode = possibleNode[x]
                                    break
                            if lastNode == newLastNode:
                                return (False, solution)

    def restartSearch(self):
        randomStartNode = random.randint(1,self.numOfNodes)
        newSolution = []
        newSolution.append(randomStartNode)
        return newSolution

numOfNodes = 60
yes = 0
no = 0

def get_node(pairs_):
    nodes = []
    for p in pairs_:
        if p[0] not in nodes:
            nodes.append(p[0])
        if p[1] not in nodes:
            nodes.append(p[1])
    
    return nodes

if __name__ == "__main__":
    ##############
    # test
    # pa_s = [['1', '2'], ['2', '3'], ['3', '4'], ['4', '5'], ['5', '6'], ['6', '7'], ['7', '8'], ['1', '9'], ['2', '10'], ['3', '11'], ['4', '12'], ['5', '13'], ['6', '14'], ['7', '15'], ['8', '16'], ['9', '10'], ['10', '11'], ['12', '13'], ['13', '14'], ['14', '15'], ['15', '16'], ['9', '17'], ['10', '18'], ['11', '19'], ['12', '20'], ['14', '22'], ['15', '23'], ['16', '24'], ['17', '18'], ['19', '20'], ['20', '21'], ['21', '22'], ['23', '24'], ['17', '25'], ['19', '27'], ['20', '28'], ['22', '30'], ['24', '32'], ['25', '26'], ['26', '27'], ['28', '29'], ['29', '30'], ['30', '31'], ['31', '32'], ['25', '33'], ['26', '34'], ['27', '35'], ['28', '36'], ['29', '37'], ['31', '39'], ['32', '40'], ['33', '34'], ['34', '35'], ['36', '37'], ['37', '38'], ['38', '39'], ['39', '40'], ['33', '41'], ['34', '42'], ['35', '43'], ['36', '44'], ['37', '45'], ['38', '46'], ['39', '47'], ['40', '48'], ['41', '42'], ['42', '43'], ['43', '44'], ['44', '45'], ['46', '47'], ['47', '48'], ['41', '49'], ['42', '50'], ['43', '51'], ['45', '53'], ['46', '54'], ['48', '56'], ['49', '50'], ['51', '52'], ['52', '53'], ['54', '55'], ['55', '56'], ['49', '57'], ['50', '58'], ['51', '59'], ['52', '60'], ['53', '61'], ['54', '62'], ['55', '63'], ['56', '64'], ['57', '58'], ['58', '59'], ['59', '60'], ['60', '61'], ['61', '62'], ['62', '63'], ['63', '64']]

    # pa_s =[['1', '2'], ['2', '3'], ['3', '4'], ['4', '5'], ['5', '6'], ['1', '7'], ['2', '8'], ['3', '9'], ['4', '10'], ['5', '11'], ['6', '12'], ['7', '8'], ['8', '9'], ['9', '10'], ['10', '11'], ['11', '12'], ['7', '13'], ['8', '14'], ['9', '15'], ['10', '16'], ['11', '17'], ['12', '18'], ['13', '14'], ['14', '15'], ['15', '16'], ['16', '17'], ['17', '18'], ['13', '19'], ['14', '20'], ['15', '21'], ['16', '22'], ['17', '23'], ['18', '24'], ['19', '20'], ['20', '21'], ['21', '22'], ['22', '23'], ['23', '24'], ['19', '25'], ['20', '26'], ['21', '27'], ['22', '28'], ['23', '29'], ['24', '30'], ['25', '26'], ['26', '27'], ['27', '28'], ['28', '29'], ['29', '30'], ['25', '31'], ['26', '32'], ['27', '33'], ['28', '34'], ['29', '35'], ['30', '36'], ['31', '32'], ['32', '33'], ['33', '34'], ['34', '35'], ['35', '36']]
    pa = [[1, 9], [1, 2], [2, 10], [2, 3], [3, 11], [4, 12], [4, 5], [5, 13], [6, 7], [7, 8], [7, 15], [8, 16], [9, 10], [10, 11], [11, 19], [12, 20], [12, 12], [12, 13], [13, 14], [14, 22], [14, 15], [15, 16], [15, 23], [16, 24], [17, 25], [17, 18], [19, 27], [19, 20], [20, 28], [20, 21], [21, 22], [22, 30], [23, 24], [24, 32], [25, 33], [26, 34], [26, 27], [26, 26], [28, 36], [28, 28], [28, 29], [29, 30], [31, 32], [31, 39], [33, 41], [33, 34], [34, 35], [35, 43], [36, 44], [36, 37], [37, 45], [37, 38], [38, 46], [38, 38], [39, 40], [39, 47], [40, 48], [41, 42], [42, 50], [42, 43], [43, 44], [44, 45], [45, 53], [46, 46], [48, 56], [49, 57], [49, 50], [50, 58], [51, 59], [52, 60], [52, 52], [53, 61], [54, 62], [54, 55], [55, 56], [55, 63], [58, 59], [59, 60], [60, 61], [61, 62], [62, 63], [63, 64]]

    nodes = get_node(pa)
    print('nodes',nodes)
    print('nodes_length:', len(nodes))
    # pa =[[int(x[0]),int(x[1])] for x in pa_s]
    print('pairs:', pa)
    graph = HamiltonianPath(len(nodes))
    graph.pairs = pa
    output = graph.isHamiltonianPathExist()
    solution = output[0]
    # print(solution)
    if len(solution) == numOfNodes:
        yes += 1
    else:
        no += 1
    exit(0)
    ########


    loop_start_time = time.clock()
    for x in range(1,101):
        print(x)
        graph = HamiltonianPath(numOfNodes)
        graph.generateHPPairs()
        output = graph.isHamiltonianPathExist()
        solution = output[0]
        if len(solution) == numOfNodes:
            yes += 1
        else:
            no += 1

    loop_time_elapsed = (time.clock() - loop_start_time)
    print("Accuracy:", yes,"%")
    print("Time taken for 100 runs:", round(loop_time_elapsed, 2))
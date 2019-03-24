import random, time


class HamiltonianPath:

    def __init__(self, numOfNodes):
        if numOfNodes > 0:
            self.numOfNodes = numOfNodes
            self.pairs = None
        else:
            print("Error")

    def generatePathLink(self):
        # generate adjacent list
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

        # print("Graph linkage:", self.graphLink)

    def grasp(self):
        solutionList = []
        firstSolution = []
        previousStartNode = []

        tempNode = len(self.pairs)
        startNode = 0
        
        ## ugly code using index to go through the dict
#        for start in range(1, len(self.graphLink)):
#            print('start:', start)
#            print(self.graphLink[start])
#            if len(self.graphLink[start]) < tempNode:
#                
#                tempNode = len(self.graphLink[start])
#                startNode = start
        
        for key, value in (self.graphLink).items():
            if len(value) < tempNode:
                tempNode = len(value)
                startNode = key

        firstSolution.append(startNode)
        previousStartNode.append(startNode)
        firstSearch = self.greedySearch(firstSolution)

        # firstSearch: (False, [9, 1])
        # solutionList: [[x,x,x],[x,x,],...]
        if firstSearch[0] == False:
            solutionList.append(firstSearch[1]) # [[9, 1]]
            # 搜索次数设置
            for y in range(1, 101):
                randomIndex = random.randint(0, len(solutionList)-1) # 0
                randomSolution = solutionList[randomIndex].copy()  # [9, 1]

                if len(randomSolution) < 2:
                    continue
                # TODO 此处可能出现bug，有待验证

                randomPosition = random.randint(1, len(randomSolution)-1) # 1
                randomNum = random.randint(1, 3)
 
                # 随机策略 移除部分解
                if randomNum == 1:  # remove second half
                    randomSolution = randomSolution[:randomPosition] # 9

                elif randomNum == 2:  # remove first half
                    randomSolution = randomSolution[randomPosition:] # 1

                else:
                    # 重新选择起始搜索节点，randomSolution=[new node]
                    randomSolution = self.restartSearch()

                # 继续贪心算法搜索
                newSearch = self.greedySearch(randomSolution)
                newSolution = newSearch[1]

                if newSearch[0]:
                    # 找到HP时直接break
                    newBestSolution = newSolution
                    break

                if newSolution not in solutionList:
                    solutionList.append(newSolution)
                
                # 选择最长的作为最优替补解
                newBestSolution = max(solutionList, key = len)

            if len(newBestSolution) == self.numOfNodes:
                # print("\nHamiltonian Path Found!\nHP:", newBestSolution)
                return [True, newBestSolution]

            else:
                # print("\nBest Solution Found:", newBestSolution)
                # print("\nLength of path:", len(newBestSolution))
                # print("\nLength of solution list:",len(solutionList))
                return [False, newBestSolution]

        else:
            # print("\nHamiltonian Path Found!\nHP:", firstSearch[1])
            return [True, firstSearch[1]]

    def isHamiltonianPathExist(self):
        time_start = time.clock()
        # 生成邻接表
        self.generatePathLink()
        # print("Finding Hamiltonian Paths...")
#        time.sleep(0.5)
#        print("self.graphLink != self.numOfNodes:", (self.graphLink))
#        print("self.graphLink != self.numOfNodes:", self.numOfNodes)
        # exit(0)
        
        # 如果邻接表的长度不等于节点的个数，则报错
        if len(self.graphLink) != self.numOfNodes:
            print("The graph is not connected.\nHence, there is no Hamiltoninan Paths.\n")
            time_elapsed = (time.clock() - time_start)
            return [-1, time_elapsed]
        else:
            result = self.grasp()
            time_elapsed = (time.clock() - time_start)
            if result[0]:
                # print("Computing time:", round(time_elapsed, 2), "seconds\n")
                return [result[1], time_elapsed]
            else:
                # print("Computing time:", round(time_elapsed, 2), "seconds\n")
                return [result[1], time_elapsed]

    def greedySearch(self, solution):
        newLastNode = solution[-1]
        while True:
            lastNode = solution[-1]
            
            # 从邻接表导入指向节点列表
            possibleNode = self.graphLink[lastNode]
            random.shuffle(possibleNode)
            
            # 如果当前解的程度等于节点数，说明找到了HP
            if len(solution) == self.numOfNodes:
                return (True, solution)
            else:
                ## ugly code
#                for x in range(0, len(possibleNode)):
#                    if possibleNode[x] not in solution:
#                        solution.append(possibleNode[x])
#                        newLastNode = possibleNode[x]
#                        break
                for x in possibleNode:
                    if x not in solution:
                        solution.append(x)
                        newLastNode = x
                        break
                
                # 针对双向对的情况，反向之后继续搜索
                if lastNode == newLastNode:
                    solution.reverse()
                    while True:
                        lastNode = solution[-1]
                        newLastNode = solution[-1]
                        possibleNode = self.graphLink[lastNode]
                        if len(solution) == self.numOfNodes:
                            return (True, solution)
                        else:
                            ## ugly code
#                            for x in range(0, len(possibleNode)):
#                                if possibleNode[x] not in solution:
#                                    solution.append(possibleNode[x])
#                                    newLastNode = possibleNode[x]
#                                    break
                            for x in possibleNode:
                                if x not in solution:
                                    solution.append(x)
                                    newLastNode = x
                                    break 
                            
                            if lastNode == newLastNode:
                                return (False, solution)

    def restartSearch(self):
        # 从节点列表中重新选择起始搜索节点，返回[new_node]
#        randomStartNode = random.randint(1,self.numOfNodes)
        randomStartNode = random.choice(list((self.graphLink).keys()))
        
        newSolution = []
        newSolution.append(randomStartNode)
        return newSolution


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
    print('nodes', nodes)
    print('nodes_length:', len(nodes))
    # pa =[[int(x[0]),int(x[1])] for x in pa_s]
    print('pairs:', pa)
    graph = HamiltonianPath(len(nodes))
    graph.pairs = pa
    output = graph.isHamiltonianPathExist()
    solution = output[0]
    print('solution: ', solution)

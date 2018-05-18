import sys
import math
import pandas as pd

class Node():
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.total = 0
        self.above = 0


class decision():   
    myRootNode = Node(None)
    def start(self):
        #self.listOfAttributesAlreadyUsed = []
        self.attributes = ['workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'native-country', 'salaryLevel']
        filePathToTraining = sys.argv[1]
        filePathToTesting = sys.argv[2]
        method = sys.argv[3]
        #percentsToUse = [2, 10, 20, 30, 40, 50, 60]
        #for eachPercent in percentsToUse:
        percentToUse = sys.argv[4]
    
        if str(method) == 'vanilla':
            self.vanilla(filePathToTraining, filePathToTesting, percentToUse)
        if str(method) == 'depth':
            percentToUseValidation = sys.argv[5]
            maxDepth = sys.argv[6]
            self.depth(filePathToTraining, filePathToTesting, percentToUse, percentToUseValidation,  int(maxDepth))
        if str(method) == 'prune':
            valPercent = sys.argv[5]
            self.prune(filePathToTraining, filePathToTesting, percentToUse, valPercent)
    

    def prune(self, filePathToTraining, filePathToTesting, percentToUse, percentForValidation):
        rootNode = self.vanillaForPrune(filePathToTraining, filePathToTesting, percentToUse, percentForValidation)
        attributes = ('workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'native-country', 'salaryLevel')
        
        train = pd.read_csv(filePathToTraining, sep = ', ', quotechar='"', header = None, engine= 'python', names = attributes)
        #X = data[['workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'native-country']].as_matrix()
        #X = data.as_matrix()
        X = train
        size = len(X)
        #print X
        percentToUse = int(percentToUse)
        size *= percentToUse
        size /= 100
        X = X[:size]
        
        validationData = pd.read_csv(filePathToTraining, sep = ', ', quotechar='"', header = None, engine= 'python', names = attributes)
        valX = validationData
        sizeVal = len(valX)
        percentToUseVal = 100 - int(percentForValidation)
        sizeVal *= percentToUseVal
        sizeVal /= 100
        valX = valX[sizeVal:]

        #print rootNode.value
        rootNew = self.getCounts(rootNode, valX)
        #print rootNew.value
        global myRootNode
        myRootNode = rootNew
        self.rep(rootNew)
        #print myRootNode.value
        trainAcc = self.accuracy(myRootNode, X)
        print "Train set accuracy: " + str(trainAcc)


        dataTest = pd.read_csv(filePathToTesting, sep = ', ', quotechar='"', header = None, engine= 'python', names = attributes)
        Y = dataTest
        size = len(Y)
        copyY = Y.copy()
        #rootNode1 = self.makeTree(Y, Y['salaryLevel'], dataTest)
        testAcc = self.accuracy(myRootNode, copyY)
        print ("Test set accuracy: " + str(testAcc))

    def countNodes(self, node):
        if node.value in ['<=50K', ">50K"]:
            return 1
        else:
            x = self.countNodes(node.left)
            y = self.countNodes(node.right)
            return x + y + 1

    def rep(self, rootNode): 
        realNode = rootNode
        ourNode = rootNode
        if ourNode.value in ['<=50K', ">50K"]:
            if ourNode.value == '>50K':
                return ourNode.total - ourNode.above
            else:
                return ourNode.above
        else:
            error = self.rep(ourNode.left) + self.rep(ourNode.right)
            ourNode.above = ourNode.left.above + ourNode.right.above
            ourNode.total = ourNode.left.total + ourNode.right.total
            if error < min(ourNode.above, ourNode.total - ourNode.above):
                return error
            else:
                if ourNode.above > ourNode.total - ourNode.above:
                    ourNode.value = ">50K"
                    return ourNode.total - ourNode.above
                else:
                    ourNode.value = "<=50K"
                    return ourNode.above


    def vanillaForPrune(self, filePathToTraining, filePathToTesting, percentToUse, percentForValidation):
        attributes = ('workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'native-country', 'salaryLevel')
        data = pd.read_csv(filePathToTraining, sep = ', ', quotechar='"', header = None, engine= 'python', names = attributes)
        #X = data[['workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'native-country']].as_matrix()
        #X = data.as_matrix()
        X = data
        size = len(X)
        #print X
        percentToUse = int(percentToUse)
        size *= percentToUse
        size /= 100
        X = X[:size]
        #print X[4]
        #data = X[X[7] == '>50k']   
        copy = X.copy()
        rootNode = self.makeTree(X, X['salaryLevel'], data)
        return rootNode
        #nodes = self.getCounts(rootNode, valX)
        #trainAcc = self.accuracy(rootNode, copy)
        #print ("Training set accuracy: " + str(trainAcc))
        #dataTest = pd.read_csv(filePathToTesting, sep = ', ', quotechar='"', header = None, engine= 'python', names = attributes)
        #Y = dataTest
        #size = len(Y)
        #copyY = Y.copy()
        #rootNode1 = self.makeTree(Y, Y['salaryLevel'], dataTest)
        #testAcc = self.accuracy(rootNode, copyY)
        #print ("Test set accuracy: " + str(testAcc))

    def depth(self, filePathToTraining, filePathToTesting, percentToUseTraining, percentToUseValidation, maxDepth):
        attributes = ('workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'native-country', 'salaryLevel')
        data = pd.read_csv(filePathToTraining, sep = ', ', quotechar='"', header = None, engine= 'python', names = attributes)
        #X = data[['workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'native-country']].as_matrix()
        #X = data.as_matrix()
        X = data
        size = len(X)
        #print X
        percentToUse = int(percentToUseTraining)
        size *= percentToUse
        size /= 100
        X = X[:size]
        #print X[4]
        #data = X[X[7] == '>50k']   
        copy = X.copy()
        rootNode = self.makeTreeDepth(X, X['salaryLevel'], data, 0, maxDepth)
        trainAcc = self.accuracy(rootNode, copy)
        print ("Training set accuracy: " + str(trainAcc))

        dataTestZ = pd.read_csv(filePathToTraining, sep = ', ', quotechar='"', header = None, engine= 'python', names = attributes)
        Z = dataTestZ
        sizeZ = len(Z)
        percentToUseVal = 100 - int(percentToUseValidation)
        sizeZ *= percentToUseVal
        sizeZ /= 100
        Z = Z[size:]
        copyZ = Z.copy()
        #rootNode2 = self.makeTreeDepth(Z, Z['salaryLevel'], dataTestZ, 0, maxDepth)
        validationAcc = self.accuracy(rootNode, copyZ)
        print ("Validation set accuracy: " + str(validationAcc))

        dataTest = pd.read_csv(filePathToTesting, sep = ', ', quotechar='"', header = None, engine= 'python', names = attributes)
        Y = dataTest
        sizeY = len(Y)
        copyY = Y.copy()
        #rootNode1 = self.makeTreeDepth(Y, Y['salaryLevel'], dataTest, 0, maxDepth)
        testAcc = self.accuracy(rootNode, copyY)
        print ("Test set accuracy: " + str(testAcc))


    def vanilla(self, filePathToTraining, filePathToTesting, percentToUse):
        attributes = ('workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'native-country', 'salaryLevel')
        data = pd.read_csv(filePathToTraining, sep = ', ', quotechar='"', header = None, engine= 'python', names = attributes)
        #X = data[['workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'native-country']].as_matrix()
        #X = data.as_matrix()
        X = data
        size = len(X)
        #print X
        percentToUse = int(percentToUse)
        size *= percentToUse
        size /= 100
        X = X[:size]
        #print X[4]
        #data = X[X[7] == '>50k']   
        copy = X.copy()
        rootNode = self.makeTree(X, X['salaryLevel'], data)
        trainAcc = self.accuracy(rootNode, copy)
        print ("Training set accuracy: " + str(trainAcc))
        dataTest = pd.read_csv(filePathToTesting, sep = ', ', quotechar='"', header = None, engine= 'python', names = attributes)
        Y = dataTest
        size = len(Y)
        copyY = Y.copy()
        #rootNode1 = self.makeTree(Y, Y['salaryLevel'], dataTest)
        testAcc = self.accuracy(rootNode, copyY)
        print ("Test set accuracy: " + str(testAcc))

        
        
        #self.makeTree(X, data[data[7])
    def majority(self, data, target):
        counts = {}
        for i, row in data.iterrows():
            #print row
            if row[-1] in counts:
                counts[row['salaryLevel']] += 1.0
            else:
                counts[row['salaryLevel']] = 1.0
        maxVal = 0
        majority = ""
        for individualKey in counts.keys():
            if counts[individualKey] > maxVal:
                maxVal = counts[individualKey]
                majority = individualKey
        return majority

    def entropy(self, data, target):
        counts = {}
        counts = data['salaryLevel'].value_counts()
        #print counts
        summation = 0.0

        for vals in counts:
            if len(counts) <= 1:
                return 0
            prob = float(vals) / len(data)
            summation += ((-1) * (prob * math.log(prob, 10)))
        return summation

    def informationGain(self, data, attributeIndex, target):
        counts = {}
        #print attributeIndex
        #print data
        #print type(attributeIndex)
        #print 'hi'
        #print self.attributes[attributeIndex]
        # print data[self.attributes]
        #print data
        values = data[attributeIndex].unique() #self.getValues(data, attributeIndex)
        values = list(values)
        bestValue = values[0]
        maxInfoGain = float("-inf")
        for singleValue in values:
            entropy = self.entropy(data, target)
            subset0 = data[data[attributeIndex] == singleValue]
            subset1 = data[data[attributeIndex] != singleValue]
            entropy -= (float(len(subset0)) / len(data) * self.entropy(subset0, target))
            entropy -= (float(len(subset1)) / len(data) * self.entropy(subset1, target))

            if entropy > maxInfoGain:
                maxInfoGain = entropy
                bestValue = singleValue
        return maxInfoGain, bestValue
    
    def getValues(self, data, attributeIndex):
        values = []
        for index, entry in data.iterrows():
            if (entry[attributeIndex] not in values):
                values.append(entry[attributeIndex])
        return values

    def bestAttribute(self, data, target):
        maxBest, bestValueToSplit = float("-inf"), ""
        index = 0
        columnValues = list(data.columns.values)
        columnValues.remove('salaryLevel')
        for columns in columnValues:
            #if i in 
            currGain, valueToSplit = self.informationGain(data, columns, target)
            if (currGain >= maxBest):
                maxBest = currGain
                bestValueToSplit = valueToSplit
                index = columns
        if maxBest <= 0.0:
            return self.majority(data, target), 20
        #if maxBest > 0.0:
            #return self.majority(data, target)
        return bestValueToSplit, index
        #else:
            #return self.majority(data, target)

    def makeTree(self, data, target, oldData):
        listOfAttributesAlreadyUsed = []
        rows, columns = data.shape  
        #print columns
        #print "HELLO"
        valuesInTargetAttribute =  data['salaryLevel'].unique()
        #target = data[columns - 1]
        #print data
        if len(valuesInTargetAttribute) == 1:
            root = Node(valuesInTargetAttribute[0])
            return root
        if len(data) <= 0 or columns <= 1:
            root = Node(self.majority(oldData, target))
            return root
        

        valueToSplit, index = self.bestAttribute(data, target)
        if index == 20:
            root = Node(self.majority(data, target))
            return root
        listOfAttributesAlreadyUsed.append(index)
        root = Node(valueToSplit)
        oldData = data
        rightData = data[data[index] != valueToSplit]
        leftData = data[data[index] == valueToSplit]
        leftData = leftData.drop(str(index), axis = 1)
        root.left = self.makeTree(leftData, target, oldData)
        root.right = self.makeTree(rightData, target, oldData)
        return root 
    
    def makeTreeDepth(self, data, target, oldData, depth, maxDepth):
        listOfAttributesAlreadyUsed = []
        rows, columns = data.shape  
        valuesInTargetAttribute =  data['salaryLevel'].unique()
    
        if len(valuesInTargetAttribute) == 1:
            root = Node(valuesInTargetAttribute[0])
            return root
            #return valuesInTargetAttribute[0]
        if len(data) <= 0 or columns <= 1:
            root = Node(self.majority(oldData, target))
            #return self.majority(oldData, target)
            return root
    
        valueToSplit, index = self.bestAttribute(data, target)
        if index == 20:
            root = Node(self.majority(data, target))
            return root
        
        if depth == maxDepth:
            root = Node(self.majority(data, target))
            return root
        #print valueToSplit
        listOfAttributesAlreadyUsed.append(index)
        #attributes = ['workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'native-country', 'salaryLevel']
        #print valueToSplit
        root = Node(valueToSplit)
        oldData = data
        #att = self.attributes[index]
        #print valueToSplit
        rightData = data[data[index] != valueToSplit]
        leftData = data[data[index] == valueToSplit]
        #print leftData[3]
        leftData = leftData.drop(str(index), axis = 1)
        #leftData.drop(leftData.columns[[index]], axis = 1, inplace = True)
        #print leftData
        depth += 1
        root.left = self.makeTreeDepth(leftData, target, oldData, depth, maxDepth)
        #print "sjdfsf"
        root.right = self.makeTreeDepth(rightData, target, oldData, depth, maxDepth)
        return root 
    
    def getCounts(self, rootNode, dataSet):
        total = 0
        above = 0
        flag = False
        size = len(dataSet)
        #print rootNode
        for index, i in dataSet.iterrows():
            rootTree = rootNode
            while rootTree.value not in ['<=50K', ">50K"]:
                flag = False
                for allValues in i:
                    if allValues == rootTree.value:
                        rootTree = rootTree.left
                        flag = True
                        break
                if flag == False:
                    rootTree = rootTree.right
            rootTree.total += 1
            if (i[8] == ">50K"):
                rootTree.above += 1
        return rootNode

    def accuracy(self, rootNode, dataSet):
        tp = 0
        flag = False
        size = len(dataSet)
        #print rootNode
        for index, i in dataSet.iterrows():
            rootTree = rootNode
            
            while rootTree.value not in ['<=50K', ">50K"]:
                flag = False
                for allValues in i:
                    if allValues == rootTree.value:
                #if i[()] == rootTree.value:
                        rootTree = rootTree.left
                        flag = True
                        break
                if flag == False:
                    rootTree = rootTree.right
            if rootTree.value == i[8]:
                tp += 1
        accuracy = tp*1.0/len(dataSet)
        return accuracy

    
D = decision()
D.start()

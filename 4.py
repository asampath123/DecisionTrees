import numpy
import math
import statistics
from numpy.core.records import record

class Node:

    def __init__(self, value, value1):
        self.left = None
        self.data = value
        self.label = value1
        self.right = None
        self.dict = {}

class Tree:

    def createNode(self, data, label):

        return Node(data, label)

    def insert(self, node , data, label):

        if node is None:
            return self.createNode(data, label)
        # if data is smaller than parent , insert it into left side
        for d in data:
            if d < node.data:
                node.left = self.insert(node.left, data, label)
            elif d > node.data:
                node.right = self.insert(node.right, data, label)

        return node


    def search(self, node, data):

        if node is None or node.data == data:
            return node

        if node.data < data:
            return self.search(node.right, data)
        else:
            return self.search(node.left, data)



    def deleteNode(self,node,data):

        if node is None:
            return None

        if data < node.data:
            node.left = self.deleteNode(node.left, data)
        elif data > node.data:
            node.right = self.deleteNode(node.right, data)
        else:
            if node.left is None and node.right is None:
                del node
            if node.left == None:
                temp = node.right
                del node
                return  temp
            elif node.right == None:
                temp = node.left
                del node
                return temp

        return node

    
    
def extractData(fileName):
    print("extracting file")
    file = open(fileName, 'r')
    traindata=[]
    print ("Filepath is:" + file.name)
    i=0;
    for everyLine in file:
         
        if not everyLine.strip() =='':
            if i==0:
                attributeTitle = everyLine.strip().split(",")
                classAttribute = attributeTitle[-1]
                i+=1
            else:
                values=everyLine.strip().split(",")
                #values=list(map(float, values))
                #values = map(int, values)
                traindata.append(dict(zip(attributeTitle,values)))
            
    #print(attributeTitle)
    #print(classAttribute)
    #print(traindata) 
    
    return traindata,attributeTitle,classAttribute


def frequentClassified(classValues):
    highestClass=None
    freqCount=0
    
    
    for item in classValues:
        if classValues.count(item) > freqCount:
            highestClass = item
            freqCount = classValues.count(item)
            
            
    return highestClass        

def entropy(subset,classAttribute):
    #print()
    frequencyList = {}
    entropyVal = 0.0

    # Calculate the frequency of each of the values in the target attr
    for item in subset:
        if (item[classAttribute] in frequencyList):
            frequencyList[item[classAttribute]] += 1.0
        else:
            frequencyList[item[classAttribute]] = 1.0
    # incomplete entropy function
    
    for freq in frequencyList.values():
        entropyVal = entropyVal + (-freq/len(subset)) * math.log(freq/len(subset), 2) 
    
    
    #print("entropy is",entropyVal)    
    return entropyVal
    


def informationGain(traindata,attributeTitle,classAttribute):
    frequencyList={}
    avgEntropy=0.0
   
    for item in traindata:
        #print(item)
        #print(attributeTitle)
        if(item[attributeTitle] in frequencyList):
            frequencyList[item[attributeTitle]] = frequencyList[item[attributeTitle]]+1.0
        else:
            frequencyList[item[attributeTitle]] = 1.0
    #print("flist is",frequencyList)        
            
    for each in frequencyList.keys():
        prob=frequencyList[each]/sum(frequencyList.values())
        subset = [item for item in traindata if item[attributeTitle] == each]
        avgEntropy=avgEntropy +prob * entropy(subset, classAttribute)
    #print("avg entropy is",avgEntropy)    
    #print("gain is",entropy(subset,classAttribute)-avgEntropy)
    #print("avgEntropy",avgEntropy)
    #print("entropy",entropy(traindata,classAttribute))
    return (entropy(traindata,classAttribute)-avgEntropy)    
    
    
            
    #print(frequencyList)        
    

def pickBest(traindata,attributeTitle,classAttribute):
    highestGain=0.0
    bestAttribute=None
    #print(attributeTitle)
    for item in attributeTitle:
        #print("attr is",item)
        gain=informationGain(traindata,item,classAttribute)
        #print(gain)
        if (gain >= highestGain and item != classAttribute):
            
            highestGain = gain
            #print("highest gain is",highestGain)
            bestAttribute = item
    
    
    print("best is",bestAttribute)
    print("highest gain is",highestGain)            
    return bestAttribute    

def uniqueFunction(lst):
    """
    Returns a list made up of the unique values found in lst.  i.e., it
    removes the redundant values in lst.
    """
    lst = lst[:]
    unique_lst = []

    # Cycle through the list and add each value to the unique list only once.
    for item in lst:
        if unique_lst.count(item) <= 0:
            unique_lst.append(item)
            
    # Return the list with all redundant values removed.
    return unique_lst


def get_values(data, attr):
    """
    Creates a list of values in the chosen attribut for each record in data,
    prunes out all of the redundant values, and return the list.  
    """
    data = data[:]
    #print("get values function")
    #print(attr)
    #for record1 in data:
        #print(record1)
#     print([record[attr] for record in data])
    unique_lst = ([record[attr] for record in data])
    unique_lst=list(map(float, unique_lst))
    return unique_lst
        
def get_examples(data, attr, value):
    """
    Returns a list of all the records in <data> with the value of <attr>
    matching the given value.
    """
    data = data[:]
    rtn_lst = []
        
    if not data:
        return rtn_lst
    else:
        record = data.pop()
        if record[attr] == value:
            rtn_lst.append(record)
            rtn_lst.extend(get_examples(data, attr, value))
            return rtn_lst
        else:
            rtn_lst.extend(get_examples(data, attr, value))
            return rtn_lst    

def get_lesser(data, attr, value):
    """
    Returns a list of all the records in <data> with the value of <attr>
    matching the given value.
    """
    data = data[:]
    rtn_lst = []
        
    if not data:
        return rtn_lst
    else:
        record = data.pop()
        #print("record is",record)
        if float(record[attr]) < value:
            #print("value of float(record[attr]) is",float(record[attr]))
            rtn_lst.append(record)
            rtn_lst.extend(get_lesser(data, attr, value))
            return rtn_lst
        else:
            rtn_lst.extend(get_lesser(data, attr, value))
            return rtn_lst
        
def get_greater(data, attr, value):
    """
    Returns a list of all the records in <data> with the value of <attr>
    matching the given value.
    """
    data = data[:]
    rtn_lst = []
        
    if not data:
        return rtn_lst
    else:
        record = data.pop()
        if float(record[attr]) >= value:
            rtn_lst.append(record)
            rtn_lst.extend(get_greater(data, attr, value))
            return rtn_lst
        else:
            rtn_lst.extend(get_greater(data, attr, value))
            return rtn_lst        



def buildTree(traindata,attributeTitle,classAttribute):
    #print("buildTree")
    classValues=[]
    unique_lst = []
    list1=[]
    list2=[]
    for item in traindata:
        classValue = item[classAttribute]
        classValues.append(classValue)
    print("frequentClassified(classValues)",frequentClassified(classValues))    
    #print(classValues)
    #print(frequentClassified(classValues))
    
    
    if (len(attributeTitle) - 1) <= 0 or not traindata:
        return frequentClassified(classValues)
    
    elif len(classValues)== classValues.count(classValues[0]) :
        return classValues[0]
    else:
        bestAtrribute = pickBest(traindata,attributeTitle,classAttribute)
        
        unique_lst = ([record[bestAtrribute] for record in traindata])
        #print(unique_lst)
        unique_lst=list(map(float, unique_lst))
        #print(unique_lst)
        medianVal=statistics.median(unique_lst)
        print("median is",medianVal)
        
    
        list1=get_lesser(traindata, bestAtrribute, medianVal)
        list2=get_greater(traindata, bestAtrribute, medianVal)   
        #print(list1)
        #print(list2) 
        
        tree=Tree()
        node=Node(medianVal,bestAtrribute)
        #subtree = buildTree(get_examples(traindata, bestAtrribute, val),[attr for attr in attributeTitle if attr != bestAttributeList],classAttribute)
        #tree.insert(node, unique_lst, bestAtrribute)
    
    #subtree=buildTree(traindata,attributeTitle,classAttribute)
    #for attr in attributeTitle:
    
    
    
    
            # Create a subtree for the current value under the "best" field
        
            #print(subtree)
            # Add the new subtree to the empty dictionary object in our new
            # tree/node we just created.
        

    return tree
    #print("done")
    #return tree
        
         
    #incomplete            
    #get the best attribute and build the subtree
                 
def traverseDecisionTree(item, tree):
    
    # If leaf, return
    if type(tree) == type("string"):
        return tree

    #recurse till leaf
    else:
        attribute= list(tree)[0]
        #print("classification attr is",attr)
        tempTree = tree[attribute][item[attribute]]
        #print("t is",tree)
        return traverseDecisionTree(item, tempTree)

def print_tree(tree, str):
    """
    This function recursively crawls through the d-tree and prints it out in a
    more readable format than a straight print of the Python dict object.  
    """
    if type(tree) == dict:
        print ("%s%s" % (str, list(tree)[0]))
        #for item in tree.values()[0].keys():
        for item in list(tree.values())[0]:
            print ("%s\t%s" % (str, item))
            print_tree(list(tree.values())[0][item], str + "\t")
    else:
        print ("%s\t->\t%s" % (str, tree))    
     
if __name__ == "__main__":
    
    
    traindata,attributeTitle,classAttribute=extractData("D://Spring 2016//DM//iris//iris1.data.txt")
    bestAttributeList=[]
    tree=buildTree(traindata,attributeTitle,classAttribute)
    print(tree)
    
    
    
    
    
    testdata,attributeTitle,classAttribute=extractData("D://Spring 2016//DM//iris//iris3.data.txt")
    testclassification=[]
    #for item in testdata:
    #    testclassification.append(traverseDecisionTree(item, tree))
    #classification = classify(tree, data)
    #for item in testclassification:
    #    print(item)
    #print(tree)  
    #print_tree(tree,"")    
    
    
    
    
    
        
    
    
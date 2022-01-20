#!/usr/bin/env python
# coding: utf-8

from tabulate import tabulate


class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur

    def disp(self, ind=1):
        print("  " * ind, self.name, " ", self.count)
        for child in self.children.values():
            child.disp(ind + 1)


def createTree(dataSet, minSup=1):
    headerTable = {}

    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    for k in list(headerTable):
        if headerTable[k] < minSup:
            del headerTable[k]
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0:
        return None, None
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]

    retTree = treeNode("Null Set", 1, None)
    for tranSet, count in dataSet.items():
        localD = {}
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [
                v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)
            ]
            updateTree(orderedItems, retTree, headerTable, count)
    return retTree, headerTable


def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)


def updateHeader(nodeToTest, targetNode):
    while nodeToTest.nodeLink != None:
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def loadSimpDat():
    simpDat = [
        ["Milk", "Onion", "Nutmeg", "Kidney Beans", "Eggs", "Yogurt"],
        ["Dill", "Onion", "Nutmeg", "Kidney Beans", "Eggs", "Yogurt"],
        ["Milk", "Apple", "Kidney Beans", "Eggs"],
        ["Milk", "Unicorn", "Corn", "Kidney Beans", "Yogurt"],
        ["Corn", "Onion", "Onion", "Kidney Beans", "Ice cream", "Eggs"],
    ]
    return simpDat


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict


simpDat = loadSimpDat()

print("\nDataset: \n", simpDat)

initSet = createInitSet(simpDat)

print("\nDataset after using frozenset: \n", initSet)

myFPtree, myHeaderTab = createTree(initSet, 3)

print("\nItems satisfying minsup threshold:\n")
itemList = []
for i in myHeaderTab.keys():
    itemList += [[i, str(myHeaderTab[i][0])]]
print(tabulate(itemList, headers=["Items", "Frequency"], tablefmt="fancy_grid"))


def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


def findPrefixPath(basePat, treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats


print("\nFP Tree:\n")
myFPtree.disp()
print("\nConditional Patterns in FP Tree for 'Onion':\n")
print(findPrefixPath("Onion", myHeaderTab["Onion"][1]))

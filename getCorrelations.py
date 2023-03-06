import numpy as np
import itertools
import time

path = "./DNA/pBluescript.txt"

def getProbabilities(pathToInputText):
    file = open(pathToInputText)
    text = file.read()
    file.close()

    keys = [x for x in set(text)]
    symbolCounts = np.array([text.count(x) for x in set(text)])
    probabilities = dict(zip(keys,symbolCounts/sum(symbolCounts)))

    return probabilities


def createPermutations(length):
    base = "AAAATTTTCCCCGGGG" # Allows for all possible permutations of 4 basepairs in a string of 4. 

    ## [Generate Permutations of "ATCG" of all possible lengths]
    permutations = {''.join(permute) for permute in set(itertools.product(base,repeat=length))}

    return permutations

def getEntropies(pathToInputText,CorrelationLengths):
    file = open(pathToInputText)
    text = file.read()
    file.close()
    generalEntropyList = []

    # Count the correlations in text.
    for correlation in range(1,CorrelationLengths+1):
        correlationDictionary = {}
        possiblePermutations = createPermutations(correlation)

        # Sample the text and count occurences
        for textPosition in range(len(text)):
            sample = text[textPosition:textPosition+correlation]
            if sample in possiblePermutations:
                correlationDictionary[sample] = correlationDictionary.get(sample,0) + 1
        
        generalEntropyList.append(correlationDictionary)

        # Sum up all the values of each permute
        sum = 0
        for permute in possiblePermutations:
            if permute in correlationDictionary:
                sum += correlationDictionary[permute]
        
        for key, value in correlationDictionary.items():
            correlationDictionary[key] = value/sum
    
    ## Calculate entropies of each m-length subsequence. blockEntropies[0] => m = 0
    blockEntropies = []
    for permutationDictionary in generalEntropyList:
        probabilityOfOccurence = list(permutationDictionary.values())
        entropy = 0
        for probability in probabilityOfOccurence:
            entropy += -probability*np.log2(probability)
        blockEntropies.append(entropy)

    return blockEntropies

def getCorrelations(blockEntropies):
    correlations = [] # K0 = 0 always
    for m in range(len(blockEntropies)):
        if m == 0:
            kValue = 0 ## nSymbols = 4
        elif m == 1:
            kValue = np.log2(4) - blockEntropies[0]
        else:
            kValue = 2*blockEntropies[m-1] - blockEntropies[m] - blockEntropies[m-2]
        correlations.append(kValue)

    return correlations


def wrapper(pathToInputText,length):
    entropies = getEntropies(pathToInputText,length)
    correlations = getCorrelations(entropies)
    #entropies = entropies[0:len(entropies)-1]
    return entropies, correlations   


print(wrapper(path,5))

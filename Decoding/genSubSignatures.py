#Author : Harshit
"""
Given Orignal Subsignature and uncertainity array, generate all possible subsignatures
"""

def combineUncertainity(orignalSubSign, uncertainity):
    """
    Generate 2^(len(uncertainity)) subsignatures

    Parameters : 

        originalSubSignature ([int]): Original SubSignature based on Rounding

        uncertainity ([(int, int)]): array of tuple containing index and possible value 

    Return :

        [str]: Array of possible subsignatures
    """
    result = []
    subSign = orignalSubSign.copy()
    util(subSign, uncertainity, 0, result)
    print(result)
    return result

def util(subSign, uncertain, index, result):
    if(index >= len(uncertain)):
        return
    
    untouch = subSign.copy()
    result.append(untouch)
    util(untouch, uncertain, index+1, result)

    swapped = subSign.copy()
    swapped[uncertain[0]] = uncertain[1]
    util(swapped, uncertain, index+1, result)
#author : Harshit
import math

def hashReducer(masterSignature, length, radix = 8):
    """
    Using master signature to generate sub-signature for Label for different label versions.

    hashReducer uses Master Signature to generate sub-signature that can be used with different label versions,
    return will be sub-signature string or None if implementation doesn't exist.

    Parameters:

        signature (str): Master Signature that is to be reduced.

        length (int): Length of sub-signature generated.

        radix (int): base of each digit in sub-signature, less than equal to 10.

    Return:

        (str): Sub-signature
    """

    if type(masterSignature) == str:

        #v2 signature Implementation, length = 21, radix = 8
        if (length == 21 and radix == 8):
            masterlength = len(masterSignature)
            grouplength = math.ceil(masterlength/length)

            extralength = grouplength*length

            #append extralength-masterlength number of character from beginning of masterSignature.
            padding = masterSignature[:(extralength-masterlength+1)]
            modifSignature = masterSignature + padding

            #now modifSignature is evenly divisible by length
            subSignature = ""
            for i in range(length):
                num = 0
                for j in range(i, i+grouplength):
                    num += ord(modifSignature[j]) - ord('0')

                subSignature += str(num%radix)

            return subSignature

        else:
            return None

    else:
        return None
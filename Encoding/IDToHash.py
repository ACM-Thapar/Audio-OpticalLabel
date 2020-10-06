# Will use SHA256 % 10 element wise for development purposes
import hashlib

def generateHash(audioId=str):

    """
    This function takes audioId as input and returns a 64 character digest.

    Also known as Signature for Audio Optical Label
    which will be unique for each audio or song.
    
    Parameters:

        audioId (str): A 18-22 character long unique Audio ID.

    Return:

        (str): A 64 character long Signature.
    """
    if(type(audioId) == str):
        m = hashlib.sha256()
        m.update(bytes(audioId, "UTF-8"))
        digestr16 = m.hexdigest()
        digestr10 = ""
        for c in digestr16:
            if (c <= '9' and c >= '0'):
                digestr10 += c
            else:
                asc = ord(c)
                asc -= 17
                digestr10 += str(asc)
        return digestr10
    else:
        return None

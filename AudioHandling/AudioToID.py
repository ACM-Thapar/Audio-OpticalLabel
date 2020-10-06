# Code reference from Hitesh's ipynb
# Module Author : Harshit and Hitesh

import numpy as np
import glob
import librosa as lr

def generateAudioID(path=str, length=20):
    """
        This function takes path to audio file in .wav format and outputs AudioID for that Audio.

        This function breaks the audio in segments=``length`` and performs rms of Apmlitude vs Time of
        each segment and maps it into [0-9A-Z] which is a character of AudioID.

        Parameters:

            path (str): Specifies the path of Audio File (.wav format).
            
            length (int): Specifies AudioID length (default is 20).

        Return:

            (str) : The AudioID corresponding to given Audio.
    """
    audio_file = glob.glob(path)

    #File not Found
    if len(audio_file) == 0:
        print(f"Error : File not found : {path}")
        return None
    
    # Reading our audio file.
    audio , _ = lr.load(audio_file[0])

    start = 0
    stop = len(audio)/length -1


    # array storing root mean square values of all segments.
    rms = np.zeros(length)



    for i in range(0,length):

        #Segmented time and audio.
        updated_audio = audio[int(start):int(stop)]


        #Appending RMS value.
        square = np.square(updated_audio)
        mean = np.mean(square)
        root = np.sqrt(mean)
        rms[i] = root


        #Modifying start stop values.
        start = stop + 1
        stop = (len(audio)/length)*(i+2) - 1
        
        
    #100 seems arbitrary, will rectify later in later version   
    result = rms*100

    # Corrosponding ASCII value for each segment.
    result = result%36 + 65 

    result = result.astype(int)

    for i in range(0,len(result)):

        if result[i] > 90:
            result[i] = 47 + (result[i] - 90) 


    string = ""
    for value in result:
        string = string + chr(value)

    return string
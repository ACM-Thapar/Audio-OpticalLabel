import AudioHandling.AudioToID as AudioID
import Encoding.IDToHash as Hash
import LabelGen.v2.bindLogo as Labelgen
import os


if __name__ == "__main__":
    #Testing modules
    aid =  AudioID.generateAudioID("Misc/TestData/Taki Taki Ft Selena Gomez - DJ Snake (DJJOhAL (mp3cut.net).wav")
    print("AudioID : " + str(aid))
    sign = Hash.generateHash(aid)
    print("Audio Signatrue : " + str(sign))

    Labelgen.bindCompanyLogo(os.getcwd()+"/Misc/assets/acm_logo.png", 120, os.getcwd()+"/LabelGen/v2/output/LabelStage2.png")
    pass


import AudioHandling.AudioToID as AudioID
import Encoding.IDToHash as Hash
import Encoding.hashReducer as hr
import LabelGen.v2.bindLogo as Labelgen
import LabelGen.v2.plotter as plt
import os


if __name__ == "__main__":
    #Testing modules
    aid =  AudioID.generateAudioID("Misc/TestData/Taki Taki Ft Selena Gomez - DJ Snake (DJJOhAL (mp3cut.net).wav")
    print("AudioID : " + str(aid))
    sign = Hash.generateHash(aid)
    print("Audio Signatrue : " + str(sign))
    v2Sign = hr.hashReducer(sign, 21)
    print("v2 AudioLabel Signature : " + v2Sign)

    plt.plotDatapoints("LabelGen/v2/output/LabelStage2.png", f"LabelGen/v2/output/{v2Sign}.png", v2Sign)

    Labelgen.bindCompanyLogo(os.getcwd()+"/Misc/assets/acm_logo.png", 120, os.getcwd()+"/LabelGen/v2/output/LabelStage2.png")
    pass


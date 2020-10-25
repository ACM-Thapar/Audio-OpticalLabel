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

    Labelgen.bindCompanyLogo("Misc/assets/multimediaQR.png", 120, f"LabelGen/v2/output/{v2Sign}.png")

    plt.plotDatapoints(f"LabelGen/v2/output/{v2Sign}.png", f"LabelGen/v2/output/{v2Sign}.png", v2Sign)
    pass


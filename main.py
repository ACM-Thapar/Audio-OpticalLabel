import AudioHandling.AudioToID as AudioID
import Encoding.IDToHash as Hash


if __name__ == "__main__":
    #Testing modules
    aid =  AudioID.generateAudioID("AudioHandling/TestData/01 (mp3cut.net).wav")
    print(aid)
    sign = Hash.generateHash(aid)
    print(sign)
    pass


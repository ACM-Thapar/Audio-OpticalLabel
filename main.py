import AudioHandling.AudioToID as AudioID
import Decoding.v2ImageToSubSign as ImageRecognizer
import Encoding.IDToHash as Hash
import Encoding.hashReducer as hr
import LabelGen.v2.bindLogo as Labelgen
import LabelGen.v2.plotter as plt
import os
import argparse
import sys

if __name__ == "__main__":
    
    SubSigns = ImageRecognizer.imageToSubSignature('Decoding/446300322707631427235.jpg')
    
    
    print(SubSigns)
    #Testing modules
    parser=argparse.ArgumentParser(description='Calculate AudioID of the file')
    parser.add_argument('-f','--file', metavar='', help='Enter the source of the Audio-file')
    parser.add_argument('-id', metavar='', help='AudioId generation-->Enter source file') 
    parser.add_argument('-sign_v1', metavar='', help='Version_1 Signature-->Enter AudioId') 
    parser.add_argument('-sign_v2', metavar='', help='Version_2 Signature-->Enter Signature')
    parser.add_argument('-logo_bind', metavar='', help='Logo Binder generation-->Enter v2_Signature') 
    parser.add_argument('-plotter', metavar='', help='Audio Plotter generation-->Enter v2_Signature')
    args=parser.parse_args()                              
    if args.id:
        print("AudioID genearated: "+AudioID.generateAudioID(str(args.id)))
    if args.sign_v1:
        print("Audio Signature v1 generated: "+Hash.generateHash(str(args.sign_v1)))
    if args.sign_v2:
        print("Audio Signature v2 generated: "+hr.hashReducer(args.sign_v2, 21))
    if args.logo_bind:
        Labelgen.bindCompanyLogo("Misc/assets/multimediaQR.png", 120, f"LabelGen/v2/output/{args.logo_bind}.png")
    if args.plotter:
        plt.plotDatapoints(f"LabelGen/v2/output/{args.plotter}.png", f"LabelGen/v2/output/{args.plotter}.png", args.plotter)
    # ../Misc/TestData/Taki Taki Ft Selena Gomez - DJ Snake (DJJOhAL (mp3cut.net).wav
    if args.file:                                              
        aid =  AudioID.generateAudioID(str(args.file))
        print("AudioID : " + str(aid))
        sign = Hash.generateHash(aid)
        print("Audio Signatrue : " + str(sign))
        v2Sign = hr.hashReducer(sign, 21)
        print("v2 AudioLabel Signature : " + v2Sign)

        Labelgen.bindCompanyLogo("Misc/assets/multimediaQR.png", 120, f"LabelGen/v2/output/{v2Sign}.png")

        plt.plotDatapoints(f"LabelGen/v2/output/{v2Sign}.png", f"LabelGen/v2/output/{v2Sign}.png", v2Sign)
    pass


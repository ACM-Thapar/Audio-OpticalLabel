## Audio Optical Label
QRCodes made more meaningful

## Current Project Structure
Directories
- Design : Contains designs and data storing area.
- LabelGen : Contains modules that will convert binary files into desired Optical Label
- AudioHandling : Conatins modules to compress binary audio files and support for multiple extensions
- Decoding : Conatins decoding versions of Optical Label
- Encoding : Conatins encoding versions of Optical Label
- ClientApp : Conatins a mini-project on App development which would scan Optical Label and use our encoding/decoding techniques to output audio/
- Misc : Contains modules for pattern recognition, and other necessary tools and features.

## Brief about Working
The 'Design' Project will be updated and finalized.

'AudioHandling' will accept any audio format of some limited duration (10-15seconds) and convert it into compressed binary.

'LabelGen' will accept compressed binaries and with the help of 'Encoding' generate an Image (Optical Label).

'ClientApp' will be the platform to deploy our work, it will utilize 'Decoding' and 'Misc' in order to perform well.

'ClientApp', in near future, maybe able to generate Labels as well with help of 'LabelGen', 'AudioHandling', 'Encoding' and 'Misc'

### We follow a systematic Git Workflow -

- Create a fork of this repo.
- Clone your fork of your repo on your pc.
- [Add Upstream to your clone](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/configuring-a-remote-for-a-fork)
- **Every change** that you do, it has to be on a branch. Commits on master would directly be closed.
- Make sure that before you create a new branch for new changes,[syncing with upstream](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork) is neccesary.


## Audio Optical Label
QRCodes made more meaningful

## Current Project Structure
Directories
- Design : Contains designs and data storing area.
- LabelGen : Contains modules that will convert binary files into desired Optical Label
- AudioHandling : Contains modules to compress binary audio files and support for multiple extensions
- Decoding : Contains decoding versions of Optical Label
- Encoding : Contains encoding versions of Optical Label
- ClientApp : Contains a mini-project on App development which would scan Optical Label and use our encoding/decoding techniques to output audio/
- Misc : Contains modules for pattern recognition, and other necessary tools and features.

## Brief about Working
The 'Design' will be updated and finalized.

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

### Good Coding practices to make project easier to grasp

- whenever defining a function add multiline comment specifying params, input and ouput with short working.
- whenever defining a class/enum/structure specify using multiline comment member data and inheritance (if any) with short description.
- specify any 3rd Party Modules being used at the starting of file.
- Don't comment out unused code and commit. Test and decide the best.
- Fully test your methods and Algorithms before commiting. (easier for reviewer)

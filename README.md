# multiple-gcp-text-to-speech
Allow users to convert expressions into sound file through GCP
CC0 - No Rights Reserved (Public Domain)

1. Put your expressions in the input.txt file, line by line

2. In gcpkey.py :
import secret # Remove this line
gcpkey = secret.gcpkey # Put your GCP api key here

3. Configure the config.json file
- voice_name : Voice name of TTS
- inputFilePath : Expressions file
- outputFolderFormat : Output folder | {folderIndex} increase each time
- outputFileFormat : Output file | {fileIndex} : index of the expression in the input file | {expression} : the expression
- startingOutputFileIndex : Starting index of the fileIndex
- startingOutputFolderIndex : Starting index of the folderIndex

import json
import os
import google.cloud.texttospeech as tts

# Load api key
try:
    from gcpkey import gcpkey
except Exception as e:
    raise Exception("You need to put your GCP Key")

# Read the content of the JSON file
print("Loading config file")
with open("config.json", 'r') as json_file:
    configs = json.load(json_file)

# Load input file
inputs = []
inputFile = configs.get("inputFilePath", "")
print(f"Loading '{inputFile}' input file")

try:
    with open(inputFile, 'r') as file:
        inputs = [line.strip() for line in file]
except FileNotFoundError:
    raise FileNotFoundError("File not found!")
except Exception as e:
    raise Exception("An error occurred:", str(e))

# Create folder
startingOutputFolderIndex = configs.get("startingOutputFolderIndex", 0)
outputFolder = configs.get("outputFolderFormat", "").format(folderIndex=startingOutputFolderIndex)
print(f"Creating folder '{outputFolder}'...")

try:
    os.mkdir(outputFolder)
except FileExistsError:
    print("Folder already exists, files could be erased.")
except Exception as e:
    raise Exception("An error occurred:", str(e))

# Increase folder number
configs["startingOutputFolderIndex"] += 1
with open("config.json", 'w') as json_file:
    json.dump(configs, json_file, indent=4)

# Model definition
print("TTS model definition...")
voice_name = configs.get("voice_name", "")
class GCPtts:
    language_code = None
    voice_params = None
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    def __init__(self, voice_name):
        self.language_code = "-".join(voice_name.split("-")[:2])
        self.voice_params = tts.VoiceSelectionParams(language_code=self.language_code, name=voice_name)

    def text_to_bytes(self, text):
        text_input = tts.SynthesisInput(text=text)

        client = tts.TextToSpeechClient(client_options={"api_key": gcpkey})
        response = client.synthesize_speech(
            input=text_input,
            voice=self.voice_params,
            audio_config=self.audio_config,
        )

        return response.audio_content
model = GCPtts(voice_name)

# Each expression
outputFileFormat = configs.get("outputFileFormat", "")
startingOutputFileIndex = configs.get("startingOutputFileIndex", 0)

for fileIndex in range(len(inputs)):
    print("TTS of " + inputs[fileIndex] + "...")
    outputFile = outputFolder + "/" + outputFileFormat.format(fileIndex = fileIndex+startingOutputFileIndex, expression = inputs[fileIndex]) + ".wav"
    with open(outputFile, "wb") as out:
        out.write(model.text_to_bytes(inputs[fileIndex]))

print("Done.")

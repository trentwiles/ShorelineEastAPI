from pydub import AudioSegment

AUDIO_FOLDER = "audio/"
OUTPUT_FOLDER = "audio/"

def combineAudios(audios, output):
    # audios should look like ["1.mp3", "2.mp3"]
    audioHolder = AudioSegment.from_file(f"{AUDIO_FOLDER}bingbong.mp3")
    for audioFile in audios:
        audioHolder += AudioSegment.from_file(f"{AUDIO_FOLDER}{audioFile}")

    savePoint = OUTPUT_FOLDER + "/" + output
    audioHolder.export(savePoint, format="mp3")

    return f"Saved to {savePoint}" 

combineAudios(["welcome_to_this_service.mp3", "Calling at.mp3", "Madison.mp3", "Branford.mp3"], "yeah.mp3")
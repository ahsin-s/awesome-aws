import whisper

model = whisper.load_model('whisper-small.pt')
# Run transcription
result = model.transcribe("extractedaudio.mp3")

# Print the transcription
print(result["text"])

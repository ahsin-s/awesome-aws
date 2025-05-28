import whisper

def download_from_s3(bucket: str, key: str):
    raise NotImplementedError

def save_transcription_result(transcription_result: str):
    raise NotImplementedError


def main():
    model = whisper.load_model('whisper-small.pt')
    # Run transcription
    result = model.transcribe("TestRecording.m4a")

    return result


if __name__ == "__main__":
    main()

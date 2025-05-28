import sys

import ffmpeg


def extract_audio(video_path, audio_path):
    try:
        ffmpeg.input(video_path).output(audio_path, acodec='mp3').run()
        print(f"Audio extracted and saved to {audio_path}")
    except ffmpeg.Error as e:
        print(f"An error occurred: {e.stderr.decode()}")


def main():
    print("SYS ARGS: ")
    print(sys.argv)

    extract_audio('samplevideo.mp4', 'extractedaudio.mp3')


if __name__ == "__main__":
    main()
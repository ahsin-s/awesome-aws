# Notes 

1. the whisper model must be downloaded ahead of time and placed in the run-inference directory. I used whisper-small and it is 500Mb. It would be a total waste of bandwidth to constantly download it for the docker build. Additionally downloading from s3 is NOT cheap.
2. alpine based docker image _can_ work in theory but it would be an absolute pain to set it up and not worth the complexity. Instead, a debian base image is used.
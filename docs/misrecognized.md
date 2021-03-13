# Misrecognized

The idea behind this endpoint is that you have used the transcriber endpoint, and got a result back, but that the result was not satisfactory.
You should call this endpoint with the misrecognized audio segment.
A record for the audio segment will be created in the database and the audio will be saved to disk.
You can then visit the misrecognized/corrections page using a web-browser, play each audio segment and type in the correct text.
Once a pairing exists between an audio segment and a string of text, it can then be part of the next deepspeech training run.




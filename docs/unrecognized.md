# Unrecognized

The idea behind this endpoint is that you have used the 
[transcribe](/docs/transcribe) endpoint, and got a result back, but that 
the result was not satisfactory.
You should call this endpoint with the unrecognized audio segment. When 
you have time, you can visit the unrecognized page using a web-browser, 
play each audio segment and type in the correct text. Once a pairing 
exists between an audio segment and a string of text, it will then be 
part of the next training iteration run. Hence as you reject 
transcriptions and mark them as unrecognized, once you type in the 
correct transcription, you would have made the set of 'gold training 
data' larger.

## Post an unrecognized audio snippet:

    url=http://localhost:8000/Bob/api/v1/En-Gb/unrecognized
    curl -H "content-type: audio/wav" --data-binary @audio.wav "$url"

You should get something like:

    {
      "filePrefix": "UnrecognizedLungReclaimRelievingSegmentLandscapeKudosScarilyContortProvidingDisliking"
    }

## Get an unrecognized audio snippet:

    url=http://localhost:8000/Bob/api/v1/En-Gb/unrecognized
    curl "$url"

You should get something like:

    {
      "audioSrc": "http://localhost:8000/Bob/api/v1/En-Gb/resources/UnrecognizedUrbanEnsureTrinityRunnerEnclosureIllusionShortcutPersevereObsessiveArmband",
      "id": "UnrecognizedUrbanEnsureTrinityRunnerEnclosureIllusionShortcutPersevereObsessiveArmband"
    }

You can then listen to the audio, and submit the id and the correct text to the [/correct/(/docs/correct) endpoint.

[back to index](/docs)

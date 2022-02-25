# Resources:

You call this endpoint to obtain the audio for a particular clip (so 
that you can hear it and vote on it), or to get an unrecognized audio 
snippet, so that you can manually transcribe it.


    url=http://localhost:8000/Bob/api/v1/En-Gb/resources
    id="UnrecognizedLungReclaimRelievingSegmentLandscapeKudosScarilyContortProvidingDisliking"
    # The id of the clip that we posted on the unrecognized endpoint
    curl "${url}/${id}" > audio.ogg

[back to index](/docs)

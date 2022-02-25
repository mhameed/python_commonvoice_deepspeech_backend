# Transcribe

The transcribe endpoint processes the given audio using the selected 
model and sends back a transcription.

if the transcription is incorrect it is expected that the audio will be reposted to either the [/unrecognized](/docs/unrecognized) or [/correct](/docs/correct) endpoints for further processing.

Examples of calling the transcribe endpoint:

## Single transcription:

    url=http://localhost:8000/Bob/api/v1/En-Gb/transcribe
    curl -H "Content-type: audio/wav" --data-binary @audio.wav "$url"
    
You should get something like:

    {
      "transcripts": [
	{
	  "confidence": -16.220125198364258,
	  "utterance": "forgive and forget"
	}
      ]
    }

## Multiple transcription candidates:

    url=http://localhost:8000/Bob/api/v1/En-Gb/transcribe
    curl -H "candidates: 3" -H "Content-type: audio/wav" --data-binary @audio.wav "$url"

should produce something like:

    {
      "transcripts": [
	{
	  "confidence": -16.220125198364258,
	  "utterance": "forgive and forget"
	},
	{
	  "confidence": -22.195079803466797,
	  "utterance": "forgive and forget"
	},
	{
	  "confidence": -26.339231491088867,
	  "utterance": "forgive an forget"
	}
      ]
    }

# Transcription with details:

Time segmentation information is returned when requesting additional details.

    url=http://localhost:8000/Bob/api/v1/En-Gb/transcribe
    curl -H "details: true" -H "Content-type: audio/wav" --data-binary @audio.wav "$url"


should produce something like:

    {
      "transcripts": [
	{
	  "confidence": -16.220125198364258,
	  "words": [
	    {
	      "duration": 0.44,
	      "start_time": 0.54,
	      "word": "forgive"
	    },
	    {
	      "duration": 0.12,
	      "start_time": 1.08,
	      "word": "and"
	    },
	    {
	      "duration": 0.24,
	      "start_time": 1.24,
	      "word": "forget"
	    }
	  ]
	}
      ]
    }

[back to index](/docs/)

# Transcriber

The transcriber uses the current model to process the given audio and sends back a transcription.
A brand new setup would use the downloaded/pre-trained deep speech model from mozilla.
Any new personalized snippets/misrecognized segments that are added will trigger a nightly training round, from a previous checkpoint.
More documentation to follow.



Examples of calling the transcriber:

## Single transcription:

    audio=$(base64 -w 0 proverbs-100.mp4)
    url=https://api.hameed.info/mesar/speech/transcriber/
    . resty
    POST $url -H "Content-Type: Application/json" <<EOF
    {"audio":"$audio"}
    EOF

You should get something like:

    {
      "transcripts": [
	{
	  "confidence": -16.220125198364258,
	  "utterance": "forgive and forget"
	}
      ]
    }

## multiple transcription candidates:

    audio=$(base64 -w 0 proverbs-100.mp4)
    url=https://api.hameed.info/mesar/speech/transcriber/
    . resty
    POST $url -H "Content-Type: Application/json" <<EOF
    {"audio":"$audio", "candidates":3}
    EOF

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

# transcription with details:
Time segmentation information is returned when requesting additional details.

    audio=$(base64 -w 0 proverbs-100.mp4)
    url=https://api.hameed.info/mesar/speech/transcriber/
    . resty
    POST $url -H "Content-Type: Application/json" <<EOF
    {"audio":"$audio", "details":true}
    EOF

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

[back to index][back]

[back]: index

# Sentences:

This endpoint is used for submitting short sentences so that they can be 
used with something like the [donate your voice app](https://github.com/Sav22999/common-voice-android/).

This endpoint is quite useful if there is no model for your language or 
if you want to extend your model and you have a document which you wish 
to include in the processing. The sentence should not be too long, so 
that when it is read back, there is less likelyhood of making mistakes.

## Posting a new sentence:

    url=http://localhost:8000/Bob/api/v1/En-Gb/sentences
    curl -H "Content-Type: Application/json" --data '{"text":"hello world"}' "$url"
    
You should receive something like:

    {
      "id": "SentenceSmolderTheftThursdayShowdownSkilletSappyAshesStableSportyMagnetism",
      "source": "",
      "text": "hello world"
    }

If you wish to include metainformation such as the source of the 
sentence, such as the filename/linenumber you can do so in the source 
field.

    url=http://localhost:8000/Bob/api/v1/En-Gb/sentences
    curl -H "Content-Type: Application/json" --data '{"text":"hello world", "source":"my_book.txt:54"}' "$url"

# Obtaining a sentence to be spoken:

If you are implementing something like the [donate your voice 
app](https://github.com/Sav22999/common-voice-android/), you might need to obtain sentences to be 
spoken.

    url=http://localhost:8000/Bob/api/v1/En-Gb/sentences
    curl "$url"

You should get something like:

    [
      {
        "id": "SentencePlodFootprintFreenessContortCulpritBuckwheatShallowBobtailGeckoSwell",
        "language": "En-Gb",
        "source": "simple_phrases.txt",
        "text": "good evening",
        "user": "Bob"
      }
    ]

If you wish to obtain more than one sentence at a time, then yu can give a count:

    url=http://localhost:8000/Bob/api/v1/En-Gb/sentences
    curl "${url}?count=3"

Once you have recorded the audio for the given sentence, 
you are expected to post to the [/clips](/docs/clips) endpoint.

[back to index](/docs)

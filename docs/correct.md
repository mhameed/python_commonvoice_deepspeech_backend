# Correct:

This endpoint is used for associating an audio snippet, with its correct 
transcription.

## Given an audio file:

    url=http://localhost:8000/Bob/api/v1/En-Gb/correct
    curl -H "sentence: hello%20world" -H "content-type: audio/ogg" --data-binary @audio.ogg

### Note:

To ensure the sentence header is correctly transmitted, it needs to be URI encoded.
You can do this in python with:

    import urllib.parse
    a = "بسم الله"
    urllib.parse.quote(a)


and in java:


    import java.net.URI;
    import java.net.URISyntaxException;
    ...
    String s = "بسم الله";
    try {
        String header = new URI(null,null, s, null).toASCIIString();
    } catch (URISyntaxException e) {
        ...
    }
    ...


## Given an unrecognized id:

If you previously did not have time to process the audio snippet, and 
submitted it to the unrecognized endpoint, and now you have had time to 
process it:

    url=http://localhost:8000/Bob/api/v1/En-Gb/correct
    curl -H "content-type: application/json" --data \ 
    '{"text":"hello world", "id":"unrecognizedGreenFishEarchSwims"}'

[back to index](/docs)

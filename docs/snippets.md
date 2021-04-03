# Snippets

Initial set of textual strings that should be recorded using the Trainer application to improve personal accuracy.

To view current snippets and their status visit [Monitor][monitor].

## example request:

    $ resty https://api.hameed.info/mesar/speech/snippets
        https://api.hameed.info/mesar/speech/snippets*
    $ GET /
    {
      "id": 108,
      "snippet": "charity covers a multitude of sins",
      "status": "p",
      "token": "24bacf03949146d4804198f270713242"
    }
    $

"snippet", is the string of text that you should record and post back.

    $ audio=$(base64 -w 0 /tmp/recording.mp4)
    $ PATCH /patch -H "Content-Type: Application/json" <<EOF
    {
      "id": 108,
      "token": "24bacf03949146d4804198f270713242",
      "status: "y",
      "audio":"$audio"
    }
    EOF
    $

## Error codes:

[back to index][back]

[back]: index
[monitor]: ../snippets/monitor/


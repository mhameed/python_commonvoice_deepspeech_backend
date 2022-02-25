# Clips:

## POST:

This endpoint is used for uploading matching audio snippets for sentences that you obtain from the 
[/sentences](/docs/sentences) endpoint.

This is used with something like the [donate your voice 
app](https://github.com/Sav22999/common-voice-android/) (speak screen).

    id="SentenceSmolderTheftThursdayShowdownSkilletSappyAshesStableSportyMagnetism"
    url=http://localhost:8000/Bob/api/v1/En-Gb/clips
    curl -H "sentence-id: ${id}" -H "content-type: audio/ogg" --data-binary @audio.ogg

# GET:

This is used to obtain audio snippets and their matching sentences, so that they can be voted on for 
their correctness.
This is used with something like the [donate your voice app](https://github.com/Sav22999/common-voice-android/) (listen screen).

    url=http://localhost:8000/Bob/api/v1/En-Gb/clips
    curl "$url"

You should get something like:

    [
      {
        "audioSrc": "http://localhost:8000/Bob/api/v1/En-Gb/resources/ClipMochaGiddinessCatchingEspionageFrightfulEconomyHurlingHabitableCreatableUndying",
        "glob": "ClipMochaGiddinessCatchingEspionageFrightfulEconomyHurlingHabitableCreatableUndying/SentenceGutterShoptalkScienceBuntHankyUnnoticedPalaceUnrivaledRejoiceShout",
        "id": "ClipMochaGiddinessCatchingEspionageFrightfulEconomyHurlingHabitableCreatableUndying",
        "sentence": {
          "id": "SentenceGutterShoptalkScienceBuntHankyUnnoticedPalaceUnrivaledRejoiceShout",
          "text": "a thing of beauty is a joy for ever"
        }
      }
    ]

## Voting for a clip:

    id="ClipMochaGiddinessCatchingEspionageFrightfulEconomyHurlingHabitableCreatableUndying"
    url=http://localhost:8000/Bob/api/v1/En-Gb/clips/${id}/votes
    # possative vote:
    curl --data '{"challenge":null, "isValid": True} "$url"
    # negative vote:
    curl --data '{"challenge":null, "isValid": False} "$url"

[back to index](/docs)

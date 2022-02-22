# Private Mozilla deepspeech recognition and training backend

The goal of this project is to provide a private API for recognition, and a way of collecting training materials for improving your deepspeech model.
Over time you will have built up both a private dataset which you can use at any point to rebase your training on a different starting model, or iteratively improved your existing model.

there are two ways of building up your training dataset.

- Use a pre-existing deepspeech model to perform recognition, and when the recognition is incorrect, submit the corrected sentence.
- Collect sentences that you wish to read, and then use the [donate your voice app](https://github.com/Sav22999/common-voice-android/) on your phone to provide matching audio recordings.

You may ask why is this an API -
because you should be able to interact with your private recognition engine from multiple frontends, such as your phone, desktop, or home assistant.

See [here](https://github.com/mhameed/python_deepspeech_driver) For a simple/functional Linux desktop frontend,


## Prerequisites

The following is a list of debian packages, if you are using a different 
distribution and you find the corresponding list for your distribution 
please consider making a pull request with the information.


- build-essential
- ffmpeg
- libmariadb-dev
- mariadb-server
- python3.7 or newer
- python3-dev
- python3-virtualenv 
- sox

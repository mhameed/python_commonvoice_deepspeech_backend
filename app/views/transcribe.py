import os
from app import db, metrics
from flask import Blueprint, jsonify, request, make_response, Response
from plumbum.cmd import ffmpeg
import numpy as np

from deepspeech import Model, version

ds = Model(os.path.join(os.getcwd(), 'deepspeech_model', 'ds.pbmm'))
ds.enableExternalScorer(os.path.join(os.getcwd(), 'deepspeech_model', 'ds.scorer'))

ffmpeg_cmd = ffmpeg['-i', '-', '-ac', '1', '-b:a', '16', '-ar', '16000', '-f', 'wav', '-']

def words_from_candidate_transcript(metadata):
    word = ""
    word_list = []
    word_start_time = 0
    # Loop through each character
    for i, token in enumerate(metadata.tokens):
        # Append character to word if it's not a space
        if token.text != " ":
            if len(word) == 0:
                # Log the start time of the new word
                word_start_time = token.start_time

            word = word + token.text
        # Word boundary is either a space or the last character in the array
        if token.text == " " or i == len(metadata.tokens) - 1:
            word_duration = token.start_time - word_start_time

            if word_duration < 0:
                word_duration = 0

            each_word = dict()
            each_word["word"] = word
            each_word["start_time"] = round(word_start_time, 4)
            each_word["duration"] = round(word_duration, 4)

            word_list.append(each_word)
            # Reset
            word = ""
            word_start_time = 0

    return word_list


def metadata_json_output(metadata):
    json_result = dict()
    json_result["transcripts"] = [{
        "confidence": transcript.confidence,
        "words": words_from_candidate_transcript(transcript),
    } for transcript in metadata.transcripts]
    return json_result

bp = Blueprint('transcribe', __name__, url_prefix='/transcribe')

metrics['cv_requests'].labels(method='post', endpoint='/', view='transcribe')
@bp.route('', methods=['POST'])
def post():
    metrics['cv_requests'].labels(method='post', endpoint='/', view='transcribe').inc()
    if not request.content_type.lower().startswith('audio/'):
        return make_response(jsonify(status='Expected "content-type: audio/*" header'), 400)
    candidates = int(request.headers.get('candidates',1))
    details = request.headers.get('details','False').lower() == 'true'
    # read the mono 16khz wav file into a numpy array suitable for deepspeech:
    audio=np.frombuffer((ffmpeg_cmd << request.get_data() ).popen().stdout.read(), np.int16)
    if details:
        return make_response(jsonify(metadata_json_output(ds.sttWithMetadata(audio, candidates))), 200)
    data = metadata_json_output(ds.sttWithMetadata(audio, candidates))
    transcripts={'transcripts':[]}
    results=[]
    for transcript in data['transcripts']:
        confidence = transcript['confidence']
        utterance = " ".join([word['word'] for word in transcript['words']])
        transcripts['transcripts'].append({'confidence':confidence, 'utterance':utterance})
    return make_response(jsonify(transcripts), 200)

# vim: sw=4 ts=4 sts=4 expandtab

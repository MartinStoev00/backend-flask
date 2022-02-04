from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path
import numpy as np



# conda install ffmpeg if nobackend error starts
def are_same(user_id):
    # files for user in "users" and a temporary one for "login"
    fpath = Path(f"users/{user_id}.wav")
    fpath2 = Path(f"login/{user_id}.wav")
    # processing on  audio before comparing
    wav = preprocess_wav(fpath)
    wav2 = preprocess_wav(fpath2)

    encoder = VoiceEncoder()
    # turns sound into utterances which allow for voices to be compared
    embed = encoder.embed_utterance(wav)
    embed2 = encoder.embed_utterance(wav2)
    # printing matrix for utterances of the two variables above
    # np.set_printoptions(precision=3, suppress=True)

    # matrix multiplication to get precise number of how close are the two voices
    # @ is short for np.matmul
    return embed @ embed2

from espnet2.bin.tts_inference import Text2Speech
from scipy.io.wavfile import write
import numpy as np

# TERMINAL
# import nltk
# nltk.download('averaged_perceptron_tagger_eng')
# nltk.download('punkt_tab')

from nltk.tokenize import sent_tokenize

class TTS:

    def __init__(self):
        self.model = Text2Speech.from_pretrained("kan-bayashi/ljspeech_fastspeech2")
        # print(self.model.__dict__)          ==> a lot
        # print(self.model.vocoder.__dict__)  ==> a lot
        self.frame_ms = int(self.model.vocoder.params["n_shift"]) / self.model.fs * 1000 * 0.9 # without 0.9 lagged behind visuals
        self.token_list = self.model.train_args.token_list
    

    def run(self, text, out_name="response"):
        """
        Return path to audio file and list of phoneme--delay pairs.
        Delay is measured in discrete (int) milliseconds.
        Text is automatically broken up into sentences to conform to 500token model limit.
        """
        out_path = f"tmp/{out_name}.wav"
        silence_frames = 4
        silence = np.zeros(silence_frames*int(self.model.fs * self.frame_ms / 900), dtype=np.float32)

        out_wav = np.empty((0,), dtype=np.float32)
        phonemes: str = []
        frame_duration = []

        for sentence in sent_tokenize(text):
            # print(sentence)
            espnet_sentence = self.model(sentence)
            out_sentence_wav = np.concatenate((silence, espnet_sentence["wav"].view(-1).cpu().numpy())) 
            out_wav = np.concatenate((out_wav, out_sentence_wav))

            processed = self.model.preprocess_fn("test", {"text": text, "lang": None})  # magic call to preprocess_fn
            tokens = processed["text"]
            sentence_phonemes: list[str] = [".."] + [self.token_list[i] for i in tokens.tolist()] 
            sentence_frame_duration = np.concatenate(([silence_frames], espnet_sentence["duration"])) 
            phonemes.extend(sentence_phonemes)
            frame_duration.extend(sentence_frame_duration)

        # inspection from simpler times:
        #   out = self.model(text)
        #   print(out.keys())  ==> dict_keys(['feat_gen', 'duration', 'pitch', 'energy', 'feat_gen_denorm', 'wav'])
        #   print(out["wav"].view(-1).cpu().numpy().dtype)  ==> float32
        write(out_path, self.model.fs, out_wav)

        phoneme_delay = []
        cumulative_int_ms = 0
        cumulative_ms = 0
        for ph, fr in zip(phonemes, frame_duration):
            fr = int(fr)
            # if not ph[0].isalpha():
            #     fr -= 1
            cumulative_ms += fr * self.frame_ms
            delay_int_ms = int(cumulative_ms - cumulative_int_ms)
            cumulative_int_ms += delay_int_ms
            # print(int(fr), cumulative_ms, cumulative_int_ms)
            phoneme_delay.append({"phoneme": ph, "delay": delay_int_ms})

        return out_path, phoneme_delay
    

if __name__=="__main__":
    tts = TTS()
    _, _ = tts.run("test. dr. manhattan loves eggs! hard to believe?")
import soundfile
from espnet2.bin.asr_inference import Speech2Text
# from espnet2.bin.s2t_inference import Speech2Text  # for newer models

# HOWTO
# https://github.com/espnet/espnet_model_zoo

model = Speech2Text.from_pretrained("kamo-naoyuki/wsj")  # it took FOREVER

speech, rate = soundfile.read("tmp/response.wav")
nbests = model(speech)

text, *_ = nbests[0]
print(text)
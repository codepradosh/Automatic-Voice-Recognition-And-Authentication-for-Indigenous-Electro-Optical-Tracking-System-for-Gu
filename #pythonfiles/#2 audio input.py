# Code retested by KhalsaLabs
# You can use your own audio file in code
# Raw or wav files would work perfectly
# For mp3 files, you need to modify code (add codex)

from __future__ import print_function
import os
from pocketsphinx import Pocketsphinx, get_model_path, get_data_path

model_path = get_model_path()
data_path = get_data_path()

config = {
'hmm': os.path.join(model_path, 'en-us'),
'lm': os.path.join(model_path, 'en-us.lm.bin'),
'dict': os.path.join(model_path, 'cmudict-en-us.dict')
}

ps = Pocketsphinx(**config)
ps.decode(
audio_file=os.path.join(data_path, 'test1.wav'), # add your audio file here
buffer_size=2048,
no_search=False,
full_utt=False
)

print(ps.hypothesis())
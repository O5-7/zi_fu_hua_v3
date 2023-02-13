import random

import cv2
import numpy as np
from code_source import code_source
from codes_style import codes_style
from ndarrays_to_str import ndarrays_to_str

code_source = code_source('xin_song_ti_16/code_sources_v3.txt', 'xin_song_ti_16/code_sources_v3_img_xinsongti_16.png', 16)
for x, y in code_source.code_dict.items():
    print(x, y.codes_num, y.codes)
ndarrays_to_str = ndarrays_to_str(np.random.randint(0, 127, (10, 10)), code_source)
print(random.Random().randint(-1,1))

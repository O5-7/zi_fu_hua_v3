import random

import cv2
import numpy as np
from code_source import code_source
from codes_style import codes_style
from ndarrays_to_str import ndarrays_to_str
from media_to_ndarray_iter import media_to_ndarray_iter

code_source = code_source('xin_song_ti_16/code_sources_v3.txt', 'xin_song_ti_16/code_sources_v3_img_xinsongti_16.png', 16)
for x, y in code_source.code_dict.items():
    print(x, y.codes_num, y.codes)

'''单张转换测试'''
np.random.seed(0)
img = np.random.randint(0, 255, (10, 10, 3), dtype=int)

ndarrays_to_str = ndarrays_to_str(code_source)
out = ndarrays_to_str.img_to_str(img, codes_style(reverse=True, color=True, codes=False))
print(out)

import numpy as np
import taichi as ti
import random
from code_source import code_source
from codes_style import codes_style

ti.init(arch=ti.cuda)


class ndarrays_to_str:
    def __init__(self, media_ndarry: np.ndarray, code_source_obj: code_source):
        self.codes_dict: dict = code_source_obj.code_dict
        self.is_colorful = media_ndarry.shape[-1] == 3
        shape_len = len(media_ndarry.shape)
        if self.is_colorful: shape_len -= 1
        self.type = 'image' if shape_len == 2 else 'gif_or_video'

    # @ti.func
    def img_to_str(self, image: np.ndarray, style: codes_style):
        out_str = ''
        for line in image:
            for pix in line:
                pass

    # @ti.func
    def gray_codes_reverse(self, pix: np.ndarray) -> str:
        out_str = ''
        if self.is_colorful:
            pix = int(np.average(pix))
        is_reverse = pix > 127
        if is_reverse: pix -= 127
        while pix not in self.codes_dict.keys():
            pix += random.Random().randint(-1, 1)
            if pix < 0: pix = 0
            if pix > 127: pix = 127

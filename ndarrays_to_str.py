import numpy as np
import taichi as ti
import random
from code_source import code_source
from codes_style import codes_style
from code_source import one_color_codes

ti.init(arch=ti.cuda)


class ndarrays_to_str:
    def __init__(self, media_ndarray: np.ndarray, code_source_obj: code_source):
        self.codes_dict: dict = code_source_obj.code_dict
        self.is_colorful = media_ndarray.shape[-1] == 3
        shape_len = len(media_ndarray.shape)
        if self.is_colorful:
            shape_len -= 1
        self.type = 'image' if shape_len == 2 else 'gif_or_video'

    # @ti.func
    def img_to_str(self, image: np.ndarray, style: codes_style):
        out_str = ''
        for line in image:
            for pix in line:
                out_str += self.gray_block(pix)  # 替换转换方法
            out_str += '[0m\n'
        return out_str

    # @ti.func
    def gray_codes_reverse(self, pix: np.ndarray) -> str:
        out_str = ''
        if self.is_colorful:
            pix = int(np.average(pix))
        is_reverse = pix > 127
        if is_reverse:
            pix -= 127
            out_str = '[38;2;0;0;0;48;2;255;255;255m'
        else:
            out_str = '[38;2;255;255;255;48;2;0;0;0m'
        while pix not in self.codes_dict.keys():
            pix += random.Random().randint(-1, 1)
            if pix < 0:
                pix = 0
            if pix > 127:
                pix = 127
        find_strs: one_color_codes = self.codes_dict[pix]
        out_str += find_strs.codes[random.Random().randint(0, find_strs.codes_num - 1)]
        return out_str

    def gray_block(self, pix: np.ndarray) -> str:
        out_str = '　'
        if self.is_colorful:
            pix = int(np.average(pix))
        pix = int(pix)
        out_str = '[48;2;{0};{0};{0}m　'.format(pix)
        return out_str

    def gray_codes_no_reverse(self, pix: np.ndarray) -> str:
        out_str = '[38;2;255;255;255;48;2;0;0;0m'
        if self.is_colorful:
            pix = int(np.average(pix))
        pix = int(pix / 2)
        while pix not in self.codes_dict.keys():
            pix += random.Random().randint(-1, 1)
            if pix < 0:
                pix = 0
            if pix > 127:
                pix = 127
        find_strs: one_color_codes = self.codes_dict[pix]
        out_str += find_strs.codes[random.Random().randint(0, find_strs.codes_num - 1)]
        return out_str

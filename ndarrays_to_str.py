import numpy as np
import taichi as ti
import random
from code_source import code_source
from codes_style import codes_style
from code_source import one_color_codes

ti.init()


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
        """
        将单帧图像按设定风格转换为字符串

        :param image: 单帧图像
        :param style: 字符风格
        :return: 单帧字符串
        """
        out_str = ''
        trans_func = self.gray_codes_no_reverse
        if style.color:
            if style.codes:
                trans_func = self.color_codes
            else:
                trans_func = self.color_block
        else:
            if style.codes:
                if style.reverse:
                    trans_func = self.gray_codes_reverse
                else:
                    trans_func = self.gray_codes_no_reverse
            else:
                trans_func = self.gray_block()
        for line in image:
            for pix in line:
                '''替换转换方法'''
                out_str += self.color_block(pix)

            out_str += '[0m\n'
        return out_str

    # @ti.func
    def gray_codes_reverse(self, pix: np.ndarray) -> str:
        out_str = ''
        if self.is_colorful:
            pix = int(np.average(pix))
        is_reverse = pix > 127
        if is_reverse:
            pix = 255 - pix
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
        out_str = ''
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

    def color_block(self, pix: np.ndarray) -> str:
        out_str = ''
        if self.is_colorful:
            out_str = '[48;2;{0};{1};{2}m　'.format(pix[0], pix[1], pix[2])
        else:
            out_str = '[48;2;{0};{0};{0}m　'.format(pix[0])
        return out_str

    def color_codes(self, pix: np.ndarray) -> str:
        out_str = ''
        r = g = b = 0
        r_code = g_code = b_code = 0
        r_bg = g_bg = b_bg = 0
        if self.is_colorful:
            r = pix[0]
            g = pix[1]
            b = pix[2]
            # print(r,g,b)
        else:
            r = g = b = pix[0]
        max_dif = max([abs(127 - r), abs(127 - g), abs(127 - b)])
        # print('max_dif  ', max_dif)
        while max_dif not in self.codes_dict.keys():
            max_dif += random.Random().randint(-1, 1)
            if max_dif < 0:
                max_dif = 0
            if max_dif > 127:
                max_dif = 127
        if r > max_dif:
            r_code = 255
            r_bg = round((r - max_dif) * (255.0 / (255.0 - float(max_dif))))
        else:
            r_code = round(r * (255.0 / max_dif))
            r_bg = 0

        if g > max_dif:
            g_code = 255
            g_bg = round((g - max_dif) * (255.0 / (255.0 - float(max_dif))))
        else:
            g_code = round(g * (255.0 / max_dif))
            g_bg = 0

        if b > max_dif:
            b_code = 255
            b_bg = round((b - max_dif) * (255.0 / (255.0 - float(max_dif))))
        else:
            b_code = round(b * (255.0 / max_dif))
            b_bg = 0

        out_str = '[38;2;{0};{1};{2};48;2;{3};{4};{5}m'.format(r_code, g_code, b_code, r_bg, g_bg, b_bg)
        find_strs: one_color_codes = self.codes_dict[max_dif]
        out_str += find_strs.codes[random.Random().randint(0, find_strs.codes_num - 1)]
        return out_str

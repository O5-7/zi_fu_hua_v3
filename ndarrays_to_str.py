import time
import numpy as np
import random
from code_source import code_source
from codes_style import codes_style
from code_source import one_color_codes


class ndarrays_to_str:
    """
    将单张图像转换为str
    """

    def __init__(self, code_source_obj: code_source):
        """
        指定字符集生成转换器

        :param code_source_obj: 字符集对象
        """
        self.codes_dict: dict = code_source_obj.code_dict
        self.color_dict: dict = code_source_obj.color_dict
        self.is_colorful = True
        self.trans_func = self._gray_codes_no_reverse
        self.img = None
        self.img_shape = None
        self.out_str = ''

    def img_to_str(self, image: np.ndarray, img_shape: tuple, style: codes_style):
        self.img = image
        self.img_shape = img_shape
        self.is_colorful = len(image.shape) == 3
        if style.color:
            if style.codes:
                self.trans_func = self._color_codes
            else:
                self.trans_func = self._color_block
        else:
            if style.codes:
                if style.reverse:
                    self.trans_func = self._gray_codes_reverse
                else:
                    self.trans_func = self._gray_codes_no_reverse
            else:
                self.trans_func = self._gray_block
        self.out_str = ''
        self._img_to_str_()
        return self.out_str

    def _img_to_str_(self):
        """
        将单帧图像按设定风格转换为字符串

        风格默认为灰色无反转字符

        :return: 单帧字符串
        """
        "tichi kernel"

        pix_str_ndarray = a = [['' for _ in range(self.img_shape[1])] for _ in range(self.img_shape[0])]
        for x in range(self.img_shape[0]):
            for y in range(self.img_shape[1]):
                pix_str_ndarray[x][y] = self.trans_func(self.img[x, y])

        for x in range(self.img_shape[0]):
            for y in range(self.img_shape[1]):
                self.out_str += pix_str_ndarray[x][y]
            self.out_str += '[0m\n'


    def _gray_codes_reverse(self, pix: np.ndarray) -> str:
        out_str = ''
        if self.is_colorful:
            pix = int(np.average(pix))
        is_reverse = pix > 127
        if is_reverse:
            pix = 255 - pix
            out_str = '[38;2;0;0;0;48;2;255;255;255m'
        else:
            out_str = '[38;2;255;255;255;48;2;0;0;0m'
        pix = self.color_dict[pix]
        find_strs: one_color_codes = self.codes_dict[pix]
        out_str += find_strs.codes[random.Random().randint(0, find_strs.codes_num - 1)]
        return out_str

    def _gray_block(self, pix: np.ndarray) -> str:
        out_str = ''
        if self.is_colorful:
            pix = int(np.average(pix))
        pix = int(pix)
        out_str = '[48;2;{0};{0};{0}m　'.format(pix)
        return out_str

    def _gray_codes_no_reverse(self, pix: np.ndarray) -> str:
        out_str = '[38;2;255;255;255;48;2;0;0;0m'
        if self.is_colorful:
            pix = int(np.average(pix))
        pix = int(pix / 2)
        pix = self.color_dict[pix]
        find_strs: one_color_codes = self.codes_dict[pix]
        out_str += find_strs.codes[random.Random().randint(0, find_strs.codes_num - 1)]
        return out_str

    def _color_block(self, pix: np.ndarray) -> str:
        out_str = ''
        if self.is_colorful:
            out_str = '[48;2;{0};{1};{2}m　'.format(pix[0], pix[1], pix[2])
        else:
            out_str = '[48;2;{0};{0};{0}m　'.format(pix[0])
        return out_str

    def _color_codes(self, pix: np.ndarray) -> str:
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
        max_dif = self.color_dict[max_dif]
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


if __name__ == '__main__':
    code_source = code_source('./xin_song_ti_16/code_sources_v3.txt',
                              './xin_song_ti_16/code_sources_v3_img_xinsongti_16.png',
                              16,
                              '新宋体'
                              )
    convert = ndarrays_to_str(code_source)
    im_shape = (10, 10, 3)
    img = np.random.randint(0, 255, size=im_shape)
    t_s = time.time()
    a = convert.img_to_str(img, im_shape, codes_style(reverse=True, color=True))
    print(time.time() - t_s)
    t_s = time.time()
    b = convert.img_to_str(img, im_shape, codes_style(codes=False, color=True))
    print(time.time() - t_s)
    print(a)
    print(b)


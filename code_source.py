import struct

import numpy as np
import cv2


class one_color_codes:
    def __init__(self, codes: str, codes_num: int):
        self.codes: str = codes
        self.codes_num: int = codes_num


class code_source:
    def __init__(self, code_source_str: str, code_source_img: str, font_size: int):
        """
        gbk字符集对象,通过原字符文件字符截图字体大小,获取
        :param code_source_str: txt文件地址
        :param code_source_img: img文件地址
        :param font_size: 字体大小
        """
        # 读取 codes文件
        code_source_file = open(code_source_str)
        codes_str_list = list(code_source_file.readline())
        code_source_file.close()
        # 读取 img文件
        source_img: np.ndarray = cv2.imread(code_source_img)[:, :, 0]
        # print('source_img:', source_img.shape)
        code_img_size_y = int(source_img.shape[0] / font_size)
        code_img_size_x = int(source_img.shape[1] / font_size)
        source_img = source_img[:code_img_size_y * font_size, :code_img_size_x * font_size]  # 裁剪
        average_size = (code_img_size_x, code_img_size_y)
        # print(average_size)
        average_color_list: np.ndarray = (cv2.resize(source_img[:], average_size, interpolation=cv2.INTER_AREA)).reshape((-1,))
        # print(average_color_list.shape)
        # 获取字体排序
        average_color_value_arg = average_color_list.argsort()

        code_sorted = [codes_str_list[i] for i in average_color_value_arg]
        color_value_sorted = [average_color_list[i] for i in average_color_value_arg]
        # print(code_sorted, '\n', color_value_sorted, sep='')
        self.code_dict = dict()  # {color:codes_str}字典
        for value in range(255):
            if value in color_value_sorted:
                codes_in_one_color = ''
                for i, code in list(enumerate(code_sorted)):
                    if color_value_sorted[i] == value:
                        codes_in_one_color += code
                self.code_dict[value] = one_color_codes(codes_in_one_color, len(codes_in_one_color))


if __name__ == "__main__":
    code_source('code_sources_v3.txt', 'code_sources_v3_img_xinsongti_16.png', 16)

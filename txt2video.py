import os
import numpy as np
import cv2
from code_source import code_source
from codes_style import codes_style
from media_to_ndarray_iter import media_to_ndarray_iter
from ndarrays_to_str import ndarrays_to_str


class txt_to_video_from_media:
    pass


class txt_to_video_from_zfh:
    def __init__(self, file_path: str, out_path: str, code_source_: code_source, type: str):
        self.file_path = file_path
        self.out_path = out_path
        self.code_source = code_source_
        self.type = type
        self.str_size: np.ndarray = None
        self.image_size: np.ndarray = None

    def gener_img(self):
        if not os.path.isdir(self.out_path) and len(os.listdir(self.out_path)) == 0:
            return 0
        else:
            zfh_file_name = ''
            file_list = os.listdir(self.file_path)
            for file_name in file_list:
                if file_name.endswith('.zfh'):
                    zfh_file_name = file_name
                    break
            if zfh_file_name == '':
                print('no such file')
                return 0
            zfh_file = open(os.path.join(self.file_path, zfh_file_name),
                            mode='r',
                            encoding='gbk')

            # meta date
            while True:
                line = zfh_file.readline()
                if line.startswith('str_size'):
                    self.str_size = np.array(eval('({})'.format(line[9:])))
                    self.image_size = code_source.font_size * self.str_size
                    # print(self.str_size)
                if line == 'END_META_DATA\n':
                    break

            han_array = list()
            line_index = 0
            color_array = np.zeros(shape=(self.str_size[0], self.str_size[1], 6), dtype='uint8')
            while True:
                line = zfh_file.readline()[:-1]
                han_index = 0
                if line == '':
                    # 输出最后一张
                    print(han_array)
                    print(color_array)
                    return
                if line.startswith('//'):
                    # write image
                    print(han_array)
                    print(color_array)

                    # new empty image
                    han_array = list()
                    color_array = np.zeros(shape=(self.str_size[0], self.str_size[1], 6), dtype='uint8')
                    line_index = 0
                    han_index = 0
                    continue
                if line.startswith('duration'):
                    continue
                first_spilt = line.split("""[38;2;""")
                print(first_spilt)
                han_array.append('')
                for color_han in first_spilt:
                    if color_han == '':
                        continue
                    han = color_han[-1]
                    if han == 'm':
                        continue
                    han_array[-1] += han

                    two_color = color_han[:-2].split(';48;2')
                    color = two_color[0] + two_color[1]
                    second_split = color.split(';')
                    color_array[line_index][han_index] = np.array(second_split, dtype='uint8')

                    han_index += 1
                line_index += 1





#

if __name__ == '__main__':
    code_source = code_source('./xin_song_ti_16/code_sources_v3.txt',
                              './xin_song_ti_16/code_sources_v3_img_xinsongti_16.png',
                              16,
                              '新宋体'
                              )
    txt_to_video_from_zfh('./Mitski', './out_text', code_source, 'image').gener_img()

import time

import numpy as np
from tqdm import tqdm
from collections.abc import Iterable
from code_source import code_source
from codes_style import codes_style
from media_to_ndarray_iter import media_to_ndarray_iter
from ndarrays_to_str import ndarrays_to_str
import cv2
import os
import copy
import moviepy.editor
from copy import deepcopy
import multiprocessing as mp


def mp_dict_tqdm(dict_len: int, mp_dict: dict):
    for count in tqdm(range(dict_len), ncols=120):
        while True:
            if mp_dict.__len__() > count:
                break


def convert_process(frame_list: np.ndarray,
                    frame_start: int,
                    s: codes_style,
                    mp_id: int,
                    mp_dict: dict):
    inter_dict = {}
    code_source_ = code_source('./xin_song_ti_16/code_sources_v3.txt',
                               './xin_song_ti_16/code_sources_v3_img_xinsongti_16.png',
                               16,
                               '新宋体'
                               )
    c = ndarrays_to_str(code_source_)

    for index in range(frame_list.__len__()):
        d, f = frame_list[index]
        frame_str = c.img_to_str(f, f.shape[:2], s)
        inter_dict.update({frame_start + index: (d, frame_str)})
        if inter_dict.__len__() == 64:
            mp_dict.update(inter_dict)
            inter_dict = {}
    mp_dict.update(inter_dict)


def convert_frame(n: np.ndarray,
                  sh: tuple,
                  c: ndarrays_to_str,
                  s: codes_style,
                  index_: int, ):
    n = cv2.resize(
        n,
        sh[::-1],
        interpolation=cv2.INTER_AREA
    )
    return index_, c.img_to_str(n, sh, s)


class zi_fu_hua:
    """
    字符画类
    """

    def __init__(self, source_file: str, codes: code_source, style: codes_style, pix_size: float = -1, inter_type=cv2.INTER_AREA):
        """
        字符画对象

        :param source_file: 输入的媒体文件
        :param codes: code_source 对象
        :param style: codes_style 对象
        :param pix_size: pix_size 多少像素宽的像素转换为一个字符, 默认为code_source对象的字符大小
        """
        self.file_path = source_file
        self.file_name = os.path.basename(self.file_path).split('.')[0]
        self.code_source = codes
        self.codes_style = style
        self.pix_size = pix_size
        if self.pix_size == -1:
            self.pix_size = codes.font_size
        self.inter_type = inter_type

    def generate_files(self, path: str = '.', audio_vol: float = 0.3, loop_play: bool = False):
        """
        输出zfh和wav文件(只有视频会输出wav文件)

        输出文件会在指定目录下的以输入媒体文件名为名的文件夹里

        :param multi_process_num: 多线程数量, 仅在视频有效
        :param audio_vol: 音量
        :param path: 输出目录
        :param loop_play: 是否循环播放
        :return:
        """

        media = media_to_ndarray_iter(self.file_path, self.pix_size, self.inter_type)
        shape = media.shape
        convert = ndarrays_to_str(self.code_source)
        if not os.path.exists(os.path.join(path, self.file_name)):
            os.makedirs(os.path.join(path, self.file_name))
        with open(os.path.join(path, '{}\\result.zfh'.format(self.file_name)), mode='w') as out_file:
            '''写入 meta_data'''
            out_file.write('//meta_data\n')
            out_file.write('version=zi_fi_hua_v3\n')
            out_file.write('github=github.com/O5-7/pix_player_v3\n')
            out_file.write('media_name={}\n'.format(self.file_name))
            out_file.write('font_type={}\n'.format(self.code_source.font_type))
            out_file.write('font_size={}\n'.format(self.code_source.font_size))
            out_file.write('str_size={},{}\n'.format(
                int(shape[1] / self.pix_size),
                int(shape[0] / self.pix_size)
            ))
            out_file.write('loop_play={}\n'.format(loop_play))
            if media.file_type == 'video':
                """ 导出音频 """
                video = moviepy.editor.VideoFileClip(self.file_path)
                audio = video.audio
                audio = audio.volumex([audio_vol] * 2)
                audio.write_audiofile(os.path.join(path, '{}\\result.wav'.format(self.file_name)))
                out_file.write('audio={}\n'.format(True))
            else:
                out_file.write('audio={}\n'.format(False))
            out_file.write("END_META_DATA\n")

            '''
            写入 str_data
            '''

            ndarrays_iter = media.get_media_ndarray_iter()
            for d, f in tqdm(ndarrays_iter, ncols=120):
                out_file.write('//new_frame\n')
                out_file.write('duration=' + str(d) + '\n')
                frame_str = convert.img_to_str(f, (int(shape[0] / self.pix_size), int(shape[1] / self.pix_size)), self.codes_style)
                while frame_str.split('\n').__len__() != (1 + int(shape[0] / self.pix_size)):
                    frame_str = convert.img_to_str(f, (int(shape[0] / self.pix_size), int(shape[1] / self.pix_size)), self.codes_style)
                    print('err! worry lines_num!')
                out_file.write(frame_str)
            '''
            行数测试
            '''
            # frame_str_lines = frame_str.split('\n').__len__()
            # if frame_str_lines != (1 + int(shape[0] / self.pix_size)):
            #     for i in range(frame_str.split('\n').__len__()):
            #         print(i, frame_str.split('\n')[i] + '[0m')
            #     print('err')
            #     exit(0)

    def generate_files_mp(self, path: str = '.', multi_process_num: int = 16, audio_vol: float = 0.3, loop_play: bool = False):
        """
        输出zfh和wav文件(只有视频会输出wav文件)

        输出文件会在指定目录下的以输入媒体文件名为名的文件夹里

        :param multi_process_num: 多线程数量, 仅在视频有效
        :param audio_vol: 音量
        :param path: 输出目录
        :param loop_play: 是否循环播放
        :return:
        """

        media = media_to_ndarray_iter(self.file_path, self.pix_size, self.inter_type)
        shape = media.shape
        convert = ndarrays_to_str(self.code_source)
        if not os.path.exists(os.path.join(path, self.file_name)):
            os.makedirs(os.path.join(path, self.file_name))
        with open(os.path.join(path, '{}\\result.zfh'.format(self.file_name)), mode='w') as out_file:
            '''写入 meta_data'''
            out_file.write('//meta_data\n')
            out_file.write('version=zi_fi_hua_v3\n')
            out_file.write('github=github.com/O5-7/pix_player_v3\n')
            out_file.write('media_name={}\n'.format(self.file_name))
            out_file.write('font_type={}\n'.format(self.code_source.font_type))
            out_file.write('font_size={}\n'.format(self.code_source.font_size))
            out_file.write('str_size={},{}\n'.format(
                int(shape[1] / self.pix_size),
                int(shape[0] / self.pix_size)
            ))
            out_file.write('loop_play={}\n'.format(loop_play))
            if media.file_type == 'video':
                """ 导出音频 """
                video = moviepy.editor.VideoFileClip(self.file_path, verbose=False)
                audio = video.audio
                audio = audio.volumex([audio_vol] * 2)
                audio.write_audiofile(os.path.join(path, '{}\\result.wav'.format(self.file_name)), verbose=False)
                out_file.write('audio={}\n'.format(True))
            else:
                out_file.write('audio={}\n'.format(False))
            out_file.write("END_META_DATA\n")
            '''
            写入 str_data
            '''
            print('done')
            ndarrays_list = media.get_media_ndarray_iter()

            range_list = []
            frame_count_per_p = int(media.frame_count / multi_process_num)
            for mp_index in range(multi_process_num):
                range_list.append([mp_index * frame_count_per_p,
                                   (mp_index + 1) * frame_count_per_p])
                if mp_index == multi_process_num - 1:
                    range_list[-1][-1] = media.frame_count

            mp_dict = mp.Manager().dict()
            p_tqdm = mp.Process(target=mp_dict_tqdm, args=(media.frame_count, mp_dict))
            p_tqdm.start()
            mp_pool = []

            for mp_index in range(multi_process_num):
                sp_range = range_list[mp_index]
                mp_pool.append(mp.Process(target=convert_process, args=(
                    deepcopy(ndarrays_list[sp_range[0]:sp_range[1]]),
                    sp_range[0],
                    self.codes_style,
                    mp_index,
                    mp_dict
                )))
            for p in mp_pool:
                p.start()

            for p in mp_pool:
                p.join()
            p_tqdm.join()

            for i in tqdm(range(media.frame_count), ncols=120):
                d, frame_str = mp_dict[i]
                out_file.write('//new_frame\n')
                out_file.write('duration=' + str(d) + '\n')
                out_file.write(frame_str)


if __name__ == '__main__':
    code_source = code_source('./xin_song_ti_16/code_sources_v3.txt',
                              './xin_song_ti_16/code_sources_v3_img_xinsongti_16.png',
                              16,
                              '新宋体'
                              )
    codes_style = codes_style(color=False, codes=True, reverse=True)
    # zi_fu_hua = zi_fu_hua(r'./fldl.gif', code_source, codes_style, pix_size=5, inter_type=cv2.INTER_NEAREST)
    # zi_fu_hua = zi_fu_hua(r'e:/objects/videos/internet_yamero.mp4', code_source, codes_style, pix_size=26, inter_type=cv2.INTER_NEAREST)
    zi_fu_hua = zi_fu_hua(r'./255test.mp4', code_source, codes_style, pix_size=16)
    zi_fu_hua.generate_files_mp(multi_process_num=8, loop_play=True)

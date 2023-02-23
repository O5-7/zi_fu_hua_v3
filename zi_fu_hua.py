from code_source import code_source
from codes_style import codes_style
from media_to_ndarray_iter import media_to_ndarray_iter
from ndarrays_to_str import ndarrays_to_str
import cv2
import os
import time


class zi_fu_hua:
    def __init__(self, source_file: str, codes: code_source, style: codes_style, pix_size: float = -1):
        self.file_path = source_file
        self.code_source = codes
        self.codes_style = style
        self.pix_size = pix_size
        if self.pix_size == -1:
            self.pix_size = codes.font_size

    def generate_files(self, path: str = '.'):
        shape, ndarrays_iter = media_to_ndarray_iter(self.file_path).get_media_ndarray_iter()
        convert = ndarrays_to_str(self.code_source)
        with open(os.path.join(path, 'result.zfh'), mode='w') as out_file:
            '''写入 mata_data'''
            out_file.write('//mata_data\n')
            out_file.write('version=zi_fi_hua_v3\n')
            out_file.write('github=github.com/O5-7/pix_player_v3\n')
            out_file.write('font_type={}\n'.format(self.code_source.font_type))
            out_file.write('font_size={}\n'.format(self.code_source.font_size))
            out_file.write('str_size={},{}\n'.format(
                int(shape[1] / self.pix_size),
                int(shape[0] / self.pix_size)
            ))

            '''
            写入 str_data
            '''
            frame_count = 0
            for d, f in ndarrays_iter:
                out_file.write('//new_frame\n')

                f = cv2.resize(
                    f,
                    (int(shape[1] / self.pix_size), int(shape[0] / self.pix_size)),
                    interpolation=cv2.INTER_AREA
                )
                frame_str = convert.img_to_str(f, (int(shape[0] / self.pix_size), int(shape[1] / self.pix_size)), self.codes_style)
                out_file.write('duration' + str(d) + '\n')
                out_file.write(frame_str)
                frame_count += 1
                print(frame_count)


if __name__ == '__main__':
    code_source = code_source('./xin_song_ti_16/code_sources_v3.txt',
                              './xin_song_ti_16/code_sources_v3_img_xinsongti_16.png',
                              16,
                              '新宋体'
                              )
    codes_style = codes_style(color=True)
    zi_fu_hua = zi_fu_hua('./aya.mp4', code_source, codes_style, pix_size=32)
    zi_fu_hua.generate_files()

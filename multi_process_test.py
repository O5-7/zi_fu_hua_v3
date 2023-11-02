import cv2
import numpy as np
from copy import deepcopy
from codes_style import codes_style
from media_to_ndarray_iter import media_to_ndarray_iter
import multiprocessing as mp
from code_source import code_source
from tqdm import tqdm

from ndarrays_to_str import ndarrays_to_str


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


if __name__ == '__main__':

    media = media_to_ndarray_iter(r'e:/objects/videos/internet_yamero.mp4')

    shape, ndarrays_iter = media.get_media_ndarray_iter()
    pix_size = 5



    codes_style_ = codes_style(color=True, codes=True, reverse=True)

    code_source_ = code_source('./xin_song_ti_16/code_sources_v3.txt',
                               './xin_song_ti_16/code_sources_v3_img_xinsongti_16.png',
                               16,
                               '新宋体'
                               )
    convert_ = ndarrays_to_str(code_source_)

    count = 0
    frame_list = []
    pool = mp.Pool(16)
    out_str_dict = {}
    for d, f in ndarrays_iter:
        frame_list.append(f)
        if frame_list.__len__() == 16:
            result_list = []
            for i in tqdm(range(frame_list.__len__()), ncols=100):
                s_f = frame_list[i]
                result_list.append(
                    pool.apply_async(
                        convert_frame, args=(
                            s_f,
                            (int(shape[0] / pix_size), int(shape[1] / pix_size)),
                            convert_,
                            codes_style_,
                            i,
                        )))
            pool.close()
            pool.join()

            for res in tqdm(result_list, ncols=100):
                index, out_str = res.get()
                print(out_str)
                out_str_dict.update({index: out_str_dict})
            frame_list = []
            pool = mp.Pool(16)

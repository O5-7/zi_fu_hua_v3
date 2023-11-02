import time

import numpy as np
import cv2
from PIL import Image
from collections.abc import Iterable

from tqdm import tqdm


class media_to_ndarray_iter:
    """
    将媒体文件读取为一个资源迭代器和形状元组,

    通过 self.get_media_ndarray_iter()方法

    获取一个元组表示shape

    一个iter,输出 tuple(duration, frame)
    """

    def __init__(self, file: str, pix_size: int, inter_type=cv2.INTER_AREA):
        self.file_path = file
        self.file_type = 'unknown'  # 'unknown', 'image', 'gif', 'video'
        self.shape = (0, 0)
        self.pix_size = pix_size
        self.inter_type = inter_type
        self.frame_count = 0
        if file.endswith(('.jpg', '.png', '.tif', '.bmp', 'jfif')):
            self.file_type = 'image'
            self.frame_count = 1
            self.shape = cv2.imread(self.file_path).shape[:2]
        if file.endswith('.gif'):
            self.file_type = 'gif'
            self.frame_count = Image.open(self.file_path).n_frames
            self.shape = np.array(Image.open(self.file_path).convert('RGB')).shape[:2]
        if file.endswith(('.mp4', '.avi', '.mov')):
            self.file_type = 'video'
            video = cv2.VideoCapture(self.file_path)
            self.frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
            video_w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            video_h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.shape = (video_h, video_w)

    def get_media_ndarray_iter(self):
        """
        返回一个资源迭代器,输出shape:tuple, tuple(duration, frame)

        duration:float  单位ms

        frame:np.ndarray

        :return:shape:tuple, collections.Iterable
        """
        iter_out = None

        if self.file_type == 'image':
            iter_out = self._image_to_ndarray_iter()

        if self.file_type == 'gif':
            iter_out = self._gif_to_ndarray_itery()

        if self.file_type == 'video':
            iter_out = self._video_to_ndarray_iter()
        return iter_out

    def _image_to_ndarray_iter(self):
        """
        返回图片的资源迭代器,且duration=0

        :return: collections.Iterable
        """
        img = np.array(cv2.imread(self.file_path))
        img = self.pix_resize(img)
        if len(img.shape) == 3:
            return [(100, img[:, :, [2, 1, 0]])]
        else:
            return [(100, img)]

    def _gif_to_ndarray_itery(self):
        """
        返回gif的资源迭代器

        :return: collections.Iterable
        """
        gif = Image.open(self.file_path)
        self.frame_count = gif.n_frames
        df_list = []
        while True:
            try:
                duration = int(gif.info['duration'])
                frame = np.array(gif.convert('RGB'))
                frame = self.pix_resize(frame)
                gif.seek(gif.tell() + 1)
                df_list.append((duration, frame))
                # yield duration, frame
            except EOFError:
                break
        return df_list

    def _video_to_ndarray_iter(self):
        """
        返回视频的资源迭代器

        :return: collections.Iterable
        """
        video = cv2.VideoCapture(self.file_path)
        self.frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        video_w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video_fps = float(video.get(cv2.CAP_PROP_FPS))
        video_frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = 1000 / video_fps
        # print(video_w, video_h, video_fps, video_frame_count)

        read_success = True
        frame_read = 0
        rate = 0.0
        time_start = time.time()
        df_list = []
        # while video.isOpened():
        for _ in tqdm(range(self.frame_count), ncols=120):
            frame_read += 1
            read_success, frame = video.read()
            rate_now = frame_read / video_frame_count
            # print(int(((time.time() - time_start) / frame_read) * (video_frame_count - frame_read)), end='s   ')
            rate = rate_now
            # print('{}/{} rate={}%'.format(frame_read, video_frame_count, round(100 * rate, 2)), end='   \n')
            # yield duration, np.array(frame)[:, :, [2, 1, 0]]
            frame = self.pix_resize(frame)
            df_list.append((duration, np.array(frame)[:, :, [2, 1, 0]]))
            # cv2.imshow('1', np.array(frame)[:, :, [2, 1, 0]])
            # cv2.waitKey(1)
        video.release()
        return df_list

    def pix_resize(self, f_input: np.ndarray):
        out = cv2.resize(
            f_input,
            (int(self.shape[1] / self.pix_size), int(self.shape[0] / self.pix_size)),
            interpolation=self.inter_type
        )
        return out


if __name__ == '__main__':
    """
    案例:
    """
    mtn = media_to_ndarray_iter('./aya.mp4')
    shape, ndarray_iter = mtn.get_media_ndarray_iter()
    print(shape)
    for d, f in ndarray_iter:
        print(d, f.shape)

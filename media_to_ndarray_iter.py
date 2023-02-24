import numpy as np
import cv2
from PIL import Image
from collections.abc import Iterable


class media_to_ndarray_iter:
    """
    将媒体文件读取为一个资源迭代器和形状元组,

    通过 self.get_media_ndarray_iter()方法

    获取一个元组表示shape

    一个iter,输出 tuple(duration, frame)
    """

    def __init__(self, file: str):
        self.file_path = file
        self.file_type = 'unknown'
        self.shape = (0, 0)
        if file.endswith(('.jpg', '.png', '.tif', '.bmp', 'jfif')):
            self.file_type = 'image'
        if file.endswith('.gif'):
            self.file_type = 'gif'
        if file.endswith(('.mp4', '.avi', '.mov')):
            self.file_type = 'video'

    def get_media_ndarray_iter(self) -> (tuple, Iterable):
        """
        返回一个资源迭代器,输出shape:tuple, tuple(duration, frame)

        duration:float  单位ms

        frame:np.ndarray

        :return:shape:tuple, collections.Iterable
        """
        iter_out = None

        if self.file_type == 'image':
            iter_out = self._image_to_ndarray_iter()
            self.shape = cv2.imread(self.file_path).shape[:2]

        if self.file_type == 'gif':
            iter_out = self._gif_to_ndarray_itery()
            self.shape = np.array(Image.open(self.file_path).convert('RGB')).shape[:2]

        if self.file_type == 'video':
            iter_out = self._video_to_ndarray_iter()
            video = cv2.VideoCapture(self.file_path)
            video_w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            video_h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

            self.shape = (video_h, video_w)
        print("return")
        return self.shape, iter_out

    def _image_to_ndarray_iter(self) -> Iterable:
        """
        返回图片的资源迭代器,且duration=0

        :return: collections.Iterable
        """
        img = np.array(cv2.imread(self.file_path))
        if len(img.shape) == 3:
            yield 0, img[:, :, [2, 1, 0]]
        else:
            yield 0, img

    def _gif_to_ndarray_itery(self) -> Iterable:
        """
        返回gif的资源迭代器

        :return: collections.Iterable
        """
        gif = Image.open(self.file_path)
        while True:
            try:
                duration = int(gif.info['duration'])
                frame = np.array(gif.convert('RGB'))
                gif.seek(gif.tell() + 1)
                yield duration, frame
            except EOFError:
                break

    def _video_to_ndarray_iter(self) -> Iterable:
        """
        返回视频的资源迭代器

        :return: collections.Iterable
        """
        video = cv2.VideoCapture(self.file_path)
        video_w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video_fps = float(video.get(cv2.CAP_PROP_FPS))
        video_frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = 1000 / video_fps
        # print(video_w, video_h, video_fps, video_frame_count)

        read_success = True
        frame_read = 0
        while video.isOpened():
            frame_read += 1
            read_success, frame = video.read()
            print('rate={}%'.format(round(frame_read * 100 / video_frame_count, 2)), end='   ')
            if not read_success:
                break
            yield duration, np.array(frame)[:, :, [2, 1, 0]]


if __name__ == '__main__':
    """
    案例:
    """
    mtn = media_to_ndarray_iter('./aya.mp4')
    shape, ndarray_iter = mtn.get_media_ndarray_iter()
    print(shape)
    for d, f in ndarray_iter:
        print(d, f.shape)

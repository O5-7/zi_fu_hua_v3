import numpy as np
import cv2
from PIL import Image
from collections.abc import Iterable


class media_to_ndarray_iter:
    """
    将媒体文件读取为一个资源迭代器, 输出tuple(duration, shape, frame)
    """

    def __init__(self, file: str):
        self.file_path = file
        self.file_type = 'unknown'
        if file.endswith(('.jpg', '.png', '.tif', '.bmp', 'jfif')):
            self.file_type = 'image'
        if file.endswith('.gif'):
            self.file_type = 'gif'
        if file.endswith(('.mp4', '.avi', '.mov')):
            self.file_type = 'video'

    def get_media_ndarray_iter(self) -> Iterable:
        """
        返回一个资源迭代器,输出 tuple(duration, shape, frame)

        duration:float  单位ms

        shape:tuple(int, int)  (h,w)

        frame:np.ndarray

        :return: collections.Iterable
        """
        iter_out = None
        if self.file_type == 'image':
            iter_out = self._image_to_ndarray_iter()
        if self.file_type == 'gif':
            iter_out = self._gif_to_ndarray_itery()
        if self.file_type == 'video':
            iter_out = self._video_to_ndarray_iter()
        return iter_out

    def _image_to_ndarray_iter(self) -> Iterable:
        """
        返回图片的资源迭代器,且duration=0

        :return: collections.Iterable
        """
        img = np.array(cv2.imread(self.file_path))
        yield 0, img.shape[:2], np.array(img)

    def _gif_to_ndarray_itery(self) -> Iterable:
        """
        返回gif的资源迭代器

        :return: collections.Iterable
        """
        gif = Image.open(self.file_path)
        shape = gif.size
        while True:
            try:
                duration = int(gif.info['duration'])
                frame = np.array(gif.convert('RGB'))
                gif.seek(gif.tell() + 1)
                yield duration, shape, frame
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
        print(video_w, video_h, video_fps, video_frame_count)

        read_success = True
        frames = []
        while video.isOpened():
            read_success, frame = video.read()
            if not read_success: break
            yield duration, (video_h, video_w), np.array(frame)


if __name__ == '__main__':
    """
    案例:
    """
    mtn = media_to_ndarray_iter('./Mitski.png')
    for d, s, f in mtn.get_media_ndarray_iter():
        print(d, s, f.shape)

import numpy as np
import cv2

from PIL import Image
from PIL import ImageSequence


class media_to_ndarray_iter:
    def __init__(self, file: str):
        self.file_path = file
        self.file_type = 'unknown'
        if file.endswith(('.jpg', '.png', '.tif', '.bmp')):
            self.file_type = 'image'
        if file.endswith('.gif'):
            self.file_type = 'gif'
        if file.endswith(('.mp4', '.avi', '.mov')):
            self.file_type = 'video'

    def get_media_ndarray_iter(self) -> np.ndarray:
        pass

    def image_to_ndarray_iter(self):
        img = np.array(cv2.imread(self.file_path))
        yield 0, img.shape, np.array(img)

    def gif_to_ndarray_itery(self):
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

    def video_to_ndarray_iter(self):
        video = cv2.VideoCapture(self.file_path)
        video_w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video_fps = float(video.get(cv2.CAP_PROP_FPS))
        video_frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = 1 / video_fps
        print(video_w, video_h, video_fps, video_frame_count)

        read_success = True
        frames = []
        while video.isOpened() and read_success:
            read_success, frame = video.read()
            yield duration, (video_w, video_h), np.array(frame)


if __name__ == '__main__':
    mtn = media_to_ndarray_iter('./aya.mp4')
    for x, y, z in mtn.video_to_ndarray_iter():
        print(z.shape)

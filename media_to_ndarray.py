import numpy as np
import cv2

from PIL import Image
from PIL import ImageSequence


class media_to_ndarray:
    def __init__(self, file: str):
        self.file_path = file
        self.file_type = 'unknown'
        if file.endswith(('.jpg', '.png', '.tif', '.bmp')):
            self.file_type = 'image'
        if file.endswith('.gif'):
            self.file_type = 'gif'
        if file.endswith(('.mp4', '.avi', '.mov')):
            self.file_type = 'video'

    def get_media_ndarray(self) -> np.ndarray:
        pass

    def image_to_ndarray(self) -> np.ndarray:
        img = cv2.imread(self.file_path)
        return np.array(img)

    def gif_to_ndarray(self) -> (np.ndarray, np.ndarray):
        gif = Image.open('./fldl.gif')
        durations = []
        frames = []
        while True:
            try:
                durations.append(gif.info['duration'])
                frame = gif.convert('RGB')
                frames.append(np.array(frame))
                gif.seek(gif.tell() + 1)
            except EOFError:
                break
        return np.array(durations), np.array(frames)


if __name__ == '__main__':
    mtn = media_to_ndarray('./fldl.gif')
    d, f = mtn.gif_to_ndarray()
    print(d.shape, f.shape)

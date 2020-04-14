from time import time


class Camera(object):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""

    def __init__(self):
        path = '/home/atmc/Desktop/CloudArcade-master/Code/bmps/'
        self.c = 0
        self.frames = [open(path + str(self.c+1) + '.bmp', 'rb').read() for count in range(20)]

    def get_frame(self):
        if frames[self.c]:
            self.c += 1
            return self.frames[self.c]

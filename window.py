class Window(object):
    id = ""
    start_width = None
    start_height = None
    width = None
    height = None

    def __init__(self):
        pass

    def __init__(self, idk="", start_width=0, start_height=0, width=0, height=0):
        self.id = idk
        self.start_width = start_width
        self.start_height = start_height
        self.width = width
        self.height = height

    def __str__(self):
        return "Window [id=" + self.id + ", start_width=" + str(self.start_width) + ", start_height=" \
               + str(self.start_height) + ", width=" + str(self.width) + ", height=" + str(self.height) + "]"


def new_window(idk, start_width, start_height, width, height):
    return Window(idk, start_width, start_height, width, height)

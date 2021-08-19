class Screen(object):
    name = ""
    start_width = None
    start_height = None
    width = None
    height = None

    def __init__(self, name, start_width, start_height, width, height):
        self.name = name
        self.start_width = start_width
        self.start_height = start_height
        self.width = width
        self.height = height

    def __str__(self):
        return "Screen [name=" + self.name + ", start_width=" + str(self.start_width) + ", start_height=" + \
               str(self.start_height) + ", width=" + str(self.width) + ", height=" + str(self.height) + "]"


def new_screen(name, start_width, start_height, width, height):
    return Screen(name, start_width, start_height, width, height)

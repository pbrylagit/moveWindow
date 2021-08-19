import command
import sys
from screen import new_screen
from window import Window

debug = "on"


def echo(to_print):
    if debug == "on":
        print(to_print)


def place_window(window, x, y, screen_width, screen_height):
    if command.check_if_maximized(window.id):
        command.minimize(window.id)
    command.move_window_cmd(x, y, window.id, screen_width, screen_height)


def move_on_screen(window, screen):
    echo("move_on_screen")
    if "U" == direction:
        move_up(window, screen)
    if "D" == direction:
        move_down(window, screen)
    if "L" == direction:
        move_left(window, screen)
    if "R" == direction:
        move_right(window, screen)


def move_up(window, screen):
    echo("move_up")
    bar_size = command.get_bar_size()
    start_height = screen.start_height + bar_size
    half_height = (screen.height / 2) - 37
    place_window(window, screen.start_width, start_height, screen.width, half_height)


def move_down(window, screen):
    echo("move_down")
    bar_size = command.get_bar_size()
    start_height = screen.start_height + (screen.height / 2) + bar_size / 2
    half_height = (screen.height / 2) - 37
    place_window(window, screen.start_width, start_height, screen.width, half_height)


def move_left(window, screen):
    echo("move_left")
    bar_size = command.get_bar_size()
    start_height = bar_size + screen.start_height
    half_height = screen.height - (bar_size * 2)
    half_width = screen.width / 2
    place_window(window, screen.start_width, start_height, half_width, half_height)


def move_right(window, screen):
    echo("move_right")
    bar_size = command.get_bar_size()
    start_height = bar_size + screen.start_height
    half_height = screen.height - (bar_size * 2)
    half_width = screen.width / 2
    start_width = screen.start_width + screen.width / 2
    place_window(window, start_width, start_height, half_width, half_height)


def get_screens():
    echo("\n" +get_screens.__name__)
    connected_screens = command.get_screens()
    echo("Connected screens from xrandr:\n" + connected_screens)
    screens = str(connected_screens).splitlines()
    list_of_screens = []
    # example: eDP-1 connected 1366x768+277+1080 ...
    for connected_screen in screens:
        screen_info = connected_screen.split(" ")
        name = screen_info[0]
        resolution = screen_info[2]
        if "primary" == resolution:
            resolution = screen_info[3]
        width = int(resolution.split("x")[0])
        height = int(resolution.split("+")[0].split("x")[1])
        start_width = int(resolution.split("+")[1])
        start_height = int(resolution.split("+")[2])
        list_of_screens.append(new_screen(name, start_width, start_height, width, height))
    list_of_screens.sort(key=lambda x: int(x.width), reverse=True)
    echo("Screen objects:")
    for s in list_of_screens:
        echo(s)
    return list_of_screens


def get_window_info():
    echo("\n" + get_window_info.__name__)
    window_id = command.get_window_id()
    # window_id = str(75497473)
    temp_window_info = str(command.get_window_info(window_id)).splitlines()

    window = Window()
    window.id = window_id

    for line in temp_window_info:
        if "Absolute upper-left X:" in line:
            window.start_width = int(line.split(":")[1])
            echo(line)
        if "Absolute upper-left Y:" in line:
            window.start_height = int(line.split(":")[1])
            echo(line)
        if "Width:" in line:
            window.width = int(line.split(":")[1])
            echo(line)
        if "Height:" in line:
            window.height = int(line.split(":")[1])
            echo(line)
    echo(window)
    return window


def select_screen(window, screens):
    echo("\n" + select_screen.__name__)
    x = window.start_width
    y = window.start_height

    for screen in screens:
        screen_start_width = screen.start_width + screen.width - 1
        screen_start_height = screen.start_height + screen.height - 1

        echo(str(screen.start_width) + " <= " + str(x) + " <= " + str(screen_start_width) + " and " +
             str(screen.start_height) + " <= " + str(y) + " <= " + str(screen_start_height))

        if screen.start_width <= x <= screen_start_width and screen.start_height <= y <= screen_start_height:
            echo("Selected screen: " + str(screen))
            return screen


def move_between_screens(screens, window_info):
    used_screen = select_screen(window_info, screens)
    final_screen = 0
    if "U" == direction:
        if command.check_if_horz_maximized(window_info.id) \
                and window_info.start_height >= used_screen.start_height + (used_screen.height / 2):
            maximize(window_info.id)
        else:
            for screen in screens:
                if used_screen.start_height > screen.start_height and used_screen.start_height == screen.height:
                    if command.check_if_maximized:
                        final_screen = screen
    if "D" == direction:
        if command.check_if_horz_maximized(window_info.id)\
                and window_info.start_height <= used_screen.start_height + (used_screen.height / 2):
            maximize(window_info.id)
        else:
            for screen in screens:
                if used_screen.start_height < screen.start_height and used_screen.height == screen.start_height:
                    if command.check_if_maximized:
                        final_screen = screen
    if "L" == direction:
        if command.check_if_vert_maximized(window_info.id) \
                and window_info.start_width >= used_screen.start_width + (used_screen.width / 2):
            maximize(window_info.id)
        else:
            for screen in screens:
                if used_screen.start_width > screen.start_width and used_screen.start_width == screen.width:
                    if command.check_if_maximized:
                        final_screen = screen
    if "R" == direction:
        if command.check_if_vert_maximized(window_info.id)\
                and window_info.width <= used_screen.width + (used_screen.width / 2):
            maximize(window_info.id)
        else:
            for screen in screens:
                if used_screen.start_width < screen.start_width and used_screen.width == screen.start_width:
                    if command.check_if_maximized:
                        final_screen = screen
    if final_screen == 0:
        echo("no final screen")
    else:
        move_and_maximize(window_info.id, final_screen.start_width, final_screen.start_height)


def center_screen(screens, window_info):
    used_screen = select_screen(window_info, screens)
    if "S" == direction:
        x = used_screen.width * 0.2
        y = used_screen.height * 0.2
        screen_height = used_screen.height * 0.6
        screen_width = used_screen.width * 0.6
        place_window(window_info, x, y, screen_width, screen_height)
    if "V" == direction:
        bar_size =37
        x = used_screen.width * 0.2
        y = bar_size
        screen_height = used_screen.height - bar_size - 7
        screen_width = used_screen.width * 0.6
        place_window(window_info, x, y, screen_width, screen_height)

def maximize(window_id):
    command.minimize(window_id)
    command.maximize(window_id)


def move_and_maximize(window_id, x, y):
    command.minimize(window_id)
    command.move_window_x_y(window_id, x, y)
    command.maximize(window_id)


def main():
    screens = get_screens()
    window_info = get_window_info()
    # move_window(screens, window_info)
    if direction in ("U", "D", "L", "R"):
        move_between_screens(screens, window_info)
    elif direction in ("S", "V"):
        center_screen(screens, window_info)


direction = sys.argv[1]
echo("install xdotool")
echo("install wmctrl")
main()

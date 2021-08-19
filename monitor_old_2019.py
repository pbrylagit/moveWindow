import command
import sys
from screen import new_screen


debug = "on"


def echo(to_print):
    if debug == "on":
        print(to_print)


def get_screens():
    connected_screens = command.get_monitors_cmd()
    screens = str(connected_screens).splitlines()
    list_of_screens = []
    # example: eDP-1 connected 1366x768+277+1080 ...
    for connected_screen in screens:
        screen_info = connected_screen.split(" ")
        name = screen_info[0]
        resolution = screen_info[2]
        width = int(resolution.split("x")[0])
        height = int(resolution.split("+")[0].split("x")[1])
        start_width = int(resolution.split("+")[1])
        start_height = int(resolution.split("+")[2])
        list_of_screens.append(new_screen(name, width, height, start_width, start_height))
    list_of_screens.sort(key=lambda x: int(x.width), reverse=True)
    for s in list_of_screens:
        echo(s)
    return list_of_screens


def move_window(x, y, screen_width, screen_height):
    if command.check_if_maximized(window_id):
        command.minimize(window_id)
    command.move_window_cmd(x, y, window_id, screen_width, screen_height)


def move_on_monitor(monitor):
    echo("move_on_one_monitor")
    bar_size = command.get_bar_size()
    if "U" == direction:
        move_up(monitor, bar_size)
    if "D" == direction:
        move_down(monitor, bar_size)

    y = bar_size + monitor.start_height
    half_height = monitor.height - (bar_size * 2)
    half_width = monitor.width / 2
    if "L" == direction:
        move_left(y, monitor, half_height, half_width)
    if "R" == direction:
        move_right(y, monitor, half_height, half_width)


def move_up(monitor, bar_size):
    echo("move_up")
    y = monitor.start_height + bar_size
    half_height = (monitor.height / 2) - 37
    move_window(monitor.start_width, y, monitor.width, half_height)


def move_down(monitor, bar_size):
    echo("move_down")
    y = monitor.start_height + (monitor.height / 2) + bar_size / 2
    half_height = (monitor.height / 2) - 37
    move_window(monitor.start_width, y, monitor.width, half_height)


def move_left(y, monitor, half_height, half_width):
    echo("move_left")
    move_window(monitor.start_width, y, half_width, half_height)


def move_right(y, monitor, half_height, half_width):
    echo("move_right")
    start_width = monitor.start_width + monitor.width / 2
    move_window(start_width, y, half_width, half_height)


def select_monitor(screens):
    echo("select_monitor()")
    x = command.get_x_window_position(window_id)
    y = command.get_y_window_position(window_id)
    echo("window x " + str(x))
    echo("window y " + str(y))

    for scr in screens:
        screen_start_width = scr.start_width + scr.width
        screen_start_height = scr.start_height + scr.height

        echo(str(x) + " >= " + str(scr.start_width) + " and " + str(x) + " <= " + str(screen_start_width) + " and " + str(y) + " >= " + str(scr.start_height) + " and " + str(y) + " <= " + str(screen_start_height))

        if x >= scr.start_width and x <= screen_start_width and y >= scr.start_height and y <= screen_start_height:
            return scr


screen_list = get_screens()
number_of_screens = len(screen_list)
echo("number_of_screens " + str(number_of_screens))
direction = sys.argv[1]
window_id = command.get_window_id()

#move_on_monitor(screen_list[0])

#if number_of_screens == 1:
#    move_on_one_monitor(screen_list[0])
if number_of_screens > 1:
    selected_monitor = select_monitor(screen_list)
    echo(selected_monitor)
    move_on_monitor(selected_monitor)


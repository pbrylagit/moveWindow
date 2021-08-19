import subprocess


def exec_command(command):
    process = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    (output, error) = process.communicate()
    return str(output).strip()


def check_if_maximized(window_id):
    print(window_id)
    horz_maxed = exec_command('xprop -id "' + window_id +
                              '" _NET_WM_STATE | grep \'_NET_WM_STATE_MAXIMIZED_HORZ\'')
    vert_maxed = exec_command('xprop -id "' + window_id +
                              '" _NET_WM_STATE | grep \'_NET_WM_STATE_MAXIMIZED_VERT\'')
    if len(horz_maxed) > 0 and len(vert_maxed) > 0:
        return True


def check_if_vert_maximized(window_id):
    print(window_id)
    horz_maxed = exec_command('xprop -id "' + window_id +
                              '" _NET_WM_STATE | grep \'_NET_WM_STATE_MAXIMIZED_HORZ\'')
    vert_maxed = exec_command('xprop -id "' + window_id +
                              '" _NET_WM_STATE | grep \'_NET_WM_STATE_MAXIMIZED_VERT\'')
    print(len(horz_maxed))
    print(vert_maxed)
    if len(horz_maxed) == 0 and len(vert_maxed) > 0:
        return True


def check_if_horz_maximized(window_id):
    print(window_id)
    horz_maxed = exec_command('xprop -id "' + window_id +
                              '" _NET_WM_STATE | grep \'_NET_WM_STATE_MAXIMIZED_HORZ\'')
    vert_maxed = exec_command('xprop -id "' + window_id +
                              '" _NET_WM_STATE | grep \'_NET_WM_STATE_MAXIMIZED_VERT\'')
    if len(horz_maxed) > 0 and len(vert_maxed) == 0:
        return True


def get_bar_size():
    return int(exec_command('xfconf-query -c xfce4-panel -p /panels -lv | grep size | awk \'{print $2}\''))


def get_screens():
    return exec_command('xrandr | grep " connected"')


def get_window_id():
    return exec_command('xdotool getactivewindow')


def get_window_info(window_id):
    print(window_id)
    return exec_command('xwininfo -id ' + str(window_id))


def maximize(window_id):
    exec_command('wmctrl -ir ' + str(window_id) +
                 ' -b add,maximized_vert,maximized_horz')


def maximize_vert(window_id):
    exec_command('wmctrl -ir ' + str(window_id) + ' -b add,maximized_vert')


def maximize_horz(window_id):
    exec_command('wmctrl -ir ' + str(window_id) + ' -b add,maximized_horz')


def minimize(window_id):
    exec_command('wmctrl -ir "' + window_id +
                 '" -b remove,maximized_vert,maximized_horz')


def move_window_cmd(x, y, window_id, width, height):
    exec_command('xdotool windowmove "' + window_id +
                 '" ' + str(int(x - 2)) + ' ' + str(y))
    exec_command('xdotool windowsize "' + window_id +
                 '" ' + str(width) + ' ' + str(height))


def window_size(window_id, width, height):
    exec_command('xdotool windowsize "' + window_id +
                 '" ' + str(width) + ' ' + str(height))


def move_window_x_y(window_id, x, y):
    exec_command('xdotool windowmove ' + str(window_id) +
                 ' ' + str(x) + ' ' + str(y))

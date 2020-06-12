#!/usr/bin/env python3
"""
Hotkeys used with xournal++, since it is not possible to
edit keyboard shortcuts in this application (bummer...)

Author: Pedro P. Bittencourt
Link:   https://github.com/pbittencourt

Original code via:
https://nitratine.net/blog/post/how-to-make-hotkeys-in-python/

Thanks to reddit user danielroseman:
https://www.reddit.com/r/learnpython/comments/h1457d/execute_function_via_dictionary_strings/
"""


from pynput.keyboard import Key, KeyCode, Listener
from pynput.mouse import Button, Controller
from time import sleep


def get_vk(key):
    """
    Get the virtual key code from a key.
    These are used so case/shift modifications are ignored.
    """
    return key.vk if hasattr(key, 'vk') else key.value.vk


def is_combination_pressed(combination):
    """
    Check if a combination is satisfied using
    the keys pressed in pressed_vks
    """
    return all([get_vk(key) in pressed_vks for key in combination])


def on_press(key):
    """ When a key is pressed """
    vk = get_vk(key)  # Get the key's vk
    pressed_vks.add(vk)  # Add it to the set of currently pressed keys

    # Loop through each combination
    for combination in combination_to_function:
        # Check if all keys in the combination are pressed
        if is_combination_pressed(combination):
            func, params = combination_to_function[combination]
            func(*params)


def on_release(key):
    """ When a key is released """
    vk = get_vk(key)  # Get the key's vk
    pressed_vks.remove(vk)  # Remove it from the set of currently pressed keys

    # Exit program when ESC is pressed
    if key == Key.esc:
        # Stop listener
        print('\n\nG00DBY3 MR R0B07!\n')
        return False


def single_menu(x, msg):
    """ Press only one button """
    mouse.position = (x, 45)
    mouse.click(Button.left, 1)
    print(msg)
    pass


def double_menu(x1, y1, x2, y2, msg):
    """ Open a dropdown menu and then select a tool """
    # click on arrow to open menu
    mouse.position = (x1, y1)
    mouse.click(Button.left, 1)
    sleep(0.25)

    # select tool
    mouse.position = (x2, y2)
    mouse.click(Button.left, 1)
    print(msg)


combination_to_function = {
    # Create a mapping of keys to function (use frozenset
    # as sets/lists are not hashable - so they can't be
    # used as keys)

    # INK COLORS
    frozenset([KeyCode(vk=114)]): [  # R
        single_menu, [1159, 'ink_red']
    ],
    frozenset([KeyCode(vk=103)]): [  # G
        single_menu, [1004, 'ink_green']
    ],
    frozenset([KeyCode(vk=98)]): [  # B
        single_menu, [1097, 'ink_blue']
    ],

    frozenset([KeyCode(vk=107)]): [  # K
        single_menu, [973, 'ink_black']
    ],
    frozenset([KeyCode(vk=108)]): [  # L
        single_menu, [1128, 'ink_grey']
    ],

    frozenset([Key.ctrl, KeyCode(vk=114)]): [  # Ctrl + R
        single_menu, [1190, 'ink_pink']
    ],
    frozenset([Key.ctrl, KeyCode(vk=103)]): [  # Ctrl + G
        single_menu, [1066, 'ink_light_green']
    ],
    frozenset([Key.ctrl, KeyCode(vk=98)]): [  # Ctrl + B
        single_menu, [1035, 'ink_light_blue']
    ],
    frozenset([KeyCode(vk=111)]): [  # O
        single_menu, [1221, 'ink_orange']
    ],
    frozenset([KeyCode(vk=121)]): [  # Y
        single_menu, [1252, 'ink_yellow']
    ],

    # STROKE FORMATS
    frozenset([KeyCode(vk=44)]): [  # ,
        double_menu, [354, 50, 354, 70, 'stroke_standard']
    ],
    frozenset([KeyCode(vk=46)]): [  # .
        double_menu, [354, 50, 354, 145, 'stroke_dotted']
    ],
    frozenset([KeyCode(vk=59)]): [  # ;
        double_menu, [354, 50, 354, 95, 'stroke_dashed']
    ],

    # TOOLS
    frozenset([KeyCode(vk=39)]): [  # "
        single_menu, [590, 'on_off_tools']
    ],
    frozenset([KeyCode(vk=112)]): [  # P
        single_menu, [320, 'pen']
    ],
    frozenset([KeyCode(vk=101)]): [  # E
        single_menu, [385, 'eraser']
    ],
    frozenset([KeyCode(vk=104)]): [  # H
        single_menu, [456, 'highlighter']
    ],

    frozenset([KeyCode(vk=231)]): [  # ç
        double_menu, [618, 50, 618, 70, 'rectangle']
    ],
    frozenset([KeyCode(vk=65107)]): [  # ~
        double_menu, [618, 50, 618, 120, 'arrow']
    ],
    frozenset([KeyCode(vk=93)]): [  # ]
        double_menu, [618, 50, 618, 145, 'line']
    ],

    # SELECTION
    frozenset([KeyCode(vk=65105)]): [  # `
        double_menu, [700, 50, 700, 75, 'select_rectangle']
    ],
    frozenset([KeyCode(vk=91)]): [  # [
        double_menu, [700, 50, 700, 125, 'select_object']
    ],

    # THICKNESS
    frozenset([KeyCode(vk=48)]): [single_menu, [810, 'thickness light']],  # )
    frozenset([KeyCode(vk=45)]): [single_menu, [844, 'thickness medium']],  # -
    frozenset([KeyCode(vk=61)]): [single_menu, [877, 'thickness strong']],  # +
}

# Send start message
print('\nStart monitoring ... \n')

# Set a mouse Controller
mouse = Controller()

# The currently pressed keys (initially empty)
pressed_vks = set()

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

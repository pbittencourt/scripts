#!/usr/bin/python3
"""
Atalhos de teclado para serem usados com o xournal++, uma vez que
não há a possibilidade de customizar atalhos de forma nativa no app.
Author: Pedro P. Bittencourt
Link:   https://github.com/pbittencourt
"""


from pynput.keyboard import Key, KeyCode, Listener
from pynput.mouse import Button, Controller
from time import sleep


# Send start message
print('\nStart monitoring ... \n')

# Set a mouse Controller
mouse = Controller()

# The currently pressed keys (initially empty)
pressed_vks = set()


def get_vk(key):
    """ Get the virtual key code from a key. These are used so case/shift modifications are ignored. """
    return key.vk if hasattr(key, 'vk') else key.value.vk


def is_combination_pressed(combination):
    """ Check if a combination is satisfied using the keys pressed in pressed_vks """
    return all([get_vk(key) in pressed_vks for key in combination])


def on_press(key):
    """ When a key is pressed """
    vk = get_vk(key)  # Get the key's vk
    pressed_vks.add(vk)  # Add it to the set of currently pressed keys

    for combination in combination_to_function:  # Loop through each combination
        if is_combination_pressed(combination):  # Check if all keys in the combination are pressed
            func, params = combination_to_function[combination]
            func(*params)


def on_release(key):
    """ When a key is released """
    vk = get_vk(key)  # Get the key's vk
    pressed_vks.remove(vk)  # Remove it from the set of currently pressed keys
    if key == Key.esc:
        # Stop listener
        print('\n\nG00DBY3 MR R0B07!\n')
        return False


def single_menu(x, y, msg):
    """ Press only one button """
    mouse.position = (x, y)
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


# Create a mapping of keys to function (use frozenset as sets/lists are not hashable - so they can't be used as keys)
# Note the missing `()` after function_1 and function_2 as want to pass the function, not the return value of the function
combination_to_function = {
    frozenset([Key.ctrl, KeyCode(vk=114)]): [single_menu, [20, 10, 'ink_red']],
    frozenset([Key.ctrl, KeyCode(vk=103)]): [single_menu, [40, 10, 'ink_green']],
    frozenset([Key.ctrl, KeyCode(vk=98)]): [single_menu, [60, 10, 'ink_blue']],
}


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

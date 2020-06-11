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


def ink_black():
    mouse.position = (973, 40)
    mouse.click(Button.left, 1)
    print('executei função ink_black')


def ink_green():
    mouse.position = (1004, 46)
    mouse.click(Button.left, 1)
    print('ink_green')


def ink_light_blue():
    mouse.position = (1035, 46)
    mouse.click(Button.left, 1)
    print('ink_light_blue')


def ink_light_green():
    mouse.position = (1066, 46)
    mouse.click(Button.left, 1)
    print('ink_light_green')


def ink_blue():
    mouse.position = (1097, 46)
    mouse.click(Button.left, 1)
    print('ink_blue')


def ink_grey():
    mouse.position = (1128, 46)
    mouse.click(Button.left, 1)
    print('ink_grey')


def ink_red():
    mouse.position = (1159, 46)
    mouse.click(Button.left, 1)
    print('ink_red')


def ink_pink():
    mouse.position = (1190, 46)
    mouse.click(Button.left, 1)
    print('ink_pink')


def ink_orange():
    mouse.position = (1221, 46)
    mouse.click(Button.left, 1)
    print('ink_orange')


def ink_yellow():
    mouse.position = (1252, 46)
    mouse.click(Button.left, 1)
    print('ink_yellow')


def stroke_standard():
    # click on arrow to open menu
    mouse.position = (354, 50)
    mouse.click(Button.left, 1)
    sleep(0.25)

    # select stroke
    mouse.position = (354, 70)
    mouse.click(Button.left, 1)
    print('stroke_standard')


def stroke_dashed():
    # click on arrow to open menu
    mouse.position = (354, 50)
    mouse.click(Button.left, 1)
    sleep(0.25)

    # select stroke
    mouse.position = (354, 95)
    mouse.click(Button.left, 1)
    print('stroke_dashed')


def stroke_dotted():
    # click on arrow to open menu
    mouse.position = (354, 50)
    mouse.click(Button.left, 1)
    sleep(0.25)

    # select stroke
    mouse.position = (354, 145)
    mouse.click(Button.left, 1)
    print('stroke dotted')


def pen():
    mouse.position = (320, 50)
    mouse.click(Button.left, 1)

    stroke_standard()
    print('pen')


def eraser():
    mouse.position = (385, 50)
    mouse.click(Button.left, 1)
    print('eraser')


def highlighter():
    mouse.position = (456, 50)
    mouse.click(Button.left, 1)
    print('highlighter')

    sleep(0.15)
    line()
    sleep(0.15)
    stroke_standard()


def on_off_tools():
    mouse.position = (590, 50)
    mouse.click(Button.left, 1)
    print('on_off_tools')


def rectangle():
    # click on arrow to open menu
    mouse.position = (618, 50)
    mouse.click(Button.left, 1)
    sleep(0.25)

    # select tool
    mouse.position = (618, 70)
    mouse.click(Button.left, 1)
    print('rectangle')


def arrow():
    # click on arrow to open menu
    mouse.position = (618, 50)
    mouse.click(Button.left, 1)
    sleep(0.25)

    # select tool
    mouse.position = (618, 120)
    mouse.click(Button.left, 1)
    print('arrow')


def line():
    # click on arrow to open menu
    mouse.position = (618, 50)
    mouse.click(Button.left, 1)
    sleep(0.25)

    # select tool
    mouse.position = (618, 145)
    mouse.click(Button.left, 1)
    print('line')


def select_rectangle():
    # click on arrow to open menu
    mouse.position = (700, 50)
    mouse.click(Button.left, 1)
    sleep(0.25)

    # select tool
    mouse.position = (700, 75)
    mouse.click(Button.left, 1)
    print('select_rectangle')


def select_object():
    # click on arrow to open menu
    mouse.position = (700, 50)
    mouse.click(Button.left, 1)
    sleep(0.25)

    # select tool
    mouse.position = (700, 125)
    mouse.click(Button.left, 1)
    print('select_object')


def thick1():
    mouse.position = (810, 46)
    mouse.click(Button.left, 1)
    print('thick1')


def thick2():
    mouse.position = (844, 46)
    mouse.click(Button.left, 1)
    print('thick2')


def thick3():
    mouse.position = (877, 46)
    mouse.click(Button.left, 1)
    print('thick3')


def get_vk(key):
    """
    Get the virtual key code from a key.
    These are used so case/shift modifications are ignored.
    """
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
            combination_to_function[combination]()  # If so, execute the function


def on_release(key):
    """ When a key is released """
    if key == Key.esc:
        # Stop listener
        print('\n\nG00DBY3 MR R0B07!\n')
        return False

    vk = get_vk(key)  # Get the key's vk
    pressed_vks.remove(vk)  # Remove it from the set of currently pressed keys


# Create a mapping of keys to function (use frozenset as sets/lists are not hashable - so they can't be used as keys)
# Note the missing `()` after function_1 and function_2 as want to pass the function, not the return value of the function
combination_to_function = {
    # INK COLORS
    frozenset([KeyCode(vk=114)]): ink_red, # R
    frozenset([KeyCode(vk=103)]): ink_green, # G
    frozenset([KeyCode(vk=98)]): ink_blue, # B

    frozenset([KeyCode(vk=107)]): ink_black, # K
    frozenset([KeyCode(vk=108)]): ink_grey, # L

    frozenset([Key.ctrl, KeyCode(vk=114)]): ink_pink, # Ctrl + R
    frozenset([Key.ctrl, KeyCode(vk=103)]): ink_light_green, # Ctrl + G
    frozenset([Key.ctrl, KeyCode(vk=98)]): ink_light_blue, # Ctrl + B
    frozenset([KeyCode(vk=111)]): ink_orange, # O
    frozenset([KeyCode(vk=121)]): ink_yellow, # Y

    # STROKE FORMATS
    frozenset([KeyCode(vk=44)]): stroke_standard, # ,
    frozenset([KeyCode(vk=46)]): stroke_dotted, # .
    frozenset([KeyCode(vk=59)]): stroke_dashed, # ;

    # TOOLS
    frozenset([KeyCode(vk=39)]): on_off_tools, # "
    frozenset([KeyCode(vk=112)]): pen, # P
    frozenset([KeyCode(vk=101)]): eraser, # E
    frozenset([KeyCode(vk=104)]): highlighter, # H

    frozenset([KeyCode(vk=231)]): rectangle, # ç
    frozenset([KeyCode(vk=65107)]): arrow, # ~
    frozenset([KeyCode(vk=93)]): line, # ]

    # SELECTION
    frozenset([KeyCode(vk=65105)]): select_rectangle, # `
    frozenset([KeyCode(vk=91)]): select_object, # [

    # THICKNESS
    frozenset([KeyCode(vk=48)]): thick1, # )
    frozenset([KeyCode(vk=45)]): thick2, # -
    frozenset([KeyCode(vk=61)]): thick3, # +
}


# Send start message
print('\nStart monitoring ... \n')

# Set a mouse Controller
mouse = Controller()

# The currently pressed keys (initially empty)
pressed_vks = set()

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

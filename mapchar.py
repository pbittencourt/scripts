#!/usr/bin/python3


from pynput.keyboard import Key, KeyCode, Listener

# The currently active modifiers
current = set()

# Combo
combo = [
    #Q    W    E    R    T    Y    U    I    O    P
    113, 119, 101, 114, 116, 121, 117, 105, 111, 112
]

def get_vk(key):
    return key.vk if hasattr(key, 'vk') else key.value.vk


def on_press(key):
    vk = get_vk(key)  # Get the key's vk
    print('Pressionei {} de código {}'.format(key, vk))

    if vk in combo:
        print('YES')

def on_release(key):
    print('{0} release'.format(key))
    if key == Key.esc:
        # Stop listener
        return False

# Collect events until released
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

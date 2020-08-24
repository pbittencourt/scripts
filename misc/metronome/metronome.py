#!/usr/bin/env python3
"""Simple Metronome"""
from subprocess import Popen
from time import sleep
import argparse

# default sounds: head and tail
head = '/home/monolito/metronome/samples/perc-metal.wav'
tail = '/home/monolito/metronome/samples/perc-808.wav'

parser = argparse.ArgumentParser(description='Simple Metronome')
parser.add_argument('-b', '--bpm', metavar='bpm',
                   default=60, help='Beats per minute')
parser.add_argument('-c', '--compass', metavar='compass',
                   default=4, help='Notes per compass')

args = parser.parse_args()

bpm = int(args.bpm)
compass = int(args.compass)
delay = 60/bpm

while True:
    beat = 0
    while beat < compass:
        sleep(delay)
        sound = head if beat == 0 else tail
        Popen(['aplay', '-q', sound])
        beat += 1

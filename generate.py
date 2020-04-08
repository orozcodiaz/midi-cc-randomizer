#!/usr/bin/env python3

# This script provide the functionality to generate random MIDI control messages based on the mapping file
# It allows you to randomly change parameters on the MIDI device and get the absolutely new sound every time
# You'll need MIDI output connected to your computer, MIDI cable and the hardware synthesizer

import rtmidi
import random
import json
import sys

from rtmidi.midiconstants import CONTROL_CHANGE

print('\x1bc')

if len(sys.argv) == 1:
    print("Usage:",sys.argv[0],"mapping-file-name.json\n")
    exit()

mappingFile = sys.argv[1]

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if not available_ports:
    print("No MIDI outputs detected")
    exit()

print("Available output ports:")
for idx, val in enumerate(available_ports):
    print("MIDI output",idx,":", val)

selected_port = input("MIDI output to use: ")

if not selected_port:
    print("You have to select MIDI output")
    exit()

midiout.open_port(int(selected_port))

print('\x1bc')

with midiout:
    try:
        with open(mappingFile) as mappingFileHandler:
            jsonObject = json.load(mappingFileHandler)

            while True:
                print('Selected output:',available_ports[int(selected_port)])
                print('Selected mapping:',mappingFile,'\n')

                for element in jsonObject: 
                    if element['type'] == 'int':
                        randomizedValue = random.randrange(0, 127)

                    if element['type'] == 'bool':
                        randomizedValue = random.choice([0, 127])

                    if element['type'] == 'list':
                        randomizedValue = random.choice(element['list'])

                    midiout.send_message([CONTROL_CHANGE, int(element['code']), int(randomizedValue)])
                    print(element["title"], ":", int(randomizedValue))
                input('\nPress enter to regenerate')
                print('\x1bc')
    except KeyboardInterrupt:
        print('')
    finally:
        print("Exit")
        midiout.close_port()
        del midiout
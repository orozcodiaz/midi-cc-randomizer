#!/usr/bin/env python3

# This script provide the functionality to generate random MIDI control messages based on the mapping file
# It allows you to randomly change parameters on the MIDI device and get the absolutely new sound every time
# You'll need MIDI output connected to your computer, MIDI cable and the hardware synthesizer

import rtmidi
import random
import json
import sys

from rtmidi.midiconstants import CONTROL_CHANGE

# Set it to True if you want to select a channel
use_channels = False#True

# Default preset value. From 0 to 15. Available amount of MIDI channels: 16
selected_channel = 0

# Clear screen
print('\x1bc')

# No input file? Show how to use
if len(sys.argv) == 1:
    print("Usage:",sys.argv[0],"mapping-file-name.json\n")
    exit()

# Assign path to mapping file from argument
mappingFile = sys.argv[1]

# Open MIDI handler
midiout = rtmidi.MidiOut()

# Get available output  ports
available_ports = midiout.get_ports()

if not available_ports:
    print("No MIDI outputs detected")
    exit()

# Show available output ports to user
print("Available output ports:")
for idx, val in enumerate(available_ports):
    print("MIDI output",idx,":", val)

# Show message to get the MIDI output port from CLI
selected_port = input("MIDI output to use: ")

# If user press "Enter" - use default port 0
if not selected_port:
    selected_port = 0

# If the setting set to use_channels=True, then let the user choose MIDI port
if use_channels:
    user_input_channel = input("Select MIDI channel to use (default is 1): ")
    if user_input_channel:
        if int(user_input_channel) > 16:
            print("Amount of available channels is 16")
            exit()
        else:
            selected_channel = int(user_input_channel) - 1

# Calculate CC channel
channel_to_use = CONTROL_CHANGE | (selected_channel & 0xF)

# Open MIDI output port
midiout.open_port(int(selected_port))

# Clear screen
print('\x1bc')

with midiout:
    try:
        with open(mappingFile) as mappingFileHandler:
            jsonObject = json.load(mappingFileHandler)

            while True:
                print('Selected output:', available_ports[int(selected_port)])
                print('Selected channel:', selected_channel + 1)
                print('Selected mapping:', mappingFile,'\n')

                # Go through JSON file and generate new values for MIDI out
                for element in jsonObject: 
                    if element['type'] == 'int':
                        randomizedValue = random.randrange(0, 127)

                    if element['type'] == 'bool':
                        randomizedValue = random.choice([0, 127])

                    if element['type'] == 'list':
                        randomizedValue = random.choice(element['list'])

                    # Send message to MIDI out
                    midiout.send_message([channel_to_use, int(element['code']), int(randomizedValue)])
                    print(element["title"], ":", int(randomizedValue))
                input('\nPress enter to regenerate')
                print('\x1bc')
    except KeyboardInterrupt:
        print('')
    finally:
        print("Exit")

        # Exit and close MIDI port
        midiout.close_port()
        del midiout
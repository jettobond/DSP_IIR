import sys

from pyfirmata2 import Arduino
from pyqtgraph.Qt import QtGui
import pickle

from qtdisplay import *

# Realtime oscilloscope at a sampling rate of 100Hz
# It displays analog channel 0.
# You can plot multiple chnannels just by instantiating
# more RealtimePlotWindow instances and registering
# callbacks from the other channels.
# Copyright (c) 2018-2020, Bernd Porr <mail@berndporr.me.uk>
# see LICENSE file.

PORT = Arduino.AUTODETECT
# PORT = '/dev/ttyUSB0'

# sampling rate: 100Hz
sampling_rate = 100

# Create an instance of an animated scrolling window
# To plot more channels just create more instances and add callback handlers below
qt_display = QtDisplay("Magnetic Force Sensor IIR Filter", sampling_rate)


# called for every new sample which has arrived from the Arduino
def callBack(data):
    # send the sample to the plotwindow
    # add any filtering here:
    # data = self.myfilter.dofilter(data)
    qt_display.addData(data)

# Get the Ardunio board.
board = Arduino(PORT)

# Set the sampling rate in the Arduino
board.samplingOn(1000 / sampling_rate)

# Register the callback which adds the data to the animated plot
board.analog[0].register_callback(callBack)

# Enable the callback
board.analog[0].enable_reporting()

# show the plot and start the animation
print("sampling rate: ", sampling_rate, "Hz")

# start display window
display_window = QtGui.QApplication(sys.argv)
display_window.exec_()

#save data episode for better design filter
output_file = open("./data/data_orignal_storage.dat", 'wb')
pickle.dump(qt_display.data_orign, output_file)
output_file.close()

# needs to be called to close the serial port
board.exit()


print("finished")
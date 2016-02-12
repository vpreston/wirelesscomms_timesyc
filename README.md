# Time Synchronization: BPSK and QPSK Demodulation
##### Project for Wireless Communications class at Olin College of Engineering

This repository is code written by Emily Tumang and Victoria Preston under the instruction of Siddhartan Govindasamy. This repo provides scripts to transmit, receive, and process wireless signals using gnuradio and python.

### Dependencies
This code will work with Python 2.7+ and Numpy 1.8+. Hardware tested with the transmission and reception using gnuradio were Ettus Research Universal Software Peripheral Radios (USRP1s). 

### Transmission
To transmit, you can execute the script in GRC Scripts > transmitter.py. This is a compiled script from gnuradio, which can be accessed in GRC Scripts > transmitter.grc. 

### Reception
To receive, simply execute the script GRC Scripts > receiver.py. This is a compiled script from gnuradio, which can be accessed in GRC Scripts > receiver.grc.

### Processing
To process a received signal, you can run python timesync.py on the command line. You will want to access the script directly in order to adjust constants, change signal file to read, etc.

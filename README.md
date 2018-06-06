# GRC Protocol Decoder
A simple way to decode a known protocol in GRC in real time.

# Usage - Protocol
Describe a protocol by grouping bits and converting them to an appropriate value.
Bits can be ignored, or optionally labelled. For example
`ignore.4 int.4` will convert the last 4 in a sequence to an integer, and the 
output will simply be, for example, `25`.
Groups can be labelled without affecting anything. For example, 
`ignore.4 label.deviceid int.4` will output: `deviceid:25`

`ignore.4` will ignore 4 bits

`label.sometext` will prepend the next value with `sometext:`

`bits.4` will just output the following 4 bits as they are

`int.8` will take the next 8 bits, convert them to an integer, and add them to the output

`hex.8` will take the next 8 bits, convert them to hex, and add them to the output

# Usage - Input Format
This will decode bits according to common transmission schemes. 

`%[bits]` will  parse bits as they were given

`%[man-bits]` will manchester-decode bits, converting 10's into 1s and 01's into 0s before converting values

`%[pwm-bits]` will PWM-decode bits, converting 110's into 1s and 100's into 0s before converting values

# Installation
make a directory called build, cd into it and run
```
cmake ..
make 
sudo make install
```


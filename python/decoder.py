#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# 
# Copyright 2018 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr
import pmt 

class decoder(gr.sync_block):
    protocol = ""
    inputformat = ""
    """
    docstring for block decoder
    """

    def manchesterDecode(self, string):
        result = ""
    
        while string != "":
            temp = string[:2]
            if temp == "10": result += "1"
            elif temp == "01": result += "0"
            else: result += "x"
            string = string[2:]
    
        return result

    def pwmDecode(self, string):
        result = ""

        while string != "":
            temp = string[:3]
            if temp == "110": result += "1"
            elif temp == "100": result += "0"
            else: result += "x"
            string = string[3:]

        return result


    def isInt(self, val):
        result = False
        try:
            i = int(val)
            result = True
        except:
            result = False
        return result

    def __init__(self, inputformat, protocol):
        gr.sync_block.__init__(self, name="decoder", in_sig=None, out_sig=None)

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

        self.protocol = protocol
        self.inputformat = inputformat

    def work(self, input_items, output_items):
        return 0

    def handle_msg(self, msg_pmt):
        try:
            msg = pmt.to_python(msg_pmt)
            message = ""
    
            if self.inputformat == "%[bits]":
                message = msg[1]
            elif self.inputformat == "%[man-bits]":
                message = self.manchesterDecode(msg[1])
            elif self.inputformat == "%[pwm-bits]":
                message = self.pwmDecode(msg[1])
            else:
                message = msg[1]
           
    
    
            output = ""
            pos = 0
            errors = []
            validated = False
    
            known_operators = ["label", "ignore", "int", "hex", "bin"]
            protocol_length = 0
            for item in self.protocol.split(" "):
                data = item.split(".")
                if data[0] not in known_operators: errors.append("unknown operator: {}".format(data[0]))
    
                if data[0] not in ["label"]:
                    if self.isInt(data[1]):
                        protocol_length += int(data[1])
                    else:
                        errors.append("invalid integer: {}".format(data[1]))
    
            if protocol_length > len(message):
                errors.append("specified protocol is longer than the message")
    
            if len(errors) != 0:
                print errors
            else:
                for item in self.protocol.split(" "):
                    data = item.split(".")
                    if data[0] == 'label':
                        output += data[1] + ":"
                    elif data[0] == "ignore":
                        pos += int(data[1])
                    elif data[0] in ["int", "hex", "bin"]:
                        temp = ""
                        for i in range(0, int(data[1])):
                            temp += message[pos]
                            pos += 1
    
                        if data[0] == "int":
                            output += "{} ".format(int(temp, 2))
                        elif data[0] == "hex":
                            output += "{} ".format(hex(int(temp, 2)))
                        elif data[0] == "bin":
                            output += "{} ".format(temp)
    
                print output
                
        except:
            print "error parsing message"        

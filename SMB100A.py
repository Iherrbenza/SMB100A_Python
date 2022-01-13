#!/usr/bin/env python. 
""" Module for  interfacing a Rohde&Schwarz SMB100A, RF&MW signal trought serial, Visa.
    The class can store a list of commands and send to the device  
"""
__author__ = 'Ivan Herrera Benzaquen'
# @Date:   2020-04-05T14:08:33+10:00
# @Last modified time: 2020-04-13T15:37:34+10:00

import time
import pyvisa


class Signal_Generator:

    def __init__(self, visa_addr='US?*::0x0AAD::0x0054::108563::INSTR'):
        
        rm = pyvisa.ResourceManager()
        if ( rm.list_resources(visa_addr)[0])== None:
            raise Exception("Rohde&Schwarz SMB100A instrument not connected") 
        self.SMB100A_addr = rm.list_resources(visa_addr)[0]
        print(self.SMB100A_addr)
        a = rm.open_resource(self.SMB100A_addr)
        a.close()
        self.timeout = 3000
        self.commands = []

        # Check the device is responding 
               
        try:
            with rm.open_resource(self.SMB100A_addr) as sg:
                sg.timeout = self.timeout 
                msg = sg.query('*IDN?')
            if ('SMB100A' not in msg):
                raise Exception("Device not responding correctly to identification \n\tIDN:%s"%msg)
        except pyvisa.VisaIOError:
            print("Instrument disconnected, check USB connection")
            time.sleep(0.5)
        print(msg)


    def send_commands(self):
        """function to send the list of command to the SMB100A"""
        rm = pyvisa.ResourceManager()
        try:
            with rm.open_resource(self.SMB100A_addr) as v:
                v.timeout = self.timeout
                for c in self.commands:
                    v.write(str(c))
                self.commands = []
        except pyvisa.VisaIOError:
            print("Instrument not responding, check USB connection")
        
    def RF_output(self, RFoutput):
        """ switch the RF output of the signal generator"""
        if RFoutput not in ['1','0','ON','OFF']:
            raise Exception("value must be one of (1, 0, ON, OFF)") 
        else:
            self.commands.append('OUTP %s'%RFoutput) 


    def RF_CW(self, freq, pw):
        """ sets the frequency output in CW, 
            freq: frequency in MHz
            pw: power out in dBm
        """
        self.commands.append('FREQ:MODE CW')
        self.commands.append('SOUR:POW:LEV:IMM:AMPL %.1f dBM'%pw)                
        self.commands.append('FREQ %.3f MHz'%freq)


    def RF_list(self, name_list = 'Labscriptlist', fqlist = [], pwlist= []):
        """Set the signal generator in list mode.
           writes a list of frequencies and powers and set the system
           to going through the list by an external trigger
            
            fqlist: list of frequency in MHz
            pwlist: list of powers in dBm
        """
        if len(fqlist) != len(pwlist):
            raise Exception("frequency and power lists have different lengths")
            msg = "ERROR"
        else:
            fq_list, pw_list = "",""
            for i, j in zip(fqlist, pwlist):
                fq_list = fq_list + " %.3f MHz,"%i
                pw_list = pw_list + " %.1f dBm,"%j
            
            self.commands.append('SOUR:LIST:SEL "%s"'%name_list)             
            self.commands.append('SOUR:LIST:FREQ %s'%fq_list[:-1])
            self.commands.append('SOUR:LIST:POW %s'%pw_list[:-1])
            self.commands.append('SOUR:LIST:DWEL 1ms')
            self.commands.append('SOUR:LIST:TRIG:SOUR EXT')
            self.commands.append('SOUR:LIST:MODE STEP')         
            self.commands.append('FREQ:MODE LIST')
         
        
    def RF_FM(self, state, mode , deviation):
        """ sets the frequency modulation of the output
            mode: selects different of noise, banwidth and deviation.
            deviaton: sets the deviation of the frequency signal in kHz (0.01 Hz steps)            
        """

        if state not in ['1','0','ON','OFF']:
            raise Exception("FM state must be one of (1, 0, ON, OFF)")
            
        if mode not in ['NORMAL','LNOISE','HDEViation']:
            raise Exception("FM mode must be one of ('NORMAL','LNOISE','HDEViation')")
        else:
            self.commands.append('FM:EXT:COUP DC')
            self.commands.append('FM:SOUR EXT')
            self.commands.append('FM:MODE %s'%mode)
            self.commands.append('FM %.3f kHz'%deviation)
            self.commands.append('FM:STAT %s'%state)

        


# Example of class use

## create an instance of the class(keyworarg not essential)
# SMB100A = Signal_Generator(visa_addr='USB?*::INSTR',timeout=3000)

# example of compile a list of commands for:
#              enable the FM with 100 kHz
#              write a list in the memory of the device
#              enable the output 
# SMB100A.FM_modulation('ON','NORMAL', 100)
# SMB100A.RF_list('list0',[78.48, 45, 69], [-1, 6, -12])
# SMB100A.RF_output('ON')

## print out of the list of commands stored
# SMB100A.commands

## clean the list of commands stored
# SMB100A.commands = []

# example of compile a list of commands for:
#              disable the FM 
#              set the output RF frequency 
#              enable the output 
# SMB100A.FM_modulation("OFF", 'NORMAL', 100)
# SMB100A.RF_CW(76.56, -1)
# SMB100A.RF_output('ON')

## write into the device of the list of commands stored
# SMB100A.send_commands()
# @Date:   2020-04-05T14:08:33+10:00
# @Last modified time: 2020-04-13T15:36:05+10:00


from __future__ import division, unicode_literals, print_function, absolute_import
from labscript_utils import PY2
if PY2:
    str = unicode
import h5py
import numpy as np
import pyvisa
from labscript import Device, LabscriptError, set_passed_properties

class SMB100A(Device):
    """A labscript_device for controlling a SMB100A RF&MW siggnal generator.
            
        Connection_table_properties:
            visa_addr: is the visa ddress of the device
            timeout: amout of time to wait before declare a timeout
    """
    description = 'SMB100A RF&MW signal generator'

    @set_passed_properties(
        property_names = {
            'connection_table_properties': ['visa_addr']}
    )
    def __init__(
        self, name, visa_addr , **kwargs):

        Device.__init__(self, name, None, visa_addr, **kwargs)
        self.name = name
        self.BLACS_connection = visa_addr
        self.timeout = 3000
        self.commands = []
      
      

    def send_commands(self):
        """function to send the list of command to the SMB100A"""
        rm = pyvisa.ResourceManager()
        try:
            with rm.open_resource(self.BLACS_connection) as v:
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
        self.commands.append('FREQ %.6f MHz'%freq)


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
                fq_list = fq_list + " %.6f MHz,"%i
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

    def generate_code(self, hdf5_file):
        dt = h5py.string_dtype()
        SMB100A_commands_list = np.array(self.commands, dtype= dt)
        group = self.init_device_group(hdf5_file)
        if self.commands:
            group.create_dataset("SMB100A_commands", data = SMB100A_commands_list)
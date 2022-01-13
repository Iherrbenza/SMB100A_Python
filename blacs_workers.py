# @Date:   2020-04-05T14:08:33+10:00
# @Last modified time: 2020-04-13T15:03:33+10:00
# __author__ = "Ivan Herrera Benzaquen"


from __future__ import division, unicode_literals, print_function, absolute_import
from labscript_utils import PY2
if PY2:
    str = unicode
from blacs.tab_base_classes import Worker
import labscript_utils.properties
import pyvisa



class SMB100AWorker(Worker):

    def init(self):
        """
        Initialise the worker
        Checks if the ESP32 is responding correctly
        """
        global h5py; import labscript_utils.h5_lock, h5py
        global Signal_Generator
        from .SMB100A import Signal_Generator
    
        self.SMB100A = Signal_Generator(self.visa_addr)
        self.timeout = 3000
        self.shot_file = None

        
    def transition_to_buffered(self, device_name, h5_file, panel_values, refresh):
        """Reading DDD commands in the shot file and send to the ESP32"""

        self.shot_file  = h5_file
        with h5py.File(self.shot_file, "r") as f:
            group = f["devices/%s"%self.device_name]
            if "SMB100A_commands" in group:
                SMB100A_commands_list = group["SMB100A_commands"][:]
            else:
                SMB100A_commands_list = None

        self.SMB100A.commands = SMB100A_commands_list
        self.SMB100A.send_commands()
        self.SMB100A.commands = []

        return {}

    def transition_to_manual(self):
        self.SMB100A.RF_FM('OFF', 'NORMAL', 100)
        self.SMB100A.RF_output(str(int(st)))
        self.SMB100A.RF_CW(fq,pw)
        self.SMB100A.send_commands()
        
        return True

    def program_manual(self, panel_values):
        global st, fq, pw
        st = panel_values['output']
        fq, pw =  panel_values['frequency'], panel_values['power']
        self.SMB100A.RF_output(str(int(st)))
        self.SMB100A.RF_CW(fq,pw)
        self.SMB100A.send_commands()
        
        return panel_values

    def abort(self):
        print('aborting!')
        return True

    def abort_buffered(self):
        print('abort_buffered: ...')
        return self.abort()

    def abort_transition_to_buffered(self):
        print('abort_transition_to_buffered: ...')
        self.shot_file = None
        return self.abort()

    def shutdown(self):
        return True

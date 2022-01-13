from __future__ import division, unicode_literals, print_function, absolute_import
from labscript_utils import PY2
if PY2:
    str = unicode
from blacs.device_base_class import DeviceTab

class SMB100ATab(DeviceTab):
    

    def initialise_GUI(self):

        RF = {
            "frequency": {
                "base_unit": "MHz",
                "min": 0.009,
                "max": 6E3,
                "step": 0.5,
                "decimals": 3,
            },
            "power": {
                "base_unit": "dBm",
                "min": -100,
                "max": 0,
                "step": 0.1,
                "decimals": 1,
            },
        }
        buttons = {}
        buttons['output'] = {}


        self.create_analog_outputs(RF)
        self.create_digital_outputs(buttons)   

        # Create widgets for output/input objects
        dds_widgets,ao_widgets,do_widgets = self.auto_create_widgets()

        # auto place the widgets in the UI
        self.auto_place_widgets(("CW RF", ao_widgets),("output", do_widgets))


    def initialise_workers(self):

        worker_initialisation_kwargs = self.connection_table.find_by_name(self.device_name).properties
        worker_initialisation_kwargs['visa_addr'] = self.BLACS_connection


        self.create_worker(
            'main_worker',
            'labscript_devices.SMB100A.blacs_workers.SMB100AWorker',
            worker_initialisation_kwargs,
        )
        self.primary_worker = 'main_worker'

        self.supports_remote_value_check(False)
        self.supports_smart_programming(False) 

# @Date:   2020-04-05T14:08:33+10:00
# @Last modified time: 2020-04-08T18:40:22+10:00

from labscript_devices import register_classes

register_classes(
    'SMB100A',
    BLACS_tab='labscript_devices.SMB100A.blacs_tabs.SMB100ATab',
    runviewer_parser=None
)

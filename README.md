# SMB100A_Python
Python scrip to interface a RF&MW generator, Rohde&amp Schwarz SMB100A, via serial (Visa).  
The class allows to control the intrument in different ways:  

Enable or disable the output.  

Set the frequency and power output in CW:  
* freq: frequency in MHz,   
* pw: power out in dBm.    

Set the signal generator in list modewrites a list of frequencies and powers and set the system to going through the list by an external trigger. 
* fqlist: list of frequency in MHz,  
* pwlist: list of powers in dBm.  

Set the frequency modulation of the output:   
* mode: selects different of noise, banwidth and deviation,
* deviaton: sets the deviation of the frequency signal in kHz (0.01 Hz steps)   

SMB100A contain the class to control the intrument via python.

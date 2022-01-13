# SMB100A_Python
Python script to interface a RF&MW generator, Rohde&amp Schwarz [SMB100A](https://www.rohde-schwarz.com/us/products/test-and-measurement/analog-signal-generators/rs-smb100a-microwave-signal-generator_63493-9379.html#:~:text=The%20compact%2C%20versatile%20R%26S%C2%AE,purity%20and%20high%20output%20power.&text=The%20R%26S%C2%AESMB100A%20is,analog%20microwave%20signal%20is%20needed.), via serial (Visa).  
As well files to integrate with [Labscript](https://github.com/labscript-suite)
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

SMB100A.py contain the class to control the intrument via python.
Rest of the files are for integration with [Labscript](https://github.com/labscript-suite) envioroment.

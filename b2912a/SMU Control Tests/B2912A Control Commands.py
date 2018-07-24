import visa
import numpy as np
from matplotlib import pyplot as plt
import time

# [:SOURce]:DIGital:EXTernal:TOUTput[:EDGE]:POSi tion
# :TRIGger<:ACQuire|:TRANsient|[:ALL]>:SOURce[:SI GNal]

rm = visa.ResourceManager()
print(rm.list_resources())
inst  = rm.open_resource(rm.list_resources()[0])

print(inst.query('*IDN?'))

NPLC = 1
Npoints = 100
voltageStart = 0.1
voltageStop = 0.1
complianceCurrent = 100e-6
measurements = 2

inst.write("*RST") # Reset

inst.write(':system:lfrequency 60')
print(inst.query(':system:lfrequency?'))


inst.write(':source:digital:ext2:function tout')
inst.write(':source:digital:ext2:polarity neg')
inst.write(':source:digital:ext2:toutput:type level')
inst.write(':source:digital:ext2:toutput:width 0.01')

inst.write(':trigger:acq:toutput:signal ext2')
inst.write(':trigger:acq:count 1')
inst.write(':trigger:acq:toutput:state on')

inst.write(':source:digital:ext3:function tinp')
inst.write(':source:digital:ext3:polarity pos')
# inst.write(':source:digital:ext3:toutput:type level')
inst.write(':source:digital:ext3:toutput:type edge')
inst.write(':source:digital:ext3:toutput:width 0.01')


inst.write(':trigger:acq:source:signal ext3')





# inst.write(':source:digital:ext4:function tout')
# inst.write(':source:digital:ext4:polarity neg')
# inst.write(':source:digital:ext4:toutput:type level')
# inst.write(':source:digital:ext4:toutput:width 0.01')


# inst.write(':arm:acq:toutput:signal ext4')
inst.write(':arm:acq:count inf')
# inst.write(':arm:acq:toutput:state on')

# inst.write(':source:digital:ext5:function tinp')
# inst.write(':source:digital:ext5:polarity neg')
# # inst.write(':source:digital:ext5:toutput:type level')
# # inst.write(':source:digital:ext5:toutput:width 0.01')


# inst.write(':arm:acq:source:signal ext5')

# inst.write(':init:immediate:acq')
inst.write(':init')


exit()


for i in range(measurements):
	# Set voltage output from 0 V to 0.1 V, 5 steps
	inst.write(":source:function:mode voltage")
	inst.write(":source:voltage:mode sweep")
	inst.write(":source:voltage:start {}".format(voltageStart))
	inst.write(":source:voltage:stop {}".format(voltageStop)) 
	inst.write(":source:voltage:points {}".format(Npoints))
	# Set auto-range current measurement
	inst.write(":sense:function \"curr\"")
	inst.write(":sense:curr:nplc {}".format(NPLC))
	inst.write(":sense:curr:prot {}".format(complianceCurrent))
	
	# Generate 5 triggers by automatic internal algorithm 
	inst.write(":trig:source aint")
	inst.write(":trig:count {}".format(Npoints))

	# Turn on output switch
	inst.write(":output on")
	# Initiate transition and acquire
	inst.write(":init (@1)")
	time.sleep(Npoints*NPLC/60)

	# inst.write("trace:stat:form sdeviation")
	# inst.write("trace:stat:form mean")
	print(inst.query(":sense:current:protection:tripped?"))

	# "source:digital:data {}".format(0b10111010111011)

	# Retrieve measurement result
	currents = inst.query_ascii_values(":fetch:arr:curr? (@1)")
	voltages = inst.query_ascii_values(":fetch:arr:voltage? (@1)")
	resistances = inst.query_ascii_values("fetch:arr:resistance? (@1)")
	times = inst.query_ascii_values(":fetch:arr:time?")

	# statData = inst.query_ascii_values(":trace:stat:data?") # Instrument says "Error +862,Trace; No trace data; Channel1"

	# use :read:arr:curr? instead of :init followed by :fetch:arr:curr?

	print(voltages)
	print(currents)
	print(resistances)
	print(times)
	# print(statData)

	plt.plot(times, currents, '.-')

	plt.title('NPLC = {}'.format(NPLC))
	plt.xlabel('Time (s)')
	plt.ylabel('Current (A)')
	plt.savefig('/Users/stevennoyce/Desktop/B2912A.png', dpi=300)
	
	print('Measurement {} of {} complete!'.format(i+1, measurements))
	time.sleep(1)
	print('Next measurement...')

plt.show()



exit()










inst.write(':SOUR:FUNC:MODE VOLT')
inst.write(':SENS:CURR:PROT 100e-6')

inst.query_ascii_values(':MEAS?')


inst.write(':SOUR:SWE:STA DOUB')

inst.write(':SOUR:VOLT:MODE SWE') 
inst.write(':SOUR:VOLT:STAR 0') # Start 0 V 
inst.write(':SOUR:VOLT:STOP 1') # Stop 1 V 
inst.write(':SOUR:VOLT:POIN 11') # 11 points

inst.write(':SOUR:SWE:RANG AUTO')


inst.write(':TRIG:SOUR TIM') 
inst.write(':TRIG:TIM 4E-3') # Interval 4 ms
inst.write(':TRIG:COUN 11') # 11 points
inst.write(':TRIG:TRAN:DEL 1E-3') # Source delay 1 ms

inst.query_ascii_values(':FETC:CURR?')



# Set the staircase sweep source and the required source functions. For details, see “Controlling the Source Output” on page 1-10.


# Set the required measurement functions. For details, see previous topics in this section.


# Set the trigger condition. See “Setting the Source Output Trigger” on page 1-15 and “Setting the Measurement Trigger” on page 1-20.


# Enable the channel. See “Enabling the Measurement Channel” on page 1-18. The channel starts output set by the :SOUR:<CURR|VOLT> command.


# Execute the :INIT command to start measurement.


# Get Measurement Data with a :FETC command


# Stop the measurement by stopping the output
inst.write(':OUTP OFF')



inst.write(':TRAC:CLE') # Clear the trace buffer
inst.write(':TRAC:POIN 1000') # Set the trace buffer size
inst.write(':TRAC:FEED SENS') # Specify data to feed
inst.write(':TRAC:FEED:CONT NEXT') # Enable the write buffer
inst.write(':TRAC:TST:FORM DELT') # Specify delta time stamps instead of absolute (ABS)

inst.write(':TRAC:DATA?') # Read all trace data

inst.write(':TRAC:STAT:FORM MEAN') # 
inst.write(':TRAC:STAT:DATA?') # 

inst.write(':TRAC:STAT:FORM SDEV') # 
inst.write(':TRAC:STAT:DATA?') # 

inst.write(':TRAC:STAT:DATA?') # 


# *RST
# SOUR:FUNC:MODE:VOLT (@1:2)
# SOUR:VOLT:RANG:AUTO ON (@1:2)
# SOUR1:VOLT 1.0
# SOUR2:VOLT 1.5


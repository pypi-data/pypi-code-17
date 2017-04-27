#import LVPM 
#import HVPM
#import sampleEngine
#import Operations as op
import LVPM
import sampleEngine
import Operations as op


Mon = LVPM.Monsoon()
Mon.setup_usb()
Mon.setVout(4.0)
#Take measurements from the Main channel
engine = sampleEngine.SampleEngine(Mon)
engine.enableCSVOutput("Main Test.csv")
engine.ConsoleOutput(True)
engine.startSampling(10000)
engine.disableChannel(sampleEngine.channels.MainCurrent)
engine.disableChannel(sampleEngine.channels.MainVoltage)

#Take measurements from the USB Channel
Mon.setVout(0)
Mon.setUSBPassthroughMode(op.USB_Passthrough.On)
engine.enableChannel(sampleEngine.channels.USBCurrent)
engine.enableChannel(sampleEngine.channels.USBVoltage)
engine.enableCSVOutput("USB Test.csv")
engine.startSampling(5000)

#Enable every channel, take measurements
engine.enableChannel(sampleEngine.channels.MainVoltage)
engine.enableChannel(sampleEngine.channels.MainCurrent)
engine.enableChannel(sampleEngine.channels.AuxCurrent)
Mon.setVout(2.5)
engine.ConsoleOutput(False)
engine.enableCSVOutput("All Test.csv")
engine.startSampling(5000)

#Enable every channel, take measurements, and retrieve them as a Python list.
engine.disableCSVOutput()
engine.startSampling(5000)
samples = engine.getSamples()
#Samples are stored in order, indexed sampleEngine.channels values
for row in samples[sampleEngine.channels.MainCurrent]:
    print(row)






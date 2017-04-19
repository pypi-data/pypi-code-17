# expose main methods
from tymed import tymedmain

tymed = tymedmain.tymed
tymedCls = tymedmain.tymedCls

lastTyme = tymedmain.lastTyme
allTyme = tymedmain.allTyme
resetTyme = tymedmain.resetTyme
lap = tymedmain.lap

FunctionNotTymedException = tymedmain.FunctionNotTymedException
BoundMethodNotInTymedClassException = tymedmain.BoundMethodNotInTymedClassException
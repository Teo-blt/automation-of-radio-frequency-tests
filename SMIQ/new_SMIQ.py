from SMIQ_helper import PrologixInstrument as ScpiInstrumentWrapper

myPrologicInst = ScpiInstrumentWrapper('COM18', 'GPIB25')
print(myPrologicInst.query('*IDN?'))
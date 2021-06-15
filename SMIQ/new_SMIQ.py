import pyvisa as visa

gpib_port = "18"
rm = visa.ResourceManager()
gpib = rm.open_resource('PROLOGIX::COM18')
gpib.write("++addr 25\n") # if GPIB device's number is 25
gpib.write("++auto 0\n") # if you want to make the device "listen" (i.e. accept commands); use value 1 instead to make it "talk" (i.e. request a read automatically after write)
gpib.write("++eoi 1\n") # Check docs for details
gpib.write("++eos 3\n") # Check docs for line ending behaviour
# ++eot_enable and ++eot_char allow automatic adding of line ending characters on write
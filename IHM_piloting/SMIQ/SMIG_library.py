################################################################################################
# TEST: Unwanted emission in the spurious domain
# EN 300 220-1 v3.1.1
################################################################################################
################################################################################################
# Board: TSL-4 V2C
# 29/06/2020
# File status: OK
################################################################################################

import visa
import serial
import os
import time
import sys

sys.path.append('P:\\e2b\\hardware\\Scripts_auto\\Python\\lib')
# from tools_SMIQ import *

################################################
# VISA instrument
rm = visa.ResourceManager()
SMIQ_SEND = rm.open_resource('GPIB0::29::INSTR')
SMIQ_SEND.write('*RST')
print(SMIQ_SEND.query('*IDN?'))

# General Setting
SMIQ_SEND.write('OUTP:STAT OFF')  # RF Output OFF
# SMIQ_SEND.write('SOUR:MOD OFF')

# TODO: Check List presence and create it if absent
# SMIQ_SEND.query('SOUR:DM:DLIS:CAT?')

# Command order should not be modified
SMIQ_SEND.write('SOUR:DM:STAT ON')  # Digital Modulation ON
SMIQ_SEND.write('SOUR:DM:SOUR DLIST')  # Source selection
SMIQ_SEND.write("SOUR:DM:DLIST:SEL 'T1_TEST'")  # 169_N2
SMIQ_SEND.write('SOUR:DM:SEQ SINGLE')  # AUTO | RETRigger | AAUTo | ARETrigger | SINGle
# Rectangle filter mandatory for WM4800 !
SMIQ_SEND.write('SOUR:DM:FILT:TYPE RECT')
# SCOSine | COSine | GAUSs | LGAuss | BESS1 | BESS2 | IS95 | EIS95 | APCO | TETRa | WCDMa | RECTangle | SPHase | USER

################################################
# Devices
serial_speed = 115200
serial_timeout = 5
DUT = serial.Serial('COM13', serial_speed, timeout=serial_timeout)

################################################
# Measurement SETTINGS
################################################
nb_frame = 50  # Number of sent frames
wait_measure = 1  # Delay between measurement (s)
coupler_atten_send_to_EUT = 0

channel_list = [  # List of Measurement channel (Hz), channel number
    868950000
]

mod_list = [  # Modulation, BW or Dev, SF or Bitrate, OBW, Sensitivity_level
    ['G', 45000, 100000, 250000, -110],  # Real sensitivity = -121 / Theoretical sensitivity = -109 (7kHz RxBW)
    # ['L',7.8,341,12500, -137] #Real sensitivity = -137 / Theoretical sensitivity = -108 (7.8kHz RxBW)
]

str_received_address_check = "CEN-785634120107"
str_received_payload_check = "PAYLOAD (19) = \n\rb4 f0 e1 d2 c3 b4 a5 96 87 78 69 5a 4b 3c 2d 1e \n\r0f 55 ff"
rssi = []
rssi_average = -999

# Result folder
result_path = os.path.dirname(__file__)
result_path += '\\Sensi'

################################################################################################
# MEASUREMENT Loop
################################################################################################
print("\n################################################\n")
print("\nStart of Test\n")
time_start = time.time()
for mod in mod_list:
    modulation = mod[0].encode('utf-8')
    freq_dev = mod[1]
    bitrate = mod[2]
    OCW = mod[3]
    sensitivity_level = mod[4]

    seq_time = time.localtime()
    filename = result_path + f'\Sensi_60deg_{mod[0]}{bitrate}_{seq_time.tm_year}-' \
                             f'{seq_time.tm_mon:02d}-{seq_time.tm_mday:02d}-' \
                             f'{seq_time.tm_hour:02d}{seq_time.tm_min:02d}.csv'

    csv_result = open(filename, 'w')
    csv_result.write("Sensitivity measurement\n")
    csv_result.write("EN300 220-1 v3.1.1\n")
    csv_result.write("Time; Channel frequency; Signal Level; Nb frame sent; PER\n")

    for freq in channel_list:

        # Configure sending device modulation
        SMIQ_SEND.write('SOUR:DM:FORM FSK2')  # FSK2 / GFSK
        SMIQ_SEND.write('SOUR:DM:SRATe %d Hz' % bitrate)  # symbol rate 1kHz to 7 MHz / Set rate BEFORE deviation
        SMIQ_SEND.write('SOUR:DM:FSK:DEV %d' % freq_dev)  # frequency deviation 100 Hz to 2.5 MHz
        SMIQ_SEND.write('SOUR:FREQ:MODE CW')  # Set mode to fixed frequency
        SMIQ_SEND.write('SOUR:FREQ:CW %d' % freq)  # Set channel frequency
        # SMIQ_SEND.write('SOUR:DM:FILT:TYPE RECTangle')
        # SCOSine | COSine | GAUSs | LGAuss | BESS1 | BESS2 | IS95 |
        # EIS95 | APCO | TETRa | WCDMa | RECTangle | SPHase | USER

        SMIQ_SEND.write('SOUR:FREQ:MODE CW')  # Set mode to fixed frequency
        SMIQ_SEND.write('OUTP:STAT ON')  # RF Output ON

        SMIQ_SEND.write('SOUR:POW:MODE FIX')  # Set power to "Fixed" mode

        sensitivity_steps = list(range(sensitivity_level - 4, sensitivity_level + 11, 1))
        sensitivity_steps = sensitivity_steps + list(range(sensitivity_level + 11, sensitivity_level + 21, 2))
        sensitivity_steps = sensitivity_steps + list(
            range(round((sensitivity_level + 26) / 10) * 10, 0, 10))  # Round to the upper decade
        print(f'\nPower levels steps calculated: {sensitivity_steps}')

        for signal_level in sensitivity_steps:

            SMIQ_SEND.write('POW %d' % (
                    signal_level + coupler_atten_send_to_EUT))
            # Set output power level at Theoretical sensitivity + 3dB

            # Set product in reception
            # DUT.write(b"\n")
            # DUT.write(b"startrx %d %d \n" % (mode, channel_number))
            # time.sleep(1)

            nb_frame_sent = 0
            nb_frame_received = 0
            print(f'\nSending {nb_frame} frames at {signal_level}dBm...')
            for i in range(0, nb_frame):

                # Send 1 frame
                print(f'\n\n==========\nSending frame {i + 1}/{nb_frame}...')
                SMIQ_SEND.write('TRIG:DM:IMM')  # Send 1 trigger event
                nb_frame_sent = nb_frame_sent + 1
                time.sleep(1)
                # Check frame reception
                received_frame = DUT.read_all().decode('utf-8')

                # ToDo Add RSSI recording

                print(received_frame)
                if str_received_address_check in received_frame:
                    print(f'Frame {i + 1}/{nb_frame} received !')
                    nb_frame_received = nb_frame_received + 1
                    rssi.append(int(received_frame[received_frame.find('RSSI') + 5:received_frame.find(',')]))

            if nb_frame_received > 0:
                rssi_average = sum(rssi) / len(rssi)

            time.sleep(1)
            print(DUT.read_all().decode('utf-8'))

            PER = (nb_frame_sent - nb_frame_received) / nb_frame_sent
            print(f'\nFrame sent = {nb_frame_sent}')
            print(f'\nPER = {PER}')

            # Time; Channel frequency; Signal Level; Nb frame sent; PER ; RSSI
            res_str = f'{time.asctime()}; {freq}; {signal_level}; {nb_frame_sent}; {PER * 100}%; {rssi_average}\n'
            print(res_str)
            csv_result.write(res_str)

            time.sleep(wait_measure)

    csv_result.close()

time_stop = time.time()
print("\n################################################\n")
print("\nEnd of Test\n")
print(f'Test duration: {time_stop - time_start}\n')
DUT.close()

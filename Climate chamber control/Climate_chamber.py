################################################################################################
## Climatic chamber control
## 29/06/2020
## File status: OK
################################################################################################

################################################
##### Cycle SETTINGS
################################################


# import visa
import serial  # requirment pyserial
import os
import time
import sys


def init(temp_min):
    try:
        # sys.path.append('\\\\samba\\share\\projet\\e2b\\hardware\\Scripts_auto\\Python\\lib')

        ################################################
        ##### VISA instrument
        serial_speed = 9600
        serial_timeout = 5
        VT = serial.Serial('COM11', serial_speed, timeout=serial_timeout)

        ################################################################################################
        ## MEASUREMENT Loop
        ################################################################################################
        print("\n################################################\n")
        print("\nStart of Test\n")
        time_start = time.time()

        # ToDo : Display cycles carac

        temp_min_duration_h = 1

        temp_max = 20
        temp_max_duration_h = 1

        change_min_duration_h = 1

        nb_cycle = 20

        for i in range(0, nb_cycle):
            VT.write(b"$00I\n\r")
            time.sleep(0.5)
            received_frame = VT.read_all().decode('utf-8')
            print(received_frame)
            print("\n")
            # ToDo print actual temp
            # ToDo Start Log

            print(f'Start cycle {i} low temp:\n')

            # Set Temp Min
            VT.write(b"$00E %06.1f 0000.0 0000.0 0000.0 0000.0 0101000000000000\n\r" % temp_min)
            time.sleep(2)

            # Wait temperature stabilisation
            change_cycle_start_time = time.time()
            while time.time() <= change_cycle_start_time + change_min_duration_h * 3600:
                # Read temp every 5 min
                VT.write(b"$00I\n\r")
                received_frame = VT.read_all().decode('utf-8')
                print(received_frame)
                print("\n")
                time.sleep(5 * 60)

            low_cycle_start_time = time.time()
            while time.time() < low_cycle_start_time + (temp_min_duration_h * 3600):
                # Read temp every 5 min
                VT.write(b"$00I\n\r")
                received_frame = VT.read_all().decode('utf-8')
                print(received_frame)
                print("\n")
                time.sleep(5 * 60)

            print(f'Start cycle {i} High temp:\n')
            # Set Temp Max
            VT.write(b"$00E %06.1f 0000.0 0000.0 0000.0 0000.0 0101000000000000\n\r" % temp_max)
            time.sleep(2)

            change_cycle_start_time = time.time()
            while time.time() < change_cycle_start_time + (change_min_duration_h * 3600):
                # Read temp every 5 min
                VT.write(b"$00I\n\r")
                received_frame = VT.read_all().decode('utf-8')
                print(received_frame)
                print("\n")
                time.sleep(5 * 60)

            high_cycle_start_time = time.time()
            while time.time() < high_cycle_start_time + (temp_max_duration_h * 3600):
                # Read temp every 5 min
                VT.write(b"$00I\n\r")
                received_frame = VT.read_all().decode('utf-8')
                print(received_frame)
                print("\n")
                time.sleep(5 * 60)

            print(f'End of cycle {i}: {time.time() - time_start}\n')

        # Stop climatic chamber
        VT.write(b"$00E 0020.0 0000.0 0000.0 0000.0 0000.0 0000000000000000\n\r")

        time_stop = time.time()
        print("\n################################################\n")
        print("\nEnd of Test\n")
        print(f'Test duration: {time_stop - time_start}\n')
        VT.close()

        """# Votsch climatic chamber VT4002
        
        # Set temperature +80 & mise à ON
        $00E 0080.0 0000.0 0000.0 0000.0 0000.0 0101000000000000
        
        # Set temperature -40 & mise à ON
        $00E -040.0 0000.0 0000.0 0000.0 0000.0 0101000000000000
        $00E -040.0 0000.0 0000.0 0000.0 0000.0 0101000000000000
        
        # Off
        $00E 0020.0 0000.0 0000.0 0000.0 0000.0 0000000000000000
        
        
        
        # Ask temperature & ref
        $00I
        
        
        > Answer
        0085.0 -039.9 0000.0 -000.1 0000.0 -190.3 0000.0 -190.3 0000.0 -190.3 0101000000000000
        """
    except:
        print("error")

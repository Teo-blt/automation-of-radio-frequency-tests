################################################################################################
# Climatic chamber control
# 29/06/2020
# File status: OK
################################################################################################

################################################
# Cycle SETTINGS
################################################


# import visa
import serial  # requirment pyserial
import time
import threading

CLIMATIC_CHAMBER_STOP = b"$00E 0020.0 0000.0 0000.0 0000.0 0000.0 0000000000000000\n\r"
SET_TEMP_MIN = b"$00E %06.1f 0000.0 0000.0 0000.0 0000.0 0101000000000000\n\r"
SET_TEMP_MAX = b"$00E %06.1f 0000.0 0000.0 0000.0 0000.0 0101000000000000\n\r"


class Mythread(threading.Thread):
    def __init__(self, temp_min, temp_max, temp_min_duration_h,
                 temp_max_duration_h, change_min_duration_h, nb_cycle, oof):  # data = additional data
        threading.Thread.__init__(self)  # do not forget this line ! (call to the constructor of the parent class)
        self.temp_min = temp_min  # additional data added to the class
        self.temp_max = temp_max
        self.temp_min_duration_h = temp_min_duration_h
        self.temp_max_duration_h = temp_max_duration_h
        self.change_min_duration_h = change_min_duration_h
        self.nb_cycle = nb_cycle
        self.oof = oof

    def run(self):
        try:
            # sys.path.append('\\\\samba\\share\\projet\\e2b\\hardware\\Scripts_auto\\Python\\lib')
            print(self.temp_min)
            print(self.temp_max)
            print(self.temp_min_duration_h)
            print(self.temp_max_duration_h)
            print(self.change_min_duration_h)
            print(self.nb_cycle)
            print(self.oof)

            ################################################
            # VISA instrument
            serial_speed = 9600
            serial_timeout = 5
            vt = serial.Serial('COM11', serial_speed, timeout=serial_timeout)

            ################################################################################################
            # MEASUREMENT Loop
            ################################################################################################

            print("\n################################################\n")
            print("\nStart of Test\n")
            time_start = time.time()

            # ToDo : Display cycles carac

            if self.oof:
                vt.write(CLIMATIC_CHAMBER_STOP)
                quit(code=self.run)

            for i in range(0, self.nb_cycle):
                vt.write(b"$00I\n\r")
                time.sleep(0.5)
                received_frame = vt.read_all().decode('utf-8')
                print(received_frame)
                print("\n")
                # ToDo print actual temp
                # ToDo Start Log

                print(f'Start cycle {i} low temp:\n')

                # Set Temp Min
                vt.write(SET_TEMP_MIN % self.temp_min)
                time.sleep(2)

                # Wait temperature stabilisation
                change_cycle_start_time = time.time()
                while time.time() <= change_cycle_start_time + self.change_min_duration_h * 3600:
                    # Read temp every min
                    vt.write(b"$00I\n\r")
                    received_frame = vt.read_all().decode('utf-8')
                    print(received_frame)
                    print("\n")
                    time.sleep(60)

                low_cycle_start_time = time.time()
                while time.time() < low_cycle_start_time + (self.temp_min_duration_h * 3600):
                    # Read temp every min
                    vt.write(b"$00I\n\r")
                    received_frame = vt.read_all().decode('utf-8')
                    print(received_frame)
                    print("\n")
                    time.sleep(60)

                print(f'Start cycle {i} High temp:\n')
                # Set Temp Max
                vt.write(SET_TEMP_MAX % self.temp_max)
                time.sleep(2)

                change_cycle_start_time = time.time()
                while time.time() < change_cycle_start_time + (self.change_min_duration_h * 3600):
                    # Read temp every 5 min
                    vt.write(b"$00I\n\r")
                    received_frame = vt.read_all().decode('utf-8')
                    print(received_frame)
                    print("\n")
                    time.sleep(5 * 60)

                high_cycle_start_time = time.time()
                while time.time() < high_cycle_start_time + (self.temp_max_duration_h * 3600):
                    # Read temp every 5 min
                    vt.write(b"$00I\n\r")
                    received_frame = vt.read_all().decode('utf-8')
                    print(received_frame)
                    print("\n")
                    time.sleep(5 * 60)

                print(f'End of cycle {i}: {time.time() - time_start}\n')

            # Stop climatic chamber
            vt.write(CLIMATIC_CHAMBER_STOP)

            time_stop = time.time()
            print("\n################################################\n")
            print("\nEnd of Test\n")
            print(f'Test duration: {time_stop - time_start}\n')
            vt.close()
        except:
            print("error")


def read():
    serial_speed = 9600
    serial_timeout = 5
    vt = serial.Serial('COM11', serial_speed, timeout=serial_timeout)
    vt.write(b"$00I\n\r")
    time.sleep(0.5)
    received_frame = vt.read_all().decode('utf-8')
    print(received_frame)
    print("\n")


"""
for i in range(0, 10):
    print("programme ", i)
    time.sleep(0.2)  # wait 100 milliseconds without doing anything,  makes the display easier to read

# Votsch climatic chamber VT4002
        
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

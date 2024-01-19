# rough draft of main
# first project using MicroPython
# CC0-1.0 license for Olzeke51, /lib has their own
from machine import *  # Pin, I2C, ADC, RTC
from utime import sleep
from DHT20 import DHT20

rtc = RTC()

button = Pin(18, Pin.IN, Pin.PULL_UP)# button connect to D18
button.irq(lambda pin: InterruptsButton(),Pin.IRQ_FALLING)#Set key interrupt

i2c0_sda = Pin(8)
i2c0_scl = Pin(9)
i2c0 = I2C(0, sda=i2c0_sda, scl=i2c0_scl)
dht20 = DHT20(0x38, i2c0)

led = Pin(25, Pin.OUT) #led was to D16;, D25 for the Udoo.key
relay_1 = Pin(20, Pin.OUT)
dbg_flg = 0

'''Key interrupt function, change the state of the light when the key is pressed'''
def InterruptsButton(): #button input
    global dbg_flg
    dbg_flg = ~dbg_flg
    led.value(dbg_flg)
    # relay.value(tmp)
    print(dbg_flg)
    if dbg_flg != 0:
        print("Debugg is enabled")
    else:
        print("Debugg is disabled")


# device routines * * * * * * * * * * * * * * * * * * 

def debugg(cmd_data):
	print("Debugg is " + cmd_data)

def light(cmd_data):
    # print("CMD-light is " + cmd_data)
    light = ADC(0)
    lightVal = light.read_u16() - 400
    print('lightvalue= ',str(lightVal))
    sleep(1)
    if (dbg_flg):
        print("debug light is: " + str(lightVal))

def azimuth(cmd_data):
	print("azimuth is " + cmd_data)


def relay1(cmd_data):
    if (dbg_flg):
        print("debug relay_1 is: ")
        print((cmd_data))
    elif cmd_data[0] == '0':
        relay_1.low()
    elif cmd_data[0] == '1':
        relay_1.high()
    else:
        print("bad relay_1 CMD")
        print((cmd_data))


def relay2(cmd_data):
	print("relay2 is " + cmd_data)


def relay3(cmd_data):
	print("relay3 is " + cmd_data)


def clock(cmd_data):
    rtc_end = len(cmd_data)
    if dbg_flg != 0:
        print("clock is " + cmd_data)
        print("this is debugg info")
        #
    else:
        if cmd_data[0] == 'S':	# SET the time>
            my_time = cmd_data[3:(rtc_end)]
            put_time = tuple(map(int, my_time.split(', ')))
            rtc.datetime(put_time)
            print((rtc.datetime())) # until I get the 
        elif cmd_data[0] == 'I':	#send out time INFO
            print((rtc.datetime())) # until I get the ESP serial
            print("Solar start time this week is :")	# need data
        elif cmd_data[0] == 'W':	#set solar start time; this week
            print("this week's solar start time for AZ setting")
        elif cmd_data[0] == 'N':	#set solar start time; next week
            print("NEXT week's solar start time for AZ setting")
        else:
            print("RTC-oops - wrong CMD", (cmd_data))
            # print(cmd_data)
	


def temp_h(cmd_data):
    print("temp_h is " + cmd_data)

    measurements = dht20.measurements
    temp_rounded = round(measurements['t'], 1)
    humidity_rounded = round(measurements['rh'], 1)
    faren = (temp_rounded * 9 / 5) + 32

    print(f"Temperature: {faren} °F, humidity: {humidity_rounded} %RH")

def power(cmd_data):
    print("power is " + cmd_data)


def battry(cmd_data):		# misspelled in honor of a nice guy
	print("battry is " + cmd_data)

# ************************ MAIN**********
# menu selection of functions - raw 01/04/24 grz
Device = ""
CMD = ""
dbg_flg = 0
cmd_data = bytes(48)
Incoming = bytes(48)
Incoming = "XR0"	#testing purposes
# Incoming  is string  !! assumed 0-based !!
# would normally come in UARTx from ESP via ESP-now
to_end = len(Incoming)
sleep(5)	# allows time to set debugg on power up/testing
# ****** CMD - & data parsing
if to_end > 1:  # Incoming != b'\n':    #None:
	if Incoming[0] == 'I':	# Info status request
		CMD = 'I'
		# Device = Incoming[1]
		cmd_data = Incoming[2:to_end]
	elif Incoming[0] == 'X':	# eXecute a CMD
		CMD = 'X'
		# Device = Incoming[1]
		cmd_data = Incoming[2:to_end]
	else:
		print("incorrect CMD/device! :", (Incoming))
		# what about Z - reset of Pico? done in ESP?

# ******DEVICE SELECTION  ********
# cmd_data has removed the first 2 chars of Incoming
# and is now just the 'data/info' part!!!
Device = Incoming[1]
if Device != b'\n':    #None:
	if Device == 'L':	# light value
		light(cmd_data)
	elif Device == 'A':	# azimuth set&report
		azimuth(cmd_data)
	elif Device == 'R':	# relay1
		relay1(cmd_data)
	elif Device == 'P':	# relay2
		relay2(cmd_data)
	elif Device == 'Q':	# relay3
		relay3(cmd_data)
	elif Device == 'C':	# Clock
		clock(cmd_data)
	elif Device == 'T':	# temperature
		temp_h(cmd_data)
	elif Device == 'S':	# Solar
		power(cmd_data)
	elif Device == 'D':	# Debug
		debugg(cmd_data)
	elif Device == 'B':	# power status
        # battry misspelled in honor of a kindly soul
		battry(cmd_data)
	else:
		print("incorrect device!\n")




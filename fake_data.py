#!/usr/bin/env python

import sys, random, string, struct, time, tempfile

""" Generate id """
def id_gen (size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.sample(chars, size))

""" Get date in YYYYMMDDHHMMSS format (14B) """
def get_date():
    return time.strftime("%Y%m%d%H%M%S")



"""
Sensor Data Packet format

06B: MessageID ($PSENS)
06B: DeviceID (unique alphanumeric ID)
15B: IMEI of GSM module
06B: ATM ID
20B: NMR (Network Code, Location Code, Cell ID, Receive Signal Strength, CSQ)
14B: Date/Time received from Mobile tower (YYYYMMDDHHMMSS)
03B: Temperature in Centigrade
10B: RFID Reader data
02B: Digital input
02B: Digital output
03B: Smoke detector output
03B: Vibration sensor output
03B: UPS battery voltage
03B: UPS battery current
02B: Analogue input
04B: RFU (Reserved for future use)
"""

class SensorReading:
    def __init__ (self, atm):
        self.msgid = '$PSENS'
        self.atm = atm
        self.nmr = id_gen(20)
        self.date = get_date()
        self.temp = self.get_temperature()
        self.rfid = self.get_rfid()
        self.din = self.get_digital_input()
        self.dout = self.get_digital_output()
        self.smoke = self.get_smoke_reading()
        self.vibration = self.get_vibration_reading()
        self.voltage = self.get_battery_voltage()
        self.current = self.get_battery_current()
        self.analogue = self.get_analogue_input()
        self.rfu = "RFUU"


    """ Get random temperature in sensible range (3B) """
    def get_temperature(self):
        return random.randint(5, 45)

    """ Get random string for RFID data (10B) """
    def get_rfid(self):
        return "RFID" + id_gen()

    """ Get digital input (2B) """
    def get_digital_input(self):
        return random.choice([ "AA", "BB", "CC", "DD", "EE", "FF" ])

    """ Get digital output (2B) """
    def get_digital_output(self):
        return random.choice([ "AA", "BB", "CC", "DD", "EE", "FF" ])

    """ Get smoke detector reading (3B) """
    def get_smoke_reading(self):
        return "SM" + str(random.choice(range(9)))

    """ Get vibration reading (3B) """
    def get_vibration_reading(self):
        return "VB" + str(random.choice(range(9)))

    """ Get battery voltage (3B) """
    def get_battery_voltage(self):
        return random.choice(range(9))

    """ Get battery current (3B) """
    def get_battery_current(self):
        return random.choice(range(9))

    """ Get analogue input (2B) """
    def get_analogue_input(self):
        ai_values = [ "A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9" ]
        return random.choice(ai_values)

    def __str__ (self):
        return struct.pack('!6s6s15s6s20s14s3s10s2s2s3s3s3s3s2s4s',
                           self.msgid,
                           self.atm.deviceid,
                           self.atm.imei,
                           self.atm.atmid,
                           self.nmr,
                           self.date,
                           str(self.temp).zfill(3),
                           self.rfid,
                           self.din,
                           self.dout,
                           self.smoke,
                           self.vibration,
                           str(self.voltage).zfill(3),
                           str(self.current).zfill(3),
                           self.analogue,
                           self.rfu)

"""
Health Packet format

06B: Message ID
06B: Device ID
15B: IMEI ID of GSM Module
06B: ATM ID
20B: NMR (Network Code, Location Code, Cell ID, Receive Signal Strength, CSQ)
14B: Date/Time received from Mobile tower (YYYYMMDDHHMMSS)
02B: Status (Camera_OK, UPS_OK, Internal_Battery_OK, Power_cable_connected, Device_open)
04B: Data1
04B: Data2
04B: RFU
"""
class HealthData:
    def __init__ (self, atm):
        self.msgid = "$PHLT"
        self.atm = atm
        self.nmr = id_gen(20)
        self.date = get_date()
        self.status = "OK"
        self.data1 = id_gen(4)
        self.data2 = id_gen(4)
        self.rfu = "RFUU"

    def __str__ (self):
        return struct.pack('!5s6s15s6s20s14s2s4s4s4s',
                           self.msgid,
                           self.atm.deviceid,
                           self.atm.imei,
                           self.atm.atmid,
                           self.nmr,
                           self.date,
                           self.status,
                           self.data1,
                           self.data2,
                           self.rfu)

class ATM:
    def __init__ (self, deviceid, imei, atmid):
        self.deviceid = deviceid
        self.imei = imei
        self.atmid = atmid

    def getSensorData (self, id):
        reading = SensorReading(self)
        temp = 'sensor%d.txt' % id
        f = open(temp, 'w+')
        f.write(str(reading))
        f.close()

    def getHealthData (self, id):
        reading = HealthData(self)
        temp = 'health%d.txt' % id
        f = open(temp, 'w+')
        f.write(str(reading))
        f.close()

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print "Must provide number of messages to be sent"
        sys.exit(1)
    else:
        print "Sending %d messages" % (int(sys.argv[1]))

    for _ in range(int(sys.argv[1])):
        atm = ATM(id_gen(), id_gen(15), id_gen())
        print "deviceid = %s" % (atm.deviceid)
        print "imeiid = %s" % (atm.imei)
        print "atmid = %s" % (atm.atmid)
        atm.getSensorData(_)
        atm.getHealthData(_)

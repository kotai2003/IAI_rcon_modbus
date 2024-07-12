#!/usr/bin/env python
""" This file can be used to communicate
with the IAI linear actuators over an RS485
communication bus.

The documentation for the ROBONet controller
is in DOC ROBONET(ME0208-13A-A).pdf

Discussion of the serial protocol begins
on page 141 section 3.9.2

Link with C code for crc calculation:
http://www.nongnu.org/avr-libc/user-manual/group__util__crc.html

Link with CRC explanation:
http://www.barrgroup.com/Embedded-Systems/How-To/CRC-Calculation-C-Code

Further details in:
Jack Crenshaw's "Implementing CRCs"
article in the January 1992
issue of Embedded Systems Programming

Page 70 - 71
The address map

Servo On
Home Ctrl
Send Position
Send Start Command

PC software edit the parameter


"""
import struct
import serial
import time


## Packet Description

# Header T1-T2-T3-T4 (silent interval)
    # 3.5 characters or more
# Address 8-bit \x3F (3FH)
# Function 8-bit
    # Read holding register \x03
    # Preset single register \x06
    # Preset multiple resgister \x10
# Data N x 8-bit
    # variable length and may be ommitted
# Error check 16-bit CRC
# Trailer T1-T2-T3-T4 (silent interval)
    # 3.5 characters or more

def crc_update(crc, a):
    """ For a character calculate crc """

    crc ^= ord(a)
    for i in range(8):
        if crc & 1:
            crc = (crc >> 1) ^ 0xA001
        else:
            crc = crc >> 1
    return crc

def calc_crc(values):
    CRC = 0xFFFF
    for value in values:
        CRC = crc_update(CRC, value)
    crcbytes = struct.pack('BB',
            CRC & 0xFF,
            (CRC & 0xFF00) >> 8)
    return values + crcbytes

def valid_crc(msg, msgcrc):
    return calc_crc(msg) == msgcrc

# Page 152
gwstatus = "\x3f\x03\xf7\x00\x00\x02"
gwstatus = calc_crc(gwstatus)
# print 'Gateway status query: %s' % gwstatus.encode('hex').upper()

# Page 155
axis0pos = "\x3f\x03\xf7\x08\x00\x02"
axis0pos = calc_crc(axis0pos)
#print 'Query Axis 0 pos: %s' % axis0pos.encode('hex').upper()

# Page 161
axis0status = "\x3f\x03\xf7\x0b\x00\x01"
axis0status = calc_crc(axis0status)

#print 'Query Axis 0 status: %s' % axis0status.encode('hex').upper()

# Page 158
axis1alarm = "\x3f\x03\xf7\x12\x00\x01"
axis1alarm = calc_crc(axis1alarm)

#print 'Query Axis 1 alarm: %s' % axis1alarm.encode("hex").upper()

# Page
resetcmd0 = "\x3f\x06\xf6\x0b\x00\x08"
resetcmd0 = calc_crc(resetcmd0)

print 'Reset command axis 0: %s' % resetcmd0.encode("hex").upper()

resetcmd1 = "\x3f\x06\xf6\x0f\x00\x08"
resetcmd1 = calc_crc(resetcmd1)

print 'Reset command axis 1: %s' % resetcmd1.encode("hex").upper()


# Page 184
axis1dir = '\x3f\x10\xf6\x0c\x00\x08\x10\x3a\x98\x00' \
            '\x00\x00\x0a\x00\x00\x00\x32\x00\x1e\x00' \
            '\x00\x00\x11'

axis1dir = calc_crc(axis1dir)


print "Axis 1 Direct mode: %s" % axis1dir.encode("hex").upper()


# Page 166
homeretcmd0 = "\x3f\x06\xf6\x0b\x00\x12"
homeretcmd0 = calc_crc(homeretcmd0)

print "Home return command: %s" % homeretcmd0.encode("hex").upper()

# Page 167
startcmd0 = "\x3f\x06\xf6\x0b\x00\x11"
startcmd0 = calc_crc(startcmd0)

print "Start command: %s" % startcmd0.encode("hex").upper()


# Page 168
pausecmd = "\x3f\x06\xf6\x0b\x00\x14"
pausecmd = calc_crc(pausecmd)

print "Pause command: %s" % pausecmd.encode("hex").upper()

# Page 184
axis0dir = '\x3f\x10\xf6\x08\x00\x08\x10\x3a\x98\x00' \
            '\x00\x00\x0a\x00\x00\x00\x32\x00\x1e\x00' \
            '\x00\x00\x11'

axis0dir = calc_crc(axis0dir)


print "Axis 0 Direct mode: %s" % axis0dir.encode("hex").upper()

# page 165
axis0son = '\x3f\x06\xf6\x0b\x00\x10'
axis0son = calc_crc(axis0son)
print "Axis 0 Servo on: %s" % axis0son.encode("hex").upper()

# Page 158
axis2alarm = "\x3f\x03\xf7\x13\x00\x01"
axis2alarm = calc_crc(axis2alarm)
print 'Query Axis 2 alarm: %s' % axis2alarm.encode("hex").upper()


# Always turn on
alwayson = "\x3f\x06\xf6\x00\x80\x00"
alwayson = calc_crc(alwayson)
print "Always run this: %s" % alwayson.encode("hex").upper()

# Brake release
axis0brake = '\x3f\x06\xf6\x0b\x80\x00'
axis0brake = calc_crc(axis0brake)
print "Axis 0 brake: %s" % axis0brake.encode('hex').upper()

class AxisStatus(object):

    INEMERGBIT = (1 << 15)
    INCRDYBIT = (1 << 14)
    INZONE1BIT = (1 << 13)
    INZONE2BIT = (1 << 12)
    INPZONEBIT = (1 << 11)
    INMODESBIT = (1 << 10)
    INWENDBIT = (1 << 9)
    INSVONBIT = (1 << 4)
    INALMBIT = (1 << 3)
    INMOVEBIT = (1 << 2)
    INHOMENDBIT = (1 << 1)
    INPOSENDBIT = (1 << 0)


    def __init__(self, status_value):
        self.status = status_value

    def isMoving(self):
        if self.status & self.INMOVEBIT:
            return True
        return False

    def isAlarm(self):
        if self.status & self.INALMBIT:
            return True
        return False

    def isHome(self):
        if self.status & self.INHOMENDBIT:
            return True
        return False

    def isInPosition(self):
        if self.status & self.INPOSENDBIT:
            return True
        return False

    def isServoOn(self):
        if self.status & self.INSVONBIT:
            return True
        return False

    def isPosLoad(self):
        if self.status & self.INWENDBIT:
            return True
        return False

    def isPosZone(self):
        if self.status & self.INPZONEBIT:
            return True
        return False

    def isZone1(self):
        if self.status & self.INZONE1BIT:
            return True
        return False

    def isZone2(self):
        if self.status & self.INZONE2BIT:
            return True
        return False

    def isCtrlReady(self):
        if self.status & self.INCRDYBIT:
            return True
        return False

    def isEmergencyStop(self):
        if self.status &  self.INEMERGBIT:
            return True
        return False

class LinearActuator(object):
    """ Interface for the IAI linear actuators
    """
    AXIS0INPUTOFFSET = 0xF608
    AXIS0OUTPUTOFFSET = 0xF708

    SLAVEADDRESS = 0x3F

    GWSTATUSOFFSET = 0xF700

    GWCTRLOFFSET = 0xF600

    WRITESINGLEREG = 0x06
    WRITEMULTIREG = 0x10
    READMULTIREG = 0x03

    CTRLOFFSET = 3
    LOPOSOFFSET = 0

    LOCURPOSOFFSET = 0
    STATUSOFFSET = 3

    OUTSONBIT = (1 << 4)
    OUTHOMEBIT = (1 << 1)
    OUTSTARTBIT = (1 << 0)
    OUTPAUSEBIT = (1 << 2)
    OUTBRKBIT = (1 << 15)
    OUTRESETBIT = (1 << 3)


    def __init__(self, axisid, com=None):
        self.axisid = axisid

        self.singbytefmt = struct.Struct(">B")
        self.twobytefmt = struct.Struct(">H")
        self.tworegfmt = struct.Struct(">HH")

        self.simulate = True
        if not com is None:
            self.com = com
            self.simulate = False

    def address(self):
        return self.singbytefmt.pack(self.SLAVEADDRESS)

    def calculateInputOffset(self):
        """ Calculate input offset """
        return self.AXIS0INPUTOFFSET + 4 * self.axisid

    def calculateOutputOffset(self):
        """ Calculate output offset """
        return self.AXIS0OUTPUTOFFSET + 4 * self.axisid

    def calculateControlReg(self):
        """ Control Reg Offet """
        return self.calculateInputOffset() + self.CTRLOFFSET

    def calculatePosReg(self):
        """ Pos register """
        return self.calculateInputOffset() + self.LOPOSOFFSET

    def calculateStatusReg(self):
        """ Status Register """
        return self.calculateOutputOffset() + self.STATUSOFFSET

    def calculateCurrentPosReg(self):
        """ Get current position """
        return self.calculateOutputOffset() + self.LOCURPOSOFFSET

    def multiWriteHeader(self, reg):
        """ Get Header for multibyte write """
        cmd = self.singbytefmt.pack(self.WRITEMULTIREG)
        reg = self.twobytefmt.pack(reg)
        return self.address() + cmd + reg

    def multiReadHeader(self, reg):
        """ Get header for multibyte read """
        cmd = self.singbytefmt.pack(self.READMULTIREG)
        reg = self.twobytefmt.pack(reg)
        return self.address() + cmd + reg

    def singleWriteHeader(self, reg):
        """ Get header for single byte write """
        cmd = self.singbytefmt.pack(self.WRITESINGLEREG)
        reg = self.twobytefmt.pack(reg)
        return self.address() + cmd + reg

    def send(self, msg):
        """ Send command to system """
        print "Sent:%s" % msg.encode('hex').upper()
        if  not self.simulate:
            self.clear_buffer()
            self.com.write(msg)

    def receiveSingleRegWrite(self, msg):
        """ Receive the expected number of bytes """
        time.sleep(0.1)
        expectedmsglen = len(msg)
        if not self.simulate:
            resp = self.com.read(len(msg))
        else:
            resp = msg

        if len(resp) == len(msg):
            print "Query and response length matches"
            if resp == msg:
                print "System validated command"

        return resp

    def receiveMultiWrite(self, msg, exampleresp=None):
        """ Receive the expected number of bytes """
        time.sleep(0.1)
        numreg = msg[4:6]
        numreg = self.twobytefmt.unpack(numreg)[0]
        numbytes = numreg * 2
        print "Expected numreg written: %d" % numreg
        print "Expected numbytes written: %d" % numbytes
        expectedmsglen = 8

        if self.simulate and exampleresp is None:
            resp = self.singbytefmt.pack(self.SLAVEADDRESS)
            resp += self.singbytefmt.pack(self.WRITESINGLEREG)
            resp += self.twobytefmt.pack(numreg)
            resp = calc_crc(resp)
            print "Simulated resp %s" % resp.encode('hex').upper()

        elif not self.simulate and not exampleresp is None:
            resp = exampleresp
        else:
            # Get response!
            resp = self.com.read(expectedmsglen)


        if valid_crc(resp[:-2],resp):
            print "System validated command"

        byteswritten = self.twobytefmt.unpack(resp[2:4])
        print "Confirmed wrote %d" % byteswritten

        return byteswritten


    def receiveMultiRead(self, msg, exampleresp=None):
        """ Receive the expected number of bytes """

        numreg = msg[-4:-2]
        numreg = self.twobytefmt.unpack(numreg)[0]
        numbytes = numreg * 2
        print "Numreg: %d" % numreg
        print "Numbytes: %d" % numbytes

        expectedmsglen = 5 + numbytes

        if self.simulate and exampleresp is None:
            print "Generate Example"
            resp = self.singbytefmt.pack(self.SLAVEADDRESS)
            resp += self.singbytefmt.pack(self.READMULTIREG)
            resp += self.singbytefmt.pack(numbytes)
            msgbytesfmt = struct.Struct(">"+ "B" * numbytes)
            data = [0 for i in range(numbytes)]
            resp += msgbytesfmt.pack(*data)
            resp = calc_crc(resp)
        elif self.simulate and not expectedmsglen is None:
            print "Using given example"
            resp = exampleresp
        else:
            print "Receive multiread"
            resp = self.com.read(expectedmsglen)
            print "MultiRead: %s" % resp.encode("hex").upper()

        if len(resp) == expectedmsglen:
            print "Received correct number of bytes"

        respnochk = resp[:-2]
        respck = calc_crc(respnochk)

        if respck == resp:
            print "crc check ok"

        else:
            print "invalid crc"

        print "Resp:%s" % resp.encode('hex').upper()

        payload = resp[3:-2]
        print "Payload: %s" % payload.encode('hex').upper()
        return payload


    def writeControl(self, value):
        """ Write the control """
        hdr = self.singleWriteHeader(self.calculateControlReg())
        value = self.twobytefmt.pack(value)
        msg = hdr + value
        msg = calc_crc(msg)
        self.send(msg)
        resp = self.receiveSingleRegWrite(msg)
        print "Resp:%s" % resp.encode('hex').upper()

    def writePos(self, posmm):
        """ Write the Pos """
        hdr = self.multiWriteHeader(self.calculatePosReg())
        numreg = self.twobytefmt.pack(2)
        numbytes = self.singbytefmt.pack(4)
        posmm = int(posmm * 100)
        loval = posmm & 0xFFFF
        loval = self.twobytefmt.pack(loval)
        hival = (posmm & 0xFFFF0000) >> 16
        hival = self.twobytefmt.pack(hival)
        msg = hdr + numreg + numbytes + loval + hival
        msg = calc_crc(msg)
        print "Sent:%s" % msg.encode('hex').upper()

        if not self.simulate:
            self.com.write(msg)
            self.receiveMultiWrite(msg)
        else:
            # Read resp
            pass


    def readStatus(self):
        hdr = self.multiReadHeader(self.calculateStatusReg())
        numreg = self.twobytefmt.pack(1)
        msg = hdr + numreg
        msg = calc_crc(msg)
        print "Sent:%s" % msg.encode('hex').upper()

        if self.simulate:
            resp = "\x3F\x03\x02\x70\x13\xF5\x8C"
        else:
            resp = None
            self.com.write(msg)

        payload = self.receiveMultiRead(msg, resp)
        #print "Resp:%s" % resp.encode('hex').upper()
        print "Payload: %s" % payload.encode('hex').upper()
        return self.twobytefmt.unpack(payload)[0]

    def readCurrentPos(self):
        hdr = self.multiReadHeader(self.calculateCurrentPosReg())
        numreg = self.twobytefmt.pack(2)
        msg = hdr + numreg
        msg = calc_crc(msg)

        print "Sent:%s" % msg.encode('hex').upper()

        if self.simulate:
            resp = "\x3F\x03\x04\x38\xA5\x00\x00\x38\xB3"
            payload = self.receiveMultiRead(msg,
                    exampleresp=resp)
        else:
            self.com.write(msg)
            payload = self.receiveMultiRead(msg)


        pos = payload
        print pos.encode('hex').upper()
        pos = self.tworegfmt.unpack(pos)
        print pos[0], (pos[1] << 16)
        pos = pos[0] + (pos[1] << 16)
        if pos & (1<<31):
            pos &= ~(1<<31)
            pos = -1*pos

        print "%f mm" % (pos / 100.0)

        self.receiveMultiRead(msg)
        return pos / 100.0

    def readGatewayStatus(self):
        hdr = self.multiReadHeader(self.GWSTATUSOFFSET)
        numreg = self.twobytefmt.pack(2)
        msg = hdr + numreg
        msg = calc_crc(msg)
        exresp = "\x3F\x03\x04\x80\x21\x00\x03\x1C\x3B"
        payload = self.receiveMultiRead(msg, exresp)
        print "Sent:%s" % msg.encode('hex').upper()
        print "Payload:%s" % payload.encode('hex').upper()


    def writeAppCtrl(self):
        hdr = self.singleWriteHeader(self.GWCTRLOFFSET)
        value = self.twobytefmt.pack(0x8000)
        msg = hdr + value
        msg = calc_crc(msg)

        print "Sent:%s" % msg.encode('hex').upper()
        if self.simulate:
            resp = msg
        else:
            self.com.write(msg)
            resp = self.receiveSingleRegWrite(msg)

        print "Resp:%s" % resp.encode('hex').upper()


    def pause(self):
        """ Pause actuator """
        self.writeControl(self.OUTSONBIT|self.OUTPAUSEBIT)

    def home(self):
        """ Home actuator """
        self.writeControl(self.OUTSONBIT|self.OUTHOMEBIT)

    def start(self):
        """ Start motion """
        self.writeControl(self.OUTSONBIT|self.OUTSTARTBIT)

    def reset(self):
        """ Reset actuator """
        self.writeControl(self.OUTRESETBIT)

    def clear_buffer(self):
        """ Flush input buffer """
        if not self.simulate:
            self.com.flushInput()

    def status(self):
        """ Read Status """
        return AxisStatus(self.readStatus())

class IAI(object):
    def __init__(self, simulate=True):
        self.sim = simulate
        if not simulate:
            self.s = serial.Serial("COM5",
                                baudrate=230400,
                               timeout=0.5)

    def turnon(self):
        print "TURNON: %s" % alwayson.encode('hex').upper()

        if not self.sim:
            self.s.write(alwayson)
            time.sleep(0.1)
            v = self.s.readline().encode('hex').upper()
            print v

    def start0(self):
        print "START AXIS 0: %s" % startcmd0.encode('hex').upper()

        if not self.sim:
            self.s.write(startcmd0)
            time.sleep(0.1)
            v = self.s.readline().encode('hex').upper()
            print v

    def home0(self):
        print "HOME AXIS 0: %s" % homeretcmd0.encode('hex').upper()

        if not self.sim:
            self.s.write(homeretcmd0)
            time.sleep(0.1)
            v = self.s.readline().encode('hex').upper()
            print v

    def reset0(self):
        print "RESET AXIS 0: %s" % resetcmd0.encode('hex').upper()

        if not self.sim:
            self.s.write(resetcmd0)
            time.sleep(0.1)
            v = self.s.readline().encode('hex').upper()
            print v

    def move0(self, posmm):
        pos = [0,0,0,0]
        axis0setpos = "\x3f\x10\xf6\x08\x00\x02\x04"
        pos[1] = posmm & 0xFF
        pos[0] = (posmm & 0xFF00) >> 8
        pos[3] = (posmm & 0xFF0000) >> 16
        pos[2] = (posmm & 0xFF000000) >> 24

        for p in pos:
            axis0setpos += chr(p)

        axis0setpos = calc_crc(axis0setpos)

        print "Move to %d mm: %s" % (posmm, axis0setpos.encode('hex').upper())

        if not self.sim:
            self.s.write(axis0setpos)
            time.sleep(0.1)
            v = self.s.readline().encode('hex').upper()
            print v

    def status0(self):
        print "STATUS AXIS 0: %s" % axis0status.encode('hex').upper()

        if not self.sim:
            self.s.write(axis0status)
            time.sleep(0.1)
            v = self.s.readline().encode('hex').upper()
            print v

    def gwstatus(self):
        print "STATUS GW: %s" % gwstatus.encode('hex').upper()

        if not self.sim:
            self.s.write(gwstatus)
            time.sleep(0.1)
            v = self.s.readline().encode('hex').upper()
            print v

    def pos0(self):
        print "MONITOR POSITION: %s" % axis0pos.encode('hex').upper()

        if not self.sim:
            self.s.write(axis0pos)
            time.sleep(0.1)
            v = self.readline().encode('hex').upper()
            print v
        else:
            v = "\x3f\x03\x04\x38\xa5\x00\x00\x38\xb3"
        vnochk = v[:-2]
        vck = calc_crc(vnochk)
        if vck == v:
            print "crc check ok"

        else:
            print "invalid crc"

        pos = vnochk[3:]
        print pos.encode('hex').upper()
        s = struct.struct(">hh")
        pos = s.unpack(pos)
        print pos[0], (pos[1] << 16)
        pos = pos[0] + (pos[1] << 16)
        print "%f mm" % (pos / 100.0)

        return pos / 100.0

if __name__ == '__main__':
    import serial
    s = serial.Serial("COM4", baudrate=115200, timeout=0.5)
    linact = LinearActuator(0)
    linact.writeAppCtrl()
    linact.reset()
    linact.home()
    linact.readStatus()
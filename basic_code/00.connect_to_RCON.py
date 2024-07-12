import minimalmodbus
import serial

# minimalmodbusの設定
minimalmodbus.BAUDRATE = 115200       # 接続する機器に応じて設定変更
minimalmodbus.BYTESIZE = 8            # 接続する機器に応じて設定変更
minimalmodbus.STOPBITS = 1            # 接続する機器に応じて設定変更
minimalmodbus.TIMEOUT = 1             # 単位: 秒
minimalmodbus.PARITY = serial.PARITY_NONE
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True

# インストゥルメントの設定
instrument = minimalmodbus.Instrument('COM4', 1, mode=minimalmodbus.MODE_RTU)


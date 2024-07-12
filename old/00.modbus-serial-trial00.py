# https://rightcode.co.jp/blog/information-technology/python-modbus-communication

import minimalmodbus as modbus
import serial
import struct

#minimalmodbusの設定
modbus.baudrate = 115200# 57600 #接続する機器に応じて設定変更
modbus.bytesize = 8     #接続する機器に応じて設定変更
modbus.stopbits = 1     #接続する機器に応じて設定変更
modbus.timeout=1        #単位sec：接続先に合わせる必要はない
modbus.parity= serial.PARITY_NONE     #接続する機器に応じて設定変更
modbus.CLOSE_PORT_AFTER_EACH_CALL=True
inst = modbus.Instrument('COM4',1,modbus.MODE_RTU)  #COM_は使用するパソコンのシリアルポートに合わせる

# #アドレス0x1001への読み出し処理
# # rd_data = inst.read_register(int(0x1001),functioncode=3,signed = False)
# # rd_data = inst.read_register(int(0x1000)+ 16*0 + int(0x0000),functioncode=3,signed = False)
# rd_data = inst.read_register(int(0x1000)+ 16*0 + int(0x0000),functioncode=3,signed = False)
#
# print(rd_data)

#アドレス0x1001への書き込み処理
# inst.write_register(int(0x1001),value = 16,functioncode=6,signed = False)

# Modbusアドレスは0から始まるため、9000の代わりに8999を使用
try:
    # レジスタ9000から10レジスタ分のデータを読み取る
    register_data = inst.read_registers(8990, 2, functioncode=3)
    print(register_data)
except IOError:
    print("Failed to read from instrument")


# # 通信テストのための読み取りを試みる
# try:
#     # 例: アドレス0からの保持レジスタの読み取りを試みる
#     # ここでの0はModbusレジスタのアドレスです
#     value = inst.read_register(0, 0)
#     print(f"Read value: {value}")
#     print("Communication is OK!")
# except (modbus.ModbusException, serial.serialutil.SerialException) as e:
#     print(f"Communication error: {e}")
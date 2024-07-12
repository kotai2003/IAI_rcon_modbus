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
instrument = minimalmodbus.Instrument('COM4', 1, mode=minimalmodbus.MODE_RTU)  # COMポートとModbusアドレスに応じて変更

# レジスタに書き込む関数
def write_register(address, value):
    try:
        instrument.write_register(address, value, functioncode=6)
        print(f"Successfully wrote {value} to register {address}")
    except IOError:
        print(f"Failed to write to register {address}")

# レジスタから読み取る関数
def read_register(address):
    try:
        value = instrument.read_register(address, functioncode=3)
        print(f"Value read from register {address}: {value}")
        return value
    except IOError:
        print(f"Failed to read from register {address}")
        return None

# アラームリセットコマンド送信（0軸目）
write_register(0x0D00, 0x0100)

# サーボONコマンド送信（0軸目）
write_register(0x0D00, 0x1010)
print("servo on")
# ジョグ+方向動作指令コマンド送信（0軸目）
# write_register(0x0D01, 0x0200)
#
# # 原点復帰コマンド送信（0軸目）
# write_register(0x0D00, 0x1010)  # サーボON状態を維持
# write_register(0x0D01, 0x1010)  # 原点復帰コマンド

# # サーボOFFコマンド送信（0軸目）
# write_register(0x0D00, 0x0000)
# print("servo off")

# レジスタの値を読み取る（例: アドレス0x1000）
read_register(0x1000)

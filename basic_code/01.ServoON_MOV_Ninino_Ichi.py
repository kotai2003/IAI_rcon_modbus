import minimalmodbus
import serial
import time

# minimalmodbusの設定
minimalmodbus.BAUDRATE = 115200       # 接続する機器に応じて設定変更
minimalmodbus.BYTESIZE = 8            # 接続する機器に応じて設定変更
minimalmodbus.STOPBITS = 1            # 接続する機器に応じて設定変更
minimalmodbus.TIMEOUT = 1             # 単位: 秒
minimalmodbus.PARITY = serial.PARITY_NONE
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True

# インストゥルメントの設定
instrument = minimalmodbus.Instrument('COM4', 1, mode=minimalmodbus.MODE_RTU)


# アラームリセットコマンドの送信
register_address = 0x0D00  # レジスタアドレス（16進数表記）
value_to_write = 0x1000  # 書き込む値（16進数表記）
instrument.write_register(register_address, value_to_write, functioncode=6)
print("アラームリセットコマンドを送信しました。")

# 正常リスポンスの受信
read_value = instrument.read_register(register_address)
print(f'Read Value: {read_value}')

# サーボONコマンドの送信
register_address = 0x0D00  # レジスタアドレス（16進数表記）
value_to_write = 0x1000  # データ（16進数表記）
instrument.write_register(register_address, value_to_write, functioncode=6)

# 現在のサーボ状態の読み取り
servo_status = instrument.read_register(register_address, functioncode=3)
print(f'Servo Status: {servo_status}')

# 原点復帰コマンドの送信
register_address = 0x0D00  # レジスタアドレス（16進数表記）
value_to_write = 0x1010  # 書き込む値（16進数表記）
instrument.write_register(register_address, value_to_write, functioncode=6)

# 現在のサーボ状態の読み取り
servo_status = instrument.read_register(register_address, functioncode=3)
print(f'Servo Status: {servo_status}')

time.sleep(3)
print("time sleeped")
#------------------------------------------------------------------------------

# 0軸目の各パラメータ設定

# 位置 (Position) 50.00mm
position_value = 0x00001388 # 小数点以下2桁までの整数に変換
# 位置決め幅 (Positioning Width) 0.10mm
positioning_width_value = 0x0000000A  # 小数点以下2桁までの整数に変換
# 速度 (Speed) 100.0mm/s
speed_value = 0x00002710 # 小数点以下2桁までの整数に変換
# 加減速度 (Acceleration/Deceleration) 0.10G
acceleration_value = 0x000A  # 小数点以下2桁までの整数に変換

# 各レジスタにデータを書き込む
register_values = [
    position_value,        # 位置
    positioning_width_value,  # 位置決め幅
    speed_value,           # 速度
    acceleration_value     # 加減速度
]

# Function code 16 (0x10) を使用して複数レジスタ書き込み
instrument.write_registers(0x9900, register_values)

print("直接数値指定・位置決め動作の各パラメータを設定しました。")
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

# ポジション番号指定のためのレジスタアドレス
register_address = 0x9800  # 16進数
value_to_write = 1  # ポジション番号1

# コマンド送信
instrument.write_register(register_address, value_to_write, functioncode=6)

# レスポンスを確認するための読み取り（オプション）
response = instrument.read_register(register_address)
print(f"レスポンス: {response}")
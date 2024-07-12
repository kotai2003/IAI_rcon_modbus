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
move_command_register = 0x9800  # 16進数
position_status_register = 0x9014  # 完了ポジション番号を確認するためのレジスタアドレス

# ポジション番号を指定する関数
def move_to_position(position_number):
    # ポジション番号指定のコマンド送信
    instrument.write_register(move_command_register, position_number, functioncode=6)

    # 移動完了の確認
    def is_move_complete():
        status = instrument.read_register(position_status_register, functioncode=3)
        return (status & (1 << (position_number - 1))) != 0

    # 移動が完了するまで待機
    while not is_move_complete():
        time.sleep(0.1)  # 100ms待機

    # 完了ポジション番号を取得
    completed_position = instrument.read_register(position_status_register, functioncode=3)
    print(f"完了ポジション番号: {completed_position}")

# ポジションNo.1からNo.10までの移動を確認するループ
# for pos in range(1, 3):
#     print(f"ポジションNo.{pos}に移動中...")
#     move_to_position(pos)
#     print(f"ポジションNo.{pos}への移動が完了しました。")

move_to_position(1)
print(f"ポジションNo.1への移動が完了しました。")
move_to_position(2)
print(f"ポジションNo.2への移動が完了しました。")
# move_to_position(0)
# print(f"ポジションNo.2への移動が完了しました。")
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



# サーボONコマンドの送信
register_address = 0x0D00  # レジスタアドレス（16進数表記）
value_to_write = 0x1000  # データ（16進数表記）
instrument.write_register(register_address, value_to_write, functioncode=6)

# 現在のサーボ状態の読み取り
servo_status = instrument.read_register(register_address, functioncode=3)
print(f'Servo Status: {servo_status}')


# 原点復帰完了の確認



# 原点復帰コマンドの送信
register_address = 0x0D00  # レジスタアドレス（16進数表記）
value_to_write = 0x1010  # 書き込む値（16進数表記）


# DSS1レジスタのアドレス
dss1_register = 0x9005  # DSS1レジスタのアドレス（マニュアルに基づく）

# 原点復帰指令の送信
instrument.write_register(register_address, value_to_write, functioncode=6)


def check_hend_bit():
    status = instrument.read_register(dss1_register, functioncode=3)


    hend_bit = (status & 0x0010) >> 4  # HENDビット（ビット4）を抽出
    return hend_bit

# HENDビットの確認
hend_status = check_hend_bit()

def is_home_complete():
    status = instrument.read_register(dss1_register, functioncode=3)
    hend_bit = (status & 0x0010) >> 4  # HENDビット（ビット4）を抽出

    print(f"status, {status}")
    print(f"status & 0x0010,{status & 0x0010}")
    print(f"(status & 0x0010) >> 4, {(status & 0x0010) >> 4} ")

    if hend_status == 1:
        print("原点復帰が完了しました。")
    else:
        print("原点復帰はまだ完了していません。")

    return hend_bit  # HENDビットが1であれば原点復帰完了

# 原点復帰が完了するまで待機
while not is_home_complete():
    time.sleep(0.1)  # 100ms待機


print("原点復帰が完了しました。")


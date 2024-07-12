import minimalmodbus as modbus
import serial

# minimalmodbusの設定
modbus.BAUDRATE = 115200
modbus.BYTESIZE = 8
modbus.STOPBITS = 1
modbus.TIMEOUT = 1
modbus.PARITY = serial.PARITY_NONE
modbus.CLOSE_PORT_AFTER_EACH_CALL = True
inst = modbus.Instrument('COM4', 1, mode=modbus.MODE_RTU)


# データを書き込む関数
def write_multiple_registers():
    try:
        # 伝文に基づくデータ配列
        data = [
            5000,  # 0x1388 -> 位置 50.00 mm
            10,  # 0x000A -> 位置決め幅 0.10 mm
            10000,  # 0x2710 -> 速度 100.0 mm/s
            10,  # 0x000A -> 加速度 0.10G
            10  # 0x000A -> 減速度 0.10G
        ]

        # 0x9900から始まるレジスタに書き込み
        inst.write_registers(0x9900, data)
        print("Registers written successfully")
    except IOError as e:
        print(f"Failed to write registers: {e}")


# 実行
write_multiple_registers()

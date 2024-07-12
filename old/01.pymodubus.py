# from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.client import ModbusSerialClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.exceptions import ModbusException

#---------- 接続開始 ----------#
client = ModbusClient(method ='rtu', port="COM4",stopbits = 1, bytesize = 8, baudrate= 115200, timeout= 1)
client.connect()

# 16進数のアドレス9000は10進数に変換する必要がある
# 16進数9000 -> 10進数は36864
start_address = 0x9000 - 1  # Modbusのアドレスは0から始まるので1を引く

# レジスタの読み取り
# スレーブアドレス1から、開始アドレス9000にある2つのレジスタを読み取る
try:
    response = client.read_holding_registers(start_address, 2, unit=1)
    # 応答が正常にあるかを確認する
    if not response.isError():
        print(response.registers)
    else:
        print(f"Modbus communication error: {response}")
except ModbusException as e:
    print(f"Modbus communication exception: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")

# 接続を閉じる
client.close()
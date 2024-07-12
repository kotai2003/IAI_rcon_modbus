import minimalmodbus
import serial
import time
import keyboard

class RCONController:
    def __init__(self, port, slave_address):
        self.port = port
        self.slave_address = slave_address
        self.instrument = None

    def connect(self):
        minimalmodbus.BAUDRATE = 115200
        minimalmodbus.BYTESIZE = 8
        minimalmodbus.STOPBITS = 1
        minimalmodbus.TIMEOUT = 1
        minimalmodbus.PARITY = serial.PARITY_NONE
        minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True

        try:
            self.instrument = minimalmodbus.Instrument(self.port, self.slave_address, mode=minimalmodbus.MODE_RTU)
            print(f"Connected to {self.port} with slave address {self.slave_address}")
        except IOError:
            print("Failed to connect to the instrument")

    def check_connection(self):
        if not self.instrument:
            print("Not connected to any instrument")
            return
        try:
            response = self.instrument.read_register(0, 1)  # レジスタアドレス0から1ワード読み取る
            print(f"Response: {response}")
        except IOError:
            print("Failed to communicate with the instrument")

    def reset_alarm(self):
        if not self.instrument:
            print("Not connected to any instrument")
            return
        try:
            register_address = 0x0D00  # レジスタアドレス（16進数表記）
            value_to_write = 0x0001  # 書き込む値（16進数表記）
            self.instrument.write_register(register_address, value_to_write, functioncode=6)
            print("アラームリセットコマンドを送信しました。")

            # 正常リスポンスの受信
            read_value = self.instrument.read_register(register_address)
            print(f'Read Value: {read_value}')
        except IOError:
            print("Failed to send Alarm Reset command")

    def servo_on(self):
        if not self.instrument:
            print("Not connected to any instrument")
            return
        try:
            register_address = 0x0D00  # レジスタアドレス（16進数表記）
            value_to_write = 0x1000  # データ（16進数表記）
            self.instrument.write_register(register_address, value_to_write, functioncode=6)
            print("サーボONコマンドを送信しました。")

            # 現在のサーボ状態の読み取り
            servo_status = self.instrument.read_register(register_address, functioncode=3)
            print(f'Servo Status: {servo_status}')
        except IOError:
            print("Failed to send Servo ON command")

    def home(self):
        if not self.instrument:
            print("Not connected to any instrument")
            return
        try:
            register_address = 0x0D00  # レジスタアドレス（16進数表記）
            value_to_write = 0x1010  # 書き込む値（16進数表記）
            dss1_register = 0x9005  # DSS1レジスタのアドレス（マニュアルに基づく）

            # 原点復帰指令の送信
            self.instrument.write_register(register_address, value_to_write, functioncode=6)
            print("原点復帰コマンドを送信しました。")

            # 原点復帰が完了するまで待機
            while not self.is_home_complete(dss1_register):
                time.sleep(0.1)  # 100ms待機

            print("原点復帰が完了しました。")
        except IOError:
            print("Failed to send Home command")

    def is_home_complete(self, dss1_register):
        try:
            status = self.instrument.read_register(dss1_register, functioncode=3)
            hend_bit = (status & 0x0010) >> 4  # HENDビット（ビット4）を抽出

            # print(f"status, {status}")
            # print(f"status & 0x0010, {status & 0x0010}")
            # print(f"(status & 0x0010) >> 4, {(status & 0x0010) >> 4} ")

            if hend_bit == 1:
                print("原点復帰が完了しました。")
            else:
                pass

            return hend_bit  # HENDビットが1であれば原点復帰完了
        except IOError:
            print("Failed to read DSS1 register")
            return False

    def move_to_position_number(self, position_number):
        if not self.instrument:
            print("Not connected to any instrument")
            return
        try:
            move_command_register = 0x9800  # ポジション番号指定のためのレジスタアドレス
            position_status_register = 0x9014  # 完了ポジション番号を確認するためのレジスタアドレス

            # ポジション番号指定のコマンド送信
            self.instrument.write_register(move_command_register, position_number, functioncode=6)
            print(f"ポジション番号{position_number}への移動コマンドを送信しました。")

            # 移動完了の確認
            def is_move_complete():
                status = self.instrument.read_register(position_status_register, functioncode=3)
                return (status & (1 << (position_number - 1))) != 0

            # 移動が完了するまで待機
            while not is_move_complete():
                time.sleep(0.1)  # 100ms待機

            # 完了ポジション番号を取得
            completed_position = self.instrument.read_register(position_status_register, functioncode=3)
            print(f"完了ポジション番号: {completed_position}")

        except IOError:
            print("Failed to move to the specified position number")


# メイン処理
if __name__ == "__main__":
    rcon = RCONController('COM4', 1)
    rcon.connect()
    rcon.check_connection()
    rcon.reset_alarm()
    rcon.servo_on()
    rcon.home()

    print("Press 'q' to stop the loop.")
    while True:
        rcon.move_to_position_number(2)
        print(f"ポジションNo.2への移動が完了しました。")
        rcon.move_to_position_number(1)
        print(f"ポジションNo.1への移動が完了しました。")

        if keyboard.is_pressed('q'):
            print("Stopping the loop.")
            break

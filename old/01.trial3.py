import minimalmodbus as modbus
import serial

# minimalmodbusの設定
modbus.baudrate = 115200  # 接続する機器に応じて設定変更
modbus.bytesize = 8       # 接続する機器に応じて設定変更
modbus.stopbits = 1       # 接続する機器に応じて設定変更
modbus.timeout = 1        # 単位sec：接続先に合わせる必要はない
modbus.parity = serial.PARITY_NONE  # 接続する機器に応じて設定変更
modbus.CLOSE_PORT_AFTER_EACH_CALL = True
inst = modbus.Instrument('COM4', 1, modbus.MODE_RTU)  # COM_は使用するパソコンのシリアルポートに合わせる

# 原点復帰のコマンド
def home_return():
    try:
        inst.write_register(0x0D00, 0x1000, functioncode=6)  # HOME_RETURN
        print("Homing successful")
    except IOError as e:
        print(f"Failed to send homing command: {e}")

# SERVO OFFのコマンド
def servo_off():
    try:
        inst.write_register(0x0D00, 0x0002, functioncode=6)  # SERVO_OFF
        print("Servo OFF successful")
    except IOError as e:
        print(f"Failed to send servo off command: {e}")

# 速度、加速度、減速度の設定と位置移動
def set_motion_params_and_move():
    try:
        # 速度を20 mm/sに設定
        print("Setting speed to 20 mm/s")
        inst.write_register(0xA100, 20000, functioncode=6)  # 速度設定 (0xA100 = 速度設定のアドレス, 20000 = 20 mm/s)

        # 加速度を0.30 Gに設定
        print("Setting acceleration to 0.30 G")
        inst.write_register(0xA101, 300, functioncode=6)  # 加速度設定 (0xA101 = 加速度設定のアドレス, 300 = 0.30 G)

        # 減速度を0.30 Gに設定
        print("Setting deceleration to 0.30 G")
        inst.write_register(0xA102, 300, functioncode=6)  # 減速度設定 (0xA102 = 減速度設定のアドレス, 300 = 0.30 G)

        # 80mmまで移動
        print("Moving to 80mm")
        inst.write_register(0xA103, 80, functioncode=6)  # 位置設定 (0xA103 = 位置設定のアドレス, 80 = 80mm)

        # 400mmまで移動
        print("Moving to 400mm")
        inst.write_register(0xA103, 400, functioncode=6)  # 位置設定 (0xA103 = 位置設定のアドレス, 400 = 400mm)

        print("Motion parameters set and move commands sent successfully")
    except IOError as e:
        print(f"Failed to set motion parameters or move: {e}")

# 実行
home_return()
set_motion_params_and_move()
servo_off()

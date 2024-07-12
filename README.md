# IAI RCON Controller using Modbus RTU with Python

This project provides a Python script to control an IAI RCON controller using the Modbus RTU protocol. It leverages the `minimalmodbus` library for easy Modbus communication. The script includes functionalities to connect to the controller, reset alarms, turn the servo on, perform homing, and move to specified position numbers.

![rcp4-main](https://github.com/user-attachments/assets/6e10ca36-7dcc-4521-8b6d-ce12c218e586)

## Features

- Connect to the IAI RCON controller via Modbus RTU.
- Reset alarms.
- Turn the servo on.
- Perform homing operation.
- Move to specified position numbers.
- Continuously move between two positions until the 'q' key is pressed.
- 
![rcon](https://github.com/user-attachments/assets/382486b5-2cb5-4f76-8106-378d1f56daff)

## Requirements

- Python 3.x
- `minimalmodbus` library
- `pyserial` library
- `keyboard` library

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/iai-rcon-controller.git
    cd iai-rcon-controller
    ```

2. Install the required libraries:
    ```bash
    pip install minimalmodbus pyserial keyboard
    ```

## Usage

1. Connect the IAI RCON controller to your computer.
2. Ensure the serial port and slave address in the script match your setup.
3. Run the script:
    ```bash
    python iai_rcon_controller.py
    ```

4. The script will:
    - Connect to the RCON controller.
    - Reset alarms.
    - Turn the servo on.
    - Perform homing.
    - Move between position numbers 2 and 1 in a loop.
    - Stop the loop when the 'q' key is pressed.

## Code Explanation

The script is organized into a class `RCONController` which encapsulates all the functionality needed to control the IAI RCON controller. Below is an overview of the methods:

- `__init__(self, port, slave_address)`: Initializes the controller with the specified serial port and slave address.
- `connect(self)`: Establishes the Modbus connection with the specified parameters.
- `check_connection(self)`: Checks the connection by reading a register.
- `reset_alarm(self)`: Resets alarms by writing to a specific register.
- `servo_on(self)`: Turns the servo on by writing to a specific register.
- `home(self)`: Performs a homing operation.
- `is_home_complete(self, dss1_register)`: Checks if the homing operation is complete by reading a register.
- `move_to_position_number(self, position_number)`: Moves to a specified position number and waits for the move to complete.

The main loop continuously moves between position numbers 2 and 1 until the 'q' key is pressed.


## License

This project is licensed under the MIT License. 

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your improvements.

## Contact

For any questions or feedback, please open an issue or contact [seonghun.choe](mailto:seonghun.choe@tomomi-research.com).




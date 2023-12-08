import atexit
import serial
import serial.tools.list_ports
import json
import time

delimiter = ","
data = []
is_starting_bundle = True


def getPorts():
    all_ports = []
    current_ports = list(serial.tools.list_ports.comports())
    for p in current_ports:
        all_ports.append(p)
    all_ports.sort()
    return all_ports


# close program handler
def exit_handler():
    print("\n\n*** Exiting program, flushing data.")
    with open('./data.json', 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == '__main__':
    atexit.register(exit_handler)
    user_choice = -1
    ports = getPorts()
    while user_choice < 0 or user_choice >= len(ports):
        for i in range(len(ports)):
            print(i, ") ", ports[i])

        user_choice = int(input("Select a port: "))
        if user_choice < 0 or user_choice >= len(ports):
            print("not a valid choice.")

    port = ports[user_choice]
    print("beginning serial connection on ", port)
    ser = serial.Serial(port=f'/dev/{ports[user_choice].name}', baudrate=115200, bytesize=8, timeout=1,
                        parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)

    while True:
        ports = getPorts()

        # disconnect
        if port not in ports:
            print("disconnected, closing pipe.")
            print(data)
            ser.close()

            with open('./data.json', 'w') as file:
                json.dump(data, file, indent=4)

            exit(0)

        if ser.in_waiting:
            message = ser.readline().decode('ascii').split("\r", 1)[0]
            cur_data = message.split(delimiter)
            if cur_data[0] == 'for_py':
                cur_data = [str(time.time())] + cur_data[1:] + ['start' if is_starting_bundle else 'middle']
                data.append(cur_data)
                print(cur_data)
                is_starting_bundle = False
            elif cur_data[0] == 'bundle':
                is_starting_bundle = True


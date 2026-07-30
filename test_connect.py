# from pymodbus.client.sync import ModbusTcpClient

# # Modbus TCP server address and port
# server_ip = "192.168.2.20"
# server_port = 502

# # Create Modbus TCP client
# client = ModbusTcpClient(server_ip, port=server_port,timeout=3.0)

# # Connect to the Modbus TCP server
# connection = client.connect()

# # Check if the connection to the Modbus server was successful
# if not connection:
#     print(f"Unable to connect to Modbus server at {server_ip}:{server_port}")
# else:
#     try:
#         # Modbus function code for reading holding registers is 0x03
#         # Define the Modbus address (starting address) and the number of registers to read
#         modbus_address = 401  # Starting address
#         num_registers = 10  # Number of registers to read

#         # Perform the Modbus read operation
#         result = client.read_holding_registers(modbus_address, num_registers, unit=1)

#         # Check if the read operation was successful
#         if not result.isError():
#             # Extract the values from the result
#             values = result.registers

#             # Print the values
#             print(f"Read successful. Values: {values}")
#         else:
#             print(f"Error reading holding registers: {result}")
#     finally:
#         # Close the Modbus TCP connection
#         client.close()

{
  "type": "call_box",
  "registers": [
    {
      "name": "button_1",
      "addr": 15
    },
    {
      "name": "b1_id",
      "addr": 16
    },
    {
      "name": "fb1",
      "addr": 17
    },
    {
      "name": "button_2",
      "addr": 11
    },
    {
      "name": "b2_id",
      "addr": 12
    },
    {
      "name": "fb2",
      "addr": 13
    },
    {
      "name": "button_3",
      "addr": 18
    },
    {
      "name": "b3_id",
      "addr": 19
    },
    {
      "name": "fb3",
      "addr": 20
    },
    {
      "name": "button_4",
      "addr": 21
    },
    {
      "name": "b4_id",
      "addr": 22
    },
    {
      "name": "fb4",
      "addr": 40
    },
    {
      "name": "button_5",
      "addr": 23
    },
    {
      "name": "b5_id",
      "addr": 24
    },
    {
      "name": "fb5",
      "addr": 41
    },
    {
      "name": "button_6",
      "addr": 25
    },
    {
      "name": "b6_id",
      "addr": 26
    },
    {
      "name": "fb6",
      "addr": 43
    }
  ],
  "protocol": {
"ip": "172.21.99.220",
"port": 3000,
"plc_series": "Q",
"comm_type": "binary"
},
  "device": {
        "max_retry": 2,
        "enable": true,
        "server_ip": "172.21.99.22",
        "server_port": 8080,
        "username": "admin",
        "password": "admin",
        "uptime_send_time": 10,
        "timeout_call_api": 5,
        "timeout_when_disconnect": 15,
        "number_of_button": 6,
        "auto_feedback": false
      },
  "protocol_type": "mc_protocol",
  "name": "line tu dong"
}

import pymcprotocol

#If you use Q series PLC
pymc3e = pymcprotocol.Type3E()
pymc3e.setaccessopt(commtype="binary")
pymc3e.connect("172.21.99.220", 3000)
wordunits_values = pymc3e.batchread_wordunits(headdevice="D15", readsize=1)
print(wordunits_values)
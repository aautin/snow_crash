try:
    with open('token', 'rb') as file:
        file_bytes = file.read()    

    byte_values = list(file_bytes)
    print(f"byte_values: {byte_values}")
    if byte_values[-1] == 10: byte_values = byte_values[:-1]

    new_token = str()
    for i in range(len(byte_values)):
        decoded_byte = (byte_values[i] - i) % 256
        new_token += chr(decoded_byte)
        print(f"{i}: {byte_values[i]} - {i} = {decoded_byte} ('{chr(decoded_byte)}')")

    print(f"Decoded token: {new_token}")

except Exception as e:
    print(f"Error: {e}")
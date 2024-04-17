def IntGenerator(data):
    ind = 0
    sum = 0
    for byte in data:
        if ind == 4:
            yield sum
            ind = 0
            sum = 0
        sum = sum * 256 + byte
        ind += 1
    yield sum
    return

def Calculate(data):
    checksum = 0
    for byte in IntGenerator(data):
        checksum += byte
    value =  (~(checksum & 0xffffffff))
    if value < 0:
        value += 2 ** (4 * 8)
    return value.to_bytes(4, 'little')

def Verify(data: bytes, checksum: bytes):
    calculated_checksum = 0
    for byte in IntGenerator(data):
        calculated_checksum += byte
    calculated_checksum &= 0xffffffff  # Оставляем только младший байт
    calculated_checksum = (~(calculated_checksum & 0xffffffff))
    if calculated_checksum < 0:
        calculated_checksum += 2 ** (4 * 8)

    return calculated_checksum.to_bytes(4, 'little') == checksum

def CreatePacket(data):
    data = len(data).to_bytes(4, 'little') + data
    data = Calculate(data) + data
    return data

def ValidatePacket(data):
    checksum = data[0: 4]
    length = data[4: 8]
    data = data[4: ]
    return len(data) - 4 == int.from_bytes(length, 'little') and Verify(data, checksum)

def GetData(data):
    return data[8:]


size = 1024
with open('text_1.txt', 'rb') as file:
    data = file.read(size)

    pkg = CreatePacket(data)
    print(ValidatePacket(pkg))
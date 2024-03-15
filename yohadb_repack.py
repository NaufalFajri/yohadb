import os
import json
import msgpack
import lz4.block
import struct
# THIS THING NEED CLEAN UP, PLS SOMEONE HELP THIS
def compress_data(data):
    compressed_data = lz4.block.compress(data)
    return compressed_data

def pack_json_to_msgpack(json_data):
    return msgpack.packb(json_data)

def swap_endianness(data):
    # Convert data to bytearray to allow in-place modification
    data_bytes = bytearray(data)
    # Swap endianness for the first 4 bytes
    data_bytes[:4] = struct.pack('<I', struct.unpack('>I', data_bytes[:4])[0])
    return bytes(data_bytes)

def process_json_file(file_path):
    with open(file_path, 'r') as json_file:
        json_data = json.load(json_file)
        if json_data == []:
            # If the JSON data is an empty array, replace it with the MessagePack representation of nil
            return b'\x90', 1  # Represents nil in MessagePack
        else:
            msgpack_data = pack_json_to_msgpack(json_data)
            compressed_data = compress_data(msgpack_data)
            compressed_length = len(compressed_data)
            if compressed_length <= 0xFF:
                header = b'\xc7' + struct.pack('>B', compressed_length + 1) + b'\x63\xd2'
            elif compressed_length <= 0xFFFF:
                header = b'\xc8' + struct.pack('>H', compressed_length + 1) + b'\x63\xd2'
            elif compressed_length <= 0xFFFFFFFF:
                header = b'\xc9' + struct.pack('>I', compressed_length + 1) + b'\x63\xd2'
            else:
                # For larger lengths, raise an error
                raise ValueError("Compressed data length is too large to handle")
            # Swap endianness for the first 4 bytes of the header
            compressed_data = swap_endianness(compressed_data)
            return header + compressed_data, len(header) + compressed_length
def combine_to_file(output_file, data_dict):
    with open(output_file, 'wb') as f:
        metadata = {}
        start_byte = 0
        for filename, (data, length) in data_dict.items():
            f.write(data)
            metadata[filename[:-5]] = [start_byte, length] #removing .json
            start_byte += length
        
        with open("temp2.json", "wb") as metadata_file:
            metadata_packed = msgpack.packb(metadata)
            metadata_file.write(metadata_packed)
            
        #with open("test_uncom.json", "w") as metadata_file333:
            #json.dump(metadata, metadata_file333)
            
import os

def main():
    folder_path = "masterdata_unpacked"  # Specify your folder path containing JSON files
    output_file = "temp1.bin"
    metadata_file = "temp2.json"
    combined_output_file = "combined_file.bin"

    compressed_data_dict = {}

    # Process each JSON file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            compressed_data, length = process_json_file(file_path)
            compressed_data_dict[filename] = (compressed_data, length)

    # Combine compressed data into output file
    combine_to_file(output_file, compressed_data_dict)

    # Read contents of metadata file
    with open(metadata_file, 'rb') as meta_file:
        metadata_content = meta_file.read()

    # Read contents of compressed data file
    with open(output_file, 'rb') as data_file:
        data_content = data_file.read()

    # Combine metadata and compressed data into a single file
    combined_data_array = metadata_content + data_content

    # Write the combined data array to a new file
    with open(combined_output_file, 'wb') as combined_file:
        combined_file.write(combined_data_array)

    if os.path.exists(output_file):
        os.remove(output_file)
    if os.path.exists(metadata_file):
        os.remove(metadata_file)
    print("Combined file created:", combined_output_file)

if __name__ == "__main__":
    main()
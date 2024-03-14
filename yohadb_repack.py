import os
import json
import msgpack
import lz4.block

def compress_data(data):
    compressed_data = lz4.block.compress(data)
    return compressed_data

def pack_json_to_msgpack(json_data):
    return msgpack.packb(json_data)

def process_json_file(file_path):
    with open(file_path, 'r') as json_file:
        json_data = json.load(json_file)
        msgpack_data = pack_json_to_msgpack(json_data)
        compressed_data = compress_data(msgpack_data)
        return compressed_data, len(compressed_data)

def combine_to_file(output_file, data_dict):
    with open(output_file, 'wb') as f:
        metadata = {}
        start_byte = 0
        for filename, (data, length) in data_dict.items():
            f.write(data)
            metadata[filename[:-5]] = [start_byte, length] #removing .json
            start_byte += length
        
        with open("test.json", "wb") as metadata_file:
            metadata_packed = msgpack.packb(metadata)
            metadata_file.write(metadata_packed)

def main():
    folder_path = "masterdata_unpacked"  # Specify your folder path containing JSON files
    output_file = "compressed.bytes"
    compressed_data_dict = {}

    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            compressed_data, length = process_json_file(file_path)
            compressed_data_dict[filename] = (compressed_data, length)

    combine_to_file(output_file, compressed_data_dict)
    print("All JSON files processed and combined into compressed.bin")
    print("Metadata saved to test.json")

if __name__ == "__main__":
    main()

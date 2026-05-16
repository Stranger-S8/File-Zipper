import zlib
import os

class deflate:
    def compress_file(self, input_path, output_path):
        
        file_extension = os.path.splitext(input_path)[1].encode('utf-8')
        print(input_path)
        
        with open(input_path, 'rb') as f:
            data = f.read()

        compressed_data = zlib.compress(file_extension + b'\x00' + data)
        
        with open(output_path, 'wb') as f:
            f.write(compressed_data)
        
        print("Compression Successful")
    

    def decompress_file(self, input_path, output_path):

        with open(input_path, 'rb') as f:
            compressed_data = f.read()
        
        decompressed_data = zlib.decompress(compressed_data)

        file_extension, file_data = decompressed_data.split(b'\x00', 1)
        file_extension = file_extension.decode('utf-8')

        output_path = os.path.splitext(output_path)[0] + file_extension
        
        with open(output_path, 'wb') as f:
            f.write(file_data)
        
        print("Decompression Successful")
        


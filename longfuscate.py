
# Import various modules
import os
import bz2
import time
import gzip
import zlib
import base64
import random
import pathlib

""" Data class """
class Encode:

    """ Encode Constructor """
    def __init__(self) -> None:
        # Define empty variable
        self.blob = None

    """ Decode Object """
    def decode_data(self, data: str) -> str:
        # Encode data object
        return data.decode("utf-8")
    
    """ Encode Object """
    def encode_data(self, data: str) -> bytes:
        # Decode data object
        return data.encode("utf-8")
    
    """ Check if blob contains data """
    def not_empty(self, blob: str) -> bool:
        # Return if data is empty or not
        return False if blob == "" or blob == " " else True

    """ Encode using base64 """
    def base64encode(self, blob: str) -> str:
        self.blob: str = blob
        # Check blob has contents
        if self.not_empty(self.blob.strip()):
            # Encode data and return in "exec" statement
            content = self.decode_data(base64.b64encode(self.encode_data(self.blob)))
            encoded = f"exec(b64decode(\"{content}\"))"

        # Return encoded object
        return encoded
    
    """ Encode using hex """
    def bytes_encode(self, blob: str) -> str:
        self.blob: str = blob
        # Check blob has contents
        if self.not_empty(self.blob.strip()):
            # Encode data and return in "exec" statement
            content = self.encode_data(self.blob).hex()
            encoded = f"exec(bytes.fromhex(\"{content}\").decode(\"utf-8\"))"

        # Return encoded object
        return encoded
    
    """ Compress using gzip """
    def gzip_encode(self, blob: str) -> str:
        self.blob: str = blob
        # Check blob has contents
        if self.not_empty(self.blob.strip()):
            # Compress data and return in "exec" statement
            content = gzip.compress(bytes(self.blob, "utf-8"))
            encoded = f"exec(decompress({content}).decode(\"utf-8\"))"

        # Return encoded object
        return encoded
    
    """ Compress using bzip """
    def bzip_encode(self, blob: str) -> str:
        self.blob: str = blob
        # Check blob has contents
        if self.not_empty(self.blob.strip()):
            # Compress data and return in "exec" statement
            content = bz2.compress(self.encode_data(self.blob), 5)
            encoded = f"exec(bdecompress({content}).decode(\"utf-8\"))"

        # Return encoded object
        return encoded
    
    """ Compress using zlib """
    def zlib_encode(self, blob: str) -> str:
        self.blob: str = blob
        # Check blob has contents
        if self.not_empty(self.blob.strip()):
            # Compress data and return in "exec" statement
            content = zlib.compress(self.encode_data(self.blob), 3)
            encoded = f"exec(zdecompress({content}).decode(\"utf-8\"))"

        # Return encoded object
        return encoded
    
    """ Encode using character codes """
    def charcode_encode(self, blob: str) -> str:
        self.blob: str = blob
        # Check blob has contents
        if self.not_empty(self.blob.strip()):
            # Encode data and return in "exec" statement
            content = " ".join([str(ord(char)) for char in self.blob])
            encoded = f"exec(''.join([chr(int(number)) for number in \"{content}\".split()]))"

        # Return encoded object
        return encoded

""" Main class """
class Longfuscate:

    def __init__(self) -> None:
        # Define empty variables
        self.blob = None
        self.file = None
        self.data = ""
        self.code = None
        self.iter = None

        # Define methods of encoding / compression
        self.methods = ["base64", "hex", "gzip", "bzip", "zlib", "charcode"]

        # Call for encoding constructor
        self.encode_constructor = Encode()

    """ Check if blob contains data """
    def not_empty(self, blob: str) -> bool:
        # Return if data is empty or not
        return False if blob == "" or blob == " " else True
    
    """ Get all the lines of code in the script """
    def get_lines(self, blob: str) -> list:
        # Gets all lines of code
        lines = [line for part in blob.split("\n") for line in part.split(";")]
        # Returns all that are not imports
        return [line for line in lines if (line.strip().startswith("import")) == False and (line.strip().startswith("from") and "import" in line) == False and (self.not_empty(line.strip())) or ("exec" in line.strip()) == True]

    """ Get all the module imports in the script """
    def get_imports(self, blob: str) -> None:
        # Get all lines of code
        lines = [line for part in blob.split("\n") for line in part.split(";")]
        # Store all the lines that are imports
        filtered = [line for line in lines if line.strip().startswith("import") or line.strip().startswith("from") and "import" in line]

        # Loop through imports
        for line in filtered:
            # Check if already imported
            if f"{line};" not in self.data:
                # If not, add import to file
                self.data += f"{line};"

        return

    """ Get a random encoding method """
    def get_random_method(self) -> str:
        # Return random method of encoding
        return random.choice(self.methods)

    """ Main function """
    def longfuscate(self):
        # Clear screen
        os.system("clear" if not "nt" in os.name else "cls")
        # Display unstable version warning
        print("\n   [NOTE] LONGFUSCATE IS IN DEVELOPMENT VERSION v1.0\n   This version is not stable and may contain errors")

        # Get path to file
        while True:
            file: str = str(input("\n   Script Location   :   "))
            # Verify an input was supplied
            if self.not_empty(file):
                # Ensure file exists
                if pathlib.Path(file.strip()).exists():
                    # Store file in variable
                    self.file: str = file.strip()
                    break

        # Get amount of iterations
        while True:
            _iter: int = str(input("   Loop Amount       :   "))
            # Verify an input was supplied
            if self.not_empty(_iter):
                # Make sure input is a digit
                if _iter.isdigit():
                    # Store file in variable
                    self.iter: int = int(_iter)

                    # Display warning if using mass iterations
                    if self.iter >= 20:
                        print("\n   [WARNING] LONGFUSCATE MASS ITERATIONS\n     - Slow execution\n     - Increased file size\n     - Increased time to encode")

                    break

        print("   ")

        # Begin timer
        start_time = time.time()

        # Get script contents
        with open(self.file, "r", encoding="utf-8") as script_file:
            # Read file data
            script_file_data = script_file.read()
            # Make sure data is not empty
            if self.not_empty(script_file_data.strip()):
                # Store file data as variable
                self.blob: str = script_file_data
                # Close file
                script_file.close()

        # Get imports
        self.get_imports(self.blob)
        # Get lines
        self.code: str = "\n".join(self.get_lines(self.blob))

        # Begin iteration
        for i in range(self.iter):
            # Get random method
            method = self.get_random_method()

            # Call base64 encode
            if method.lower() == "base64":
                self.code: str = self.encode_constructor.base64encode(self.code)
                # Add import for base64
                if not "from base64 import b64decode as b64decode;" in self.data:
                    self.data += "from base64 import b64decode as b64decode;"

            # Call hex encode
            elif method.lower() == "hex":
                self.code: str = self.encode_constructor.bytes_encode(self.code)

            # Call gzip compress
            elif method.lower() == "gzip":
                self.code: str = self.encode_constructor.gzip_encode(self.code)
                # Add import for gzip
                if not "from gzip import decompress as decompress;" in self.data:
                    self.data += "from gzip import decompress as decompress;"

            # Call bzip compress
            elif method.lower() == "bzip":
                self.code: str = self.encode_constructor.bzip_encode(self.code)
                # Add import for bzip
                if not "from bz2 import decompress as bdecompress;" in self.data:
                    self.data += "from bz2 import decompress as bdecompress;"

            # Call zlib compress
            elif method.lower() == "zlib":
                self.code: str = self.encode_constructor.zlib_encode(self.code)
                # Add import for zlib
                if not "from zlib import decompress as zdecompress;" in self.data:
                    self.data += "from zlib import decompress as zdecompress;"

            # Call character code encode
            elif method.lower() == "charcode":
                self.code: str = self.encode_constructor.charcode_encode(self.code)

        # Combine code
        self.data += f"{self.code}"

        # Create path to obfuscated file
        pathlib.Path(f"{os.getcwd()}/dist/").mkdir(parents = True, exist_ok = True)
        with open(f"{os.getcwd()}/dist/longfuscated.py", "w", encoding="utf-8") as obfuscated_file:
            # Write obfuscated file contents
            obfuscated_file.write(self.data)
            # Close file
            obfuscated_file.close()

        # End timer
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Display time taken to encode
        print(f"   Operation completed in {round(elapsed_time, 3)} seconds.\n")

if __name__ == "__main__":
    # Get constructor
    constructor = Longfuscate()
    # Call main function
    constructor.longfuscate()

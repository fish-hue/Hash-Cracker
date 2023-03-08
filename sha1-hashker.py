import hashlib
import argparse

# Parse the command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="specify the filename of the rainbow table", required=True)
args = parser.parse_args()

# Load the rainbow table from the specified file
table_file = args.file
table = {}
with open(table_file, "r") as f:
    for line in f:
        end, start = line.strip().split(":")
        table[end] = start

# Prompt the user to enter a hash value
hash_value = input("Enter the hash value to crack: ")

# Check that the input hash value is valid
if len(hash_value) != 40:
    print("Error: Invalid hash value. Please enter a valid SHA-1 hash value.")
else:
    # Look up the hash value in the rainbow table
    plaintext = None
    if hash_value in table:
        plaintext = table[hash_value]
    else:
        chain_length = 1000
        for end, start in table.items():
            if end == hashlib.sha1(start.encode()).hexdigest():
                for i in range(chain_length - 1):
                    start = hashlib.sha1(start.encode()).hexdigest()
                    if hashlib.sha1(start.encode()).hexdigest() == hash_value:
                        plaintext = start
                        break
                if plaintext is not None and hashlib.sha1(plaintext.encode()).hexdigest() != hash_value:
                    plaintext = None
                break

    # Print the plaintext value that corresponds to the input hash value
    if plaintext is not None:
        print(f"The plaintext value for the hash value {hash_value} is {plaintext}")
    else:
        print(f"No match found for the hash value {hash_value}")

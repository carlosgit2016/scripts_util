import bcrypt
import sys

password = str(sys.argv[1]).encode('utf-8') # Convert to bytes

# Generate a salt
salt = bcrypt.gensalt(rounds=12)

# Hash the password
hashed_password = bcrypt.hashpw(password, salt)

print(hashed_password.decode()) # print hashed password as string

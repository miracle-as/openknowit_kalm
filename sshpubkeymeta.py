import re
from datetime import datetime

def extract_expiration_date(public_key_comment):
    expiration_match = re.search(r'expire=(\d{4}-\d{2}-\d{2})', public_key_comment)
    if expiration_match:
        expiration_date_str = expiration_match.group(1)
        expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d')
        return expiration_date
    else:
        return None

# Read the public key from a file
public_key_file = "public_key.pub"
with open(public_key_file, "r") as f:
    public_key_comment = f.read().strip()

# Extract expiration date from the comment
expiration_date = extract_expiration_date(public_key_comment)
if expiration_date:
    print("Expiration Date:", expiration_date.strftime('%Y-%m-%d'))
else:
    print("No expiration date found in the comment.")


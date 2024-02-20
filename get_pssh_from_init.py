import base64

import requests
import xmltodict


def read_pssh_from_bytes(bytes: bytes):
    pssh_offset = bytes.rfind(b"pssh")
    _start = pssh_offset - 4
    _end = pssh_offset - 4 + bytes[pssh_offset - 1]
    pssh = bytes[_start:_end]
    return pssh


url = input("Enter Init segment url: ")
headers = {
    # "Range": "bytes=0-962",
}
print("Downloading...")

res = requests.get(url, headers=headers)
if not res.ok:
    print(f"Could not download init segment: {res.text}")

pssh = read_pssh_from_bytes(res.content)
if pssh is not None:
    print(f"PSSH: {base64.b64encode(pssh).decode('utf8')}")
else:
    print("Failed to extract PSSH!")

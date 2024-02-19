# Script maded by MoiZz
# Added Kid Extracotr by Aiman
# Added OS Select options by Phantom


import os
import subprocess
import re
import base64
import urllib.request
import binascii
from urllib.error import HTTPError

def get_pssh(keyId):
    array_of_bytes = bytearray(b'\x00\x00\x002pssh\x00\x00\x00\x00')
    array_of_bytes.extend(bytes.fromhex("edef8ba979d64acea3c827dcd51d21ed"))
    array_of_bytes.extend(b'\x00\x00\x00\x12\x12\x10')
    array_of_bytes.extend(bytes.fromhex(keyId.replace("KID =", "").strip()))
    return base64.b64encode(bytes.fromhex(array_of_bytes.hex()))

def return_pssh(kid):
    kid = kid.replace('KID =', '').strip()
    return "PSSH = {}".format(get_pssh(kid).decode('utf-8'))

def print_color(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m", end="", flush=True)

def get_pssh_from_url(url, os_choice):
    mpd_headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    if url == "":
        print_color("URL input aborted. Exiting...", "91")
        return

    try:
        pssh_list = []
        mpd_data = urllib.request.urlopen(url).read().decode('utf-8')
        baseurl = url.rstrip("/") + "/"
        psshs = re.findall(">([\S]+)</(?:cenc:)?pssh", mpd_data)
        if psshs:
            for pssh in psshs:
                pesx = binascii.hexlify(base64.b64decode(pssh)).decode('utf-8')
                if "edef8ba9" in pesx:
                    if pssh not in pssh_list:
                        pssh_list.append(pssh)

        if pssh_list:
            print_color("PSSH = ", "92")
            print_color(" ".join(pssh_list), "92")
            start_over()
            return

        print_color("No PSSH found. Calculating the PSSH, please wait.\n", "91")

        subprocess.run(['yt-dlp', '--allow-u', '--no-progress', '--console-title', url],
                       stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        for file in os.listdir():
            if file.endswith('.mp4') and file != 'test.mp4':
                os.rename(file, 'test.mp4')
                break

        kid = None
        dump_tool = 'mp4dump.exe' if os_choice == '1' else 'mp4dump'
        dump_output = subprocess.run([dump_tool, 'test.mp4'], capture_output=True, text=True).stdout
        for line in dump_output.split('\n'):
            if 'KID' in line:
                kid = re.search(r'\[(.*?)\]', line)
                if kid:
                    kid = kid.group(1)
                    print_color("KID = " + kid, "93")  # Принтира KID с жълт цвят (код 93)
                break

        if kid:
            pssh_result = return_pssh(kid)
            if pssh_result:
                print_color(pssh_result, "92")
                start_over()
        else:
            print("\nMPD doesn't have a KID.")

        for file in os.listdir():
            if file.endswith('.m4a') or file == 'test.mp4':
                os.remove(file)

    except HTTPError as e:
        print_color("Failed to fetch the MPD data. Please check the URL and try again.", "91")
        print("\n", end="")
        print_color(str(e), "91")
        start_over()

    except ValueError as e:
        if "unknown url type" in str(e):
            print_color("Invalid URL format. Please enter a valid URL.", "91")
            start_over()
        else:
            raise e

def enter_url(os_choice):
    url = input("Enter the URL (or leave empty to abort): ")
    if url:
        get_pssh_from_url(url, os_choice)
    else:
        print_color("URL input aborted. Exiting...", "91")

def start_over():
    os_choice = input("\nChoose your operating system: \n1. Windows \n2. Linux \nYour choice: ")
    if os_choice in ['1', '2']:
        enter_url(os_choice)
    else:
        print("Invalid choice. Exiting...")


if os.path.exists('test.mp4'):
    os.remove('test.mp4')

start_over()

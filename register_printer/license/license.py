import platform
import psutil
import hashlib
from pathlib import Path
from .key import key

class LicenseException(Exception):
    pass

def find_addr():
    a = psutil.net_if_addrs()
    result = None
    found = False
    for q in a:
        for t in a[q]:
            if t.family == psutil.AF_LINK:
                result = t.address
                found = True
                break
        if found:
            break
    return result

def get_unique_id():
    t = find_addr()
    t = platform.node() + platform.processor()
    b = t.encode()
    m = hashlib.sha256()
    m.update(b)
    z = m.hexdigest()
    return z

def generate_license(my_id):
    m = hashlib.sha512()
    b = my_id.encode()
    m.update(b)
    m.update(key.encode())
    c = m.hexdigest()
    return c

def is_valid_license(my_id, my_license):
    m = hashlib.sha512()
    b = my_id.encode()
    m.update(b)
    m.update(key.encode())
    c = m.hexdigest()
    if c == my_license:
        return True
    else:
        return False

def check_license():
    home_path = Path.home()
    license_file = home_path.joinpath("RegisterPrinterLicense.txt")
    unique_id = get_unique_id()
    if not license_file.exists():
        msg = "No license file(" + str(license_file) + ") found.\n"
        msg += "Please generate license using ID: " + unique_id
        raise LicenseException(msg)

    license_content = None
    with license_file.open() as f:
        license_content = f.readline().strip()

    if not is_valid_license(unique_id, license_content):
        msg = "License file(" + str(license_file) + ") is invalid.\n"
        msg += "Please generate license using ID: " + unique_id
        raise LicenseException(msg)
    return
    

from register_printer.license import (
    generate_license)

unique_id = input("Please input your ID: ")
license_content = generate_license(unique_id.strip())
with open("RegisterPrinterLicense.txt", "w") as f:
    f.write(license_content)

    

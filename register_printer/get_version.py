import pkgutil


def get_version():
    version_bin = pkgutil.get_data("register_printer", "VERSION")
    version_str = version_bin.decode('UTF-8')
    version_str = version_str.strip()
    return version_str

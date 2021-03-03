import logging
from register_printer.__main__ import main


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(module)s %(message)s')

main()

import logging
import sys

#log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_formatter = logging.Formatter('%(message)s')
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setLevel(logging.DEBUG)
log_handler.setFormatter(log_formatter)

log = logging.getLogger()
log.setLevel(logging.DEBUG)
log.addHandler(log_handler)

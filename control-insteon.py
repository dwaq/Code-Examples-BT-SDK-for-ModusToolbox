#!python
import time,requests,sys
import pprint
from insteonlocal.Hub import Hub
import config
import logging
from sys import stdout

## To begin, create a file called config.py containing:
#host = "hub's ip"
#username = "hub's username"
#password = "hub's password"
# or comment out the import config and manually specify below

try:
    FORMAT = '[%(asctime)s] (%(filename)s:%(lineno)s) %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG, filename='insteon.log')
    #logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    logger = logging.getLogger('')

    # create hub object
    hub = Hub(
        config.host,
        config.username, 
        config.password, 
        '25105', #port 
        10, #timeout
        logger
    )
    buffer = hub.get_buffer_status()
except requests.exceptions.RequestException as e:
   if hub.http_code == 401:
       print("Unauthorized...check user/pass for hub\n")
       sys.exit(1)
   else:
       print(e)
       sys.exit(1)

dimmer1 = hub.dimmer('502739')

# set to argument if included
if(len(sys.argv)==2):
    dimmer1.on(sys.argv[1])
# otherwise turn off    
else:    
    dimmer1.on(0)
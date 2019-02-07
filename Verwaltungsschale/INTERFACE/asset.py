import json
from random import randint
import time

from FUNCTIONALITY.configuration import config
from FUNCTIONALITY.module import module


def main():

    interface = module('INTERFACE', config)
    count = 0
    response ="0"

    while True:
        try:
            sockets = dict(interface.poller.poll(10))
            if interface.socket in sockets:

                MESSAGE = interface.receive()
                CORE = interface.extract_core(MESSAGE)


                request = CORE["request"]


                RESPONSE = interface.create_message(TO = MESSAGE, CORE = {"current position" : response, "current loop": count})
                interface.send(RESPONSE)


            count += 1
            response = "{}°".format(randint(0,360))




        except KeyboardInterrupt:
            break



if __name__ == "__main__":
    main()

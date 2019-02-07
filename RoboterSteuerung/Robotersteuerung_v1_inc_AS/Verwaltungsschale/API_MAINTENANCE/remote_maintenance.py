import json

from structure.configuration import config
from structure.module import module



def main():

    remote_maintenance = module('API_MAINTENANCE', config)


    while True:
        try:

            MESSAGE = remote_maintenance.receive()
            CORE = remote_maintenance.extract_core(MESSAGE)


            request = CORE["request"]

            if request == "run maintenance protocol A1":

                response = "the maintenance protocol was successfully completed"

            elif request == "run maintenance protocol C3":

                REQUEST = remote_maintenance.create_message(TO = 'DATABASE', CORE = {"request":"school"})
                remote_maintenance.send(REQUEST)

                MESSAGE_2 = remote_maintenance.receive()

                response = remote_maintenance.extract_core(MESSAGE_2)


            RESPONSE = remote_maintenance.create_message(TO = MESSAGE, CORE = {request : response})
            remote_maintenance.send(RESPONSE)


        except KeyboardInterrupt:
            break





if __name__ == "__main__":
    main()

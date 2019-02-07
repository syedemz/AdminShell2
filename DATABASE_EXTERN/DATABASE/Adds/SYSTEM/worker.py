import json

from FUNCTIONALITY.configuration import config
from FUNCTIONALITY.module import module

from FUNCTIONALITY.system import sys_function_A
from FUNCTIONALITY.system import sys_function_B
from FUNCTIONALITY.system import sys_function_C

def main():

    system = module('SYSTEM', config)


    while True:
        try:

            MESSAGE = system.receive()
            CORE = system.extract_core(MESSAGE)


            request = CORE["request"]
            if request == 'A':
                sys_function_A.main()
            elif request == 'B':
                sys_function_B.main()
            elif request == 'C':
                sys_function_C.main()

            response = "function has been executed"


            RESPONSE = system.create_message(TO = MESSAGE, CORE = {request : response})
            system.send(RESPONSE)


        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()

import json

from structure.configuration import config
from structure.module import module

from SYSTEM import sys_function_A
from SYSTEM import sys_function_B
from SYSTEM import sys_function_C



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

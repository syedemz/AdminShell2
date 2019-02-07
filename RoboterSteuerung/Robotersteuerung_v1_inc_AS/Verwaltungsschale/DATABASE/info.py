import json
import pandas

from structure.configuration import config
from structure.module import module



def main():

    database = module('DATABASE', config)

    db_pandas = pandas.read_csv("database/data.csv")


    while True:
        try:

            MESSAGE = database.receive()
            CORE = database.extract_core(MESSAGE)


            request = CORE["request"]
            response = db_pandas[request].to_dict()
            for key in response:
                response = str(response)


            RESPONSE = database.create_message(TO = MESSAGE, CORE = {request : response})
            database.send(RESPONSE)


        except KeyboardInterrupt:
            break





if __name__ == "__main__":
    main()

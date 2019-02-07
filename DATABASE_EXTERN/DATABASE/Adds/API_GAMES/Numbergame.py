import os
import sys

curdir = os.path.abspath(os.path.dirname(__file__))
topdir = os.path.abspath(os.path.join(curdir, os.pardir, os.pardir))
if topdir not in sys.path:
	sys.path.insert(0, topdir)

from FUNCTIONALITY.configuration import config
from FUNCTIONALITY.module import module
import random

def main():

    api_games = module("API_GAMES", config)
    unknown_number = str(random.randint(1000,9999))

    while True:
        try:

            MESSAGE = api_games.receive()
            CORE = api_games.extract_core(MESSAGE)

            number = CORE["number"]

            if number == unknown_number:
                response = "Richtig geraten!"
                zusatz = "Voll einfach!"
                unknown_number = str(random.randint(1000,9999))
                
            else:
                response = "Raten sie erneut!"
                if int(number) < int(unknown_number):
                    zusatz = "Versuchen Sie eine größere Zahl!"
                elif int(number) > int(unknown_number):
                    zusatz = "Versuchen Sie eine kleinere Zahl!"

            RESPONSE = api_games.create_message(TO = MESSAGE, CORE = {"Antwort" : response, "Zusatz": zusatz})
            api_games.send(RESPONSE)

        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()

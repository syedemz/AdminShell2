from structure.configuration import config
from structure.broker import broker



def main():

    control = broker(config)
    control.mediate()



if __name__ == '__main__':
    main()

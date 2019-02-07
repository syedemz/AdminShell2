from os import path, pardir, system
from time import sleep
import sys
"""The path to the administration (Verwaltungsschale - level) has to be set in
sys.path once, so the packages can be found.
"""
curdir = path.abspath(path.dirname(__file__))
topdir = path.abspath(path.join(curdir, pardir))
if topdir not in sys.path:
	sys.path.insert(0, topdir)

from broker import broker
from FUNCTIONALITY.configuration import config


def main():

	control = broker(config)
	control.mediate()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import os

OHD_ROOT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
OHD_DIR = os.path.join(OHD_ROOT_PATH, "open_hardware_definitions")
PARSER_DIR = os.path.join(OHD_ROOT_PATH, "parsers")
DATASHEET_DIR = os.path.join(PARSER_DIR, "datasheets")
DEFINITIONS_DIR = os.path.join(OHD_DIR, "definitions")
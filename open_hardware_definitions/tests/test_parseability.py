#!/usr/bin/env python3

import glob
from open_hardware_definitions import Device
from open_hardware_definitions.common import DEFINITIONS_DIR

def test_parseability():
  # Discover all yaml files
  passed = True
  for definition in glob.glob(f"{DEFINITIONS_DIR}/**/*.yaml"):
    print(f"Testing {definition.replace(DEFINITIONS_DIR + '/', '')}... ", end='')

    try:
      Device.load_file(definition)
      print('OK')
    except Exception:
      print('Failed!')
      passed = False

  if not passed:
    raise Exception("Not all definitions are parseable!")

if __name__ == "__main__":
  test_parseability()
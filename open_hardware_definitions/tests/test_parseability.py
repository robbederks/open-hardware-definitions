#!/usr/bin/env python3

import glob
import tqdm
import multiprocessing
from open_hardware_definitions import Device
from open_hardware_definitions.common import DEFINITIONS_DIR

def _test(path):
  try:
    Device.load_file(path)
    return True
  except Exception:
    print(f"Testing {path.replace(DEFINITIONS_DIR + '/', '')} failed!")
    return False

def test_parseability():
  with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
    # Discover all yaml files
    files = glob.glob(f"{DEFINITIONS_DIR}/**/*.yaml")
    if not all(tqdm.tqdm(pool.imap(_test, files), total=len(files))):
      raise Exception("Not all definitions are parseable!")

if __name__ == "__main__":
  test_parseability()
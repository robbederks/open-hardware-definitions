#!/usr/bin/env python3

import os
import glob
import tqdm
import multiprocessing

from open_hardware_definitions.common import DEFINITIONS_DIR
from open_hardware_definitions.tests.test_compliance import _test

def cleanup_non_compliant():
  with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
    # Discover all yaml files
    files = glob.glob(f"{DEFINITIONS_DIR}/**/*.yaml")
    results = list(tqdm.tqdm(pool.imap(_test, files), total=len(files)))

  for path, compliant in results:
    if not compliant:
      print("Deleting", path)
      os.remove(path)

if __name__ == "__main__":
  cleanup_non_compliant()
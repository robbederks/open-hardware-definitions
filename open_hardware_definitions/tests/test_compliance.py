#!/usr/bin/env python3

import glob
import tqdm
import multiprocessing
from open_hardware_definitions import Device
from open_hardware_definitions.common import DEFINITIONS_DIR

def _test(path):
  try:
    # Check if it's parseable
    try:
      dev = Device.load_file(path)
    except Exception as e:
      raise Exception("Unable to parse!") from e

    # Check if any regions overlap
    if hasattr(dev, 'regions'):
      for i, r in enumerate(dev.regions):
        for j, r2 in enumerate(dev.regions):
          if i == j:
            continue

          if max(r.base_addr, r2.base_addr) < min(r.base_addr + r.size, r2.base_addr + r2.size):
            raise Exception(f"Regions '{r.name}' and '{r2.name}' overlap!")

    # Check if there are any modules which overlap
    if hasattr(dev, 'modules'):
      for i, m in enumerate(dev.modules):
        for j, m2 in enumerate(dev.modules):
          if i == j:
            continue

          if max(m.base_addr, m2.base_addr) < min(m.base_addr + m.get_size(), m2.base_addr + m2.get_size()):
            print(hex(m.base_addr), hex(m.get_size()), hex(m2.base_addr), hex(m2.get_size()))
            raise Exception(f"Modules '{m.name}' and '{m2.name}' overlap!")


    return (path, True)
  except Exception as e:
    print(f"Testing {path.replace(DEFINITIONS_DIR + '/', '')} failed!: {str(e)}")
    return (path, False)

def test_compliance():
  with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
    # Discover all yaml files
    files = glob.glob(f"{DEFINITIONS_DIR}/**/*.yaml")
    if not all(map(lambda r: r[1], tqdm.tqdm(pool.imap(_test, files), total=len(files)))):
      raise Exception("Not all definitions passed!")

if __name__ == "__main__":
  test_compliance()
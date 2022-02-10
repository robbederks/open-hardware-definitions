#!/usr/bin/env python3

import os
import glob
from convert import convert

from open_hardware_definitions.common import DEFINITIONS_DIR, PARSER_DIR

SVD_DIR = f"{PARSER_DIR}/svd/cmsis-svd/data"

# TODO: parallelize

for fn in glob.glob(f"{SVD_DIR}/**/*.svd"):
  base_name = fn.replace(SVD_DIR + '/', '').replace('.svd', '')

  if "ARM_SAMPLE" not in base_name:
    try:
      print(f"Converting {base_name}... ", end='')

      ohd = convert(fn)

      output_path = f"{DEFINITIONS_DIR}/{base_name}.yaml"
      os.makedirs(os.path.dirname(output_path), exist_ok=True)
      with open(output_path, 'w') as f:
        f.write(ohd.dump())

      print("OK!")
    except Exception as e:
      print("FAILED! Reason:", e)

print("Done!")

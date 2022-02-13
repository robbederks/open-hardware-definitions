#!/usr/bin/env python3

import os
import glob
import tqdm
import multiprocessing
from convert import convert

from open_hardware_definitions.common import DEFINITIONS_DIR, PARSER_DIR

SVD_DIR = f"{PARSER_DIR}/svd/cmsis-svd/data"

def _convert(fn):
  base_name = fn.replace(SVD_DIR + '/', '').replace('.svd', '')

  if "ARM_SAMPLE" not in base_name:
    try:
      ohd = convert(fn)

      output_path = f"{DEFINITIONS_DIR}/{base_name}.yaml"
      os.makedirs(os.path.dirname(output_path), exist_ok=True)
      with open(output_path, 'w') as f:
        f.write(ohd.dump())
    except Exception as e:
      print(f"Converting {base_name} FAILED! Reason:", e)


with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
  files = glob.glob(f"{SVD_DIR}/**/*.svd")
  list(tqdm.tqdm(pool.imap(_convert, files), total=len(files)))

print("Done!")

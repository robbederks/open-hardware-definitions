#!/usr/bin/env python3

# This loader is inspired by https://github.com/leveldown-security/SVD-Loader-Ghidra/blob/master/SVD-Loader.py

import os
import math
import argparse
import ghidra_bridge

from open_hardware_definitions import Device
from open_hardware_definitions.common import DEFINITIONS_DIR

def load_ohd(dev):
  # Connect to Ghidra
  with ghidra_bridge.GhidraBridge(interactive_mode=True) as bridge:
    ghidra = bridge.get_ghidra_api()
    api = bridge.get_flat_api()

    # Get program objects
    program = api.getState().getCurrentProgram()
    listing = program.getListing()
    address_space = program.getAddressFactory().getDefaultAddressSpace()
    symbol_table = program.getSymbolTable()

    # Data types for bit sizes
    DATA_TYPES = {
      8: ghidra.program.model.data.ByteDataType,
      16: ghidra.program.model.data.UnsignedShortDataType,
      32: ghidra.program.model.data.UnsignedIntegerDataType,
      64: ghidra.program.model.data.UnsignedLongLongDataType,
    }

    # TODO: fix this in a good way
    # If regions exist, create the region memory map.
    # First, we delete all the blocks which overlap
    # if len(dev.regions) > 0:
    #   def overlap(start1, len1, start2, len2):
    #     return max(start1, start2) < min(start1 + len1, start2 + len2)

    #   print(dir(program.memory))
    #   to_delete = []
    #   for block in program.memory.getBlocks():
    #     for region in dev.regions:
    #       if overlap(block.start.getOffset(), block.size, region.base_addr, region.size):
    #         to_delete.append(block)
    #         print("deleting", block.name, block.start)
    #         break

    #   for block in to_delete:
    #     program.memory.removeBlock(block)

    # Add a block for the modules
    # TODO: remove / change blocks if it exists
    for module in dev.modules:
      min_addr = module.base_addr
      max_addr = 0

      if hasattr(module, "registers"):
        for register in module.registers:
          if min_addr == None:
            min_addr = register.addr
          min_addr = min(min_addr, register.addr)
          max_addr = max(max_addr, register.addr + (math.ceil(dev.bit_width / 8)))

      if max_addr == 0 and hasattr(module, "size"):
        max_addr = module.base_addr + module.size

      try:
        mod_block = program.memory.createUninitializedBlock(module.name, address_space.getAddress(min_addr), max_addr - min_addr, False)
        mod_block.setRead(True)
        mod_block.setWrite(True)
        mod_block.setExecute(False)
        mod_block.setVolatile(True)
        if hasattr(module, "description"):
          mod_block.setComment(module.description)
        print(f"Added a module region \"{module.name}\" from {hex(min_addr)} to {hex(max_addr)}")
      except Exception:
        print(f"Adding a module region \"{module.name}\" from {hex(min_addr)} to {hex(max_addr)} FAILED! Already existing?")

    # Add all the registers
    for module in dev.modules:
      # Create Module namespace it it doesn't exist
      namespace = symbol_table.getNamespace(module.name, None)
      if not namespace:
        namespace_name = module.name.strip().replace(' ', '_')
        print(f"Creating '{namespace_name}' namespace")
        namespace = symbol_table.createNameSpace(None, namespace_name, ghidra.program.model.symbol.SourceType.IMPORTED)

      if not hasattr(module, "registers"):
        continue

      print(f"Adding registers for module '{module.name}'...")
      for register in module.registers:
        addr = address_space.getAddress(register.addr)
        data_type = DATA_TYPES[register.size_bits if hasattr(register, 'size_bits') else dev.bit_width]
        try:
          if not listing.getDataAt(addr).isDefined():
            listing.createData(addr, data_type())
          reg_name = register.name.strip().replace(' ', '_')
          symbol_table.createLabel(addr, reg_name, namespace, ghidra.program.model.symbol.SourceType.IMPORTED)
          print(f"- Added '{reg_name}' at {hex(register.addr)}")
        except Exception as e:
          print(f"- Adding register '{reg_name}' at {hex(register.addr)} FAILED!", str(e))



def ohd_file_parser(val):
  value = val.strip()
  if not value.endswith('.yaml'):
    value += '.yaml'

  if not os.path.isfile(value):
    value = os.path.join(DEFINITIONS_DIR, value)
    if not os.path.isfile(value):
      raise Exception(f"No definition file found matching '{val}'")
  value = os.path.abspath(value)

  print("Loading", value)
  return Device.load_file(value)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Load an OHD file into Ghidra over ghidra-loader")
  parser.add_argument('ohd_definition', type=ohd_file_parser, help="OHD definition (absolute file path)")
  args = parser.parse_args()

  load_ohd(args.ohd_definition)

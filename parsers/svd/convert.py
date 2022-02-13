#!/usr/bin/env python

import sys
import math

# TODO: remove hack
sys.path.append("/home/robbe/open-hardware-definitions/parsers/svd/cmsis-svd/python")
from cmsis_svd.parser import SVDParser

from open_hardware_definitions import Device, Module, Register, Field
from open_hardware_definitions.helpers import HexInt

def convert(svd_dev_path):
  svd_dev = SVDParser.for_xml_file(svd_dev_path).get_device()

  dev = Device(
    manufacturer=svd_dev.vendor,
    part_number=svd_dev.name,
    bit_width=svd_dev.width,
    endianness=svd_dev.cpu.endian,
    architecture="ARM Cortex-M",
  )

  register_set = set()

  for per in svd_dev.peripherals:
    mod = Module(
      name=per.name,
      base_addr=per.base_address,
      description=per.description,
    )

    max_addr = per.base_address
    for reg in per.registers:
      fields = []
      for f in reg.fields:
        # TODO: do we want descriptions here too?
        evs = {}
        if f.enumerated_values:
          for ev in f.enumerated_values:
            evs[ev.value] = ev.name

        fields.append(Field(
          name=f.name,
          bit_offset=f.bit_offset,
          bit_width=f.bit_width,
          description=f.description,
          read_allowed=('read' in f.access if f.access else None),
          write_allowed=('write' in f.access if f.access else None),
          enum_values=evs if len(evs.keys()) > 0 else None
        ))

      size = reg.size if reg.size else svd_dev.width
      byte_size = math.ceil(size/8)
      max_addr = max(max_addr, per.base_address + reg.address_offset + byte_size)
      addr = per.base_address + reg.address_offset

      # This is needed to clean up multiple register definitions for a single address.
      # Seems like SVDs are a big fan of this, I don't like it...
      if not any(map(lambda a: a in register_set, range(addr, addr + byte_size))):
        mod.registers.append(Register(
          name=reg.name,
          addr=addr,
          size_bits=size,
          description=reg.description,
          read_allowed=('read' in reg.access if reg.access else None),
          write_allowed=('write' in reg.access if reg.access else None),
          reset_value=reg.reset_value,
          fields=fields
        ))

        for a in range(addr, addr + byte_size):
          register_set.add(a)

    mod.size = HexInt(max_addr - per.base_address)
    dev.modules.append(mod)

  return dev

if __name__ == "__main__":
  # Convert!
  dev = convert(sys.argv[1])

  # Dump out!
  print(dev.dump())

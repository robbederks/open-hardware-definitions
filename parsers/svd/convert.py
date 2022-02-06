#!/usr/bin/env python

import sys

# TODO: remove hack
sys.path.append("/home/robbe/open-hardware-definitions/parsers/svd/cmsis-svd/python")
from cmsis_svd.parser import SVDParser

from open_hardware_definitions import Device, Module, Register

def convert(svd_dev):
  dev = Device(
    manufacturer=svd_dev.vendor,
    part_number=svd_dev.name,
    bit_width=svd_dev.width,
    endianness=svd_dev.cpu.endian,
  )

  for per in svd_dev.peripherals:
    mod = Module(
      name=per.name,
      base_addr=per.base_address,
      size=per.address_block.size,
      description=per.description,
    )

    for reg in per.registers:
      mod.registers.append(Register(
        name=reg.name,
        addr=reg.address_offset,
        size_bits=reg.size,
        description=reg.description,
        read_allowed=('read' in reg.access if reg.access else None),
        write_allowed=('write' in reg.access if reg.access else None),
        reset_value=reg.reset_value
      ))

      # TODO: register fields!

    dev.modules.append(mod)

  return dev

if __name__ == "__main__":
  # Parse XML
  svd_dev = SVDParser.for_xml_file(sys.argv[1]).get_device()
  dev = convert(svd_dev)

  print(dev.dump())
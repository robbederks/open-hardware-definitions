#!/usr/bin/env python

import sys

# TODO: remove hack
sys.path.append("/home/robbe/open-hardware-definitions/parsers/svd/cmsis-svd/python")
from cmsis_svd.parser import SVDParser

from open_hardware_definitions import Device, Module, Register, Field

def convert(svd_dev_path):
  svd_dev = SVDParser.for_xml_file(svd_dev_path).get_device()

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

      mod.registers.append(Register(
        name=reg.name,
        addr=reg.address_offset,
        size_bits=reg.size,
        description=reg.description,
        read_allowed=('read' in reg.access if reg.access else None),
        write_allowed=('write' in reg.access if reg.access else None),
        reset_value=reg.reset_value,
        fields=fields
      ))

    dev.modules.append(mod)

  return dev

if __name__ == "__main__":
  # Convert!
  dev = convert(sys.argv[1])

  # Dump out!
  print(dev.dump())

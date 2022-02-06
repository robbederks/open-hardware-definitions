#!/usr/bin/env python3

import yaml
from open_hardware_definitions.helpers import CleanYAMLObject, HexInt

# Make sure we represent HexInt values as hex
yaml.add_representer(HexInt, lambda dumper, data: dumper.represent_int(hex(data)))


class Endianness:
  LITTLE = 'little'
  BIG = 'big'


class Processor(CleanYAMLObject):
  yaml_tag = "!Processor"

  def __init__(self,
               manufacturer,
               part_number,
               bit_width=None,
               endianness=None,
               modules=None,
               extras=None):
    self.manufacturer = manufacturer
    self.part_number = part_number
    self.bit_width = bit_width
    self.endianness = endianness
    if extras:
      for k in extras.keys():
        setattr(self, k, extras[k])

    self.modules = modules if modules else []

  def dump(self):
    return yaml.dump(self, sort_keys=False)


class Module(CleanYAMLObject):
  yaml_tag = "!Module"

  def __init__(self, name=None, base_addr=None, registers=None, extras=None):
    self.name = name
    self.base_addr = HexInt(base_addr)
    if extras:
      for k in extras.keys():
        setattr(self, k, extras[k])

    self.registers = registers if registers else []


class Register(CleanYAMLObject):
  yaml_tag = "!Register"

  def __init__(self,
               name,
               addr,
               description=None,
               read_allowed=None,
               write_allowed=None,
               default_value=None,
               extras=None):
    self.name = name
    self.addr = HexInt(addr)
    self.description = description
    self.read_allowed = read_allowed
    self.write_allowed = write_allowed
    self.default_value = HexInt(default_value) if default_value else None
    if extras:
      for k in extras.keys():
        setattr(self, k, extras[k])


if __name__ == "__main__":
  p = Processor("NXP", "MPC5668x", endianness=Endianness.LITTLE, extras={'flash_size': 1024})

  fr = Module("FlexRay", 0x1000)
  fr.registers.extend([
    Register('REG_A', 0x1000, "This is register A"),
    Register('REG_B', 0x1004, "This is register B")
  ])

  p.modules.append(fr)

  print(p.dump())

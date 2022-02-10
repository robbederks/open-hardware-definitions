#!/usr/bin/env python3

import yaml
from enum import Enum
from typing import Any, List, Mapping, Optional
from open_hardware_definitions.helpers import CleanYAMLObject, HexInt

# Make sure we represent HexInt values as hex
yaml.add_representer(HexInt, lambda dumper, data: dumper.represent_scalar('tag:yaml.org,2002:int', hex(data)))


class Endianness(Enum):
  LITTLE = 'little'
  BIG = 'big'


class Field(CleanYAMLObject):
  yaml_tag = "!Field"

  def __init__(self,
               name,
               bit_offset,
               bit_width,
               description=None,
               read_allowed=None,
               write_allowed=None,
               enum_values=None,
               extras=None):
    self.name = name
    self.bit_offset = bit_offset
    self.bit_width = bit_width
    self.description = description
    self.read_allowed = read_allowed
    self.write_allowed = write_allowed
    self.enum_values = enum_values
    if extras:
      for k in extras.keys():
        setattr(self, k, extras[k])


class Register(CleanYAMLObject):
  yaml_tag = "!Register"

  def __init__(self,
               name,
               addr,
               size_bits,
               description=None,
               read_allowed=None,
               write_allowed=None,
               reset_value=None,
               fields=None,
               extras=None):
    self.name = name
    self.addr = HexInt(addr)
    self.size_bits = size_bits
    self.description = description
    self.read_allowed = read_allowed
    self.write_allowed = write_allowed
    self.reset_value = HexInt(reset_value) if reset_value else None
    if extras:
      for k in extras.keys():
        setattr(self, k, extras[k])

    self.fields = fields if fields else []


class Module(CleanYAMLObject):
  yaml_tag = "!Module"

  def __init__(self,
               name=None,
               base_addr=None,
               size=None,
               description=None,
               registers=None,
               extras=None):
    self.name = name
    self.description = description
    self.base_addr = HexInt(base_addr)
    self.size = HexInt(size) if size else None
    if extras:
      for k in extras.keys():
        setattr(self, k, extras[k])

    self.registers = registers if registers else []

  def __str__(self):
    return f"Module '{self.name}': Base address: {hex(self.base_addr)}"

class Device(CleanYAMLObject):
  yaml_tag = "!Device"

  def __init__(self,
               manufacturer: str,
               part_number: str,
               architecture: Optional[str] = None,
               bit_width: Optional[int] = None,
               endianness: Optional[Endianness] = None,
               modules: Optional[List[Module]] = None,
               extras: Optional[Mapping[str, Any]]=None) -> None:
    self.manufacturer = manufacturer
    self.part_number = part_number
    self.architecture = architecture
    self.bit_width = bit_width
    self.endianness = endianness
    if extras:
      for k in extras.keys():
        setattr(self, k, extras[k])

    self.modules = modules if modules else []

  def dump(self):
    return yaml.dump(self, sort_keys=False)


if __name__ == "__main__":
  p = Device("NXP", "MPC5668x", endianness=Endianness.LITTLE, extras={'flash_size': 1024})

  fr = Module("FlexRay", 0x1000)
  fr.registers.extend([
    Register('REG_A', 0x1000, "This is register A"),
    Register('REG_B', 0x1004, "This is register B", fields=[
      Field('FIELD_B1', 0, 2),
      Field('FIELD_B2', 2, 2, enum_values={0: "enum0", 2: "enum2"}),
    ])
  ])

  p.modules.append(fr)

  print(p.dump())

#!/usr/bin/env python3

from __future__ import annotations

import yaml
try:
  # Speed up with the C-libs if possible
  from yaml import CFullLoader as Loader, CDumper as Dumper
except ImportError:
  from yaml import FullLoader as Loader, Dumper # type: ignore

import math
from enum import Enum
from typing import Any, List, Mapping, Optional, Union

from open_hardware_definitions.helpers import CleanYAMLObject, HexInt

# Make sure we represent HexInt values as hex
yaml.add_representer(
  HexInt,
  lambda dumper, data: dumper.represent_scalar('tag:yaml.org,2002:int', hex(data)),
  Dumper)

class Endianness(Enum):
  LITTLE = 'little'
  BIG = 'big'

yaml.add_representer(
  Endianness,
  lambda dumper, data: dumper.represent_str(data.value),
  Dumper)

class Field(CleanYAMLObject):
  yaml_loader = Loader
  yaml_dumper = Dumper
  yaml_tag = "!Field"

  def __init__(self,
               name: str,
               bit_offset: int,
               bit_width: int,
               description: Optional[str] = None,
               read_allowed: Optional[bool] = None,
               write_allowed: Optional[bool] = None,
               enum_values: Optional[Mapping[int, str]] = None,
               extras: Optional[Mapping[str, Any]] = None):
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
  yaml_loader = Loader
  yaml_dumper = Dumper
  yaml_tag = "!Register"

  def __init__(self,
               name: str,
               addr: int,
               size_bits: Optional[int] = None,
               description: Optional[str] = None,
               read_allowed: Optional[bool] = None,
               write_allowed: Optional[bool] = None,
               reset_value: Optional[int] = None,
               fields: Optional[List[Field]] = None,
               extras: Optional[Mapping[str, Any]] = None) -> None:
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


class Region(CleanYAMLObject):
  yaml_loader = Loader
  yaml_dumper = Dumper
  yaml_tag = "!Region"

  def __init__(self,
               name: str,
               base_addr: int,
               size: int,
               readable: Optional[bool] = None,
               writable: Optional[bool] = None,
               executable: Optional[bool] = None,
               volatile: Optional[bool] = None,
               description: Optional[str] = None,
               extras: Optional[Mapping[str, Any]] = None) -> None:
    self.name = name
    self.base_addr = HexInt(base_addr)
    self.size = HexInt(size)
    self.readable = readable
    self.writable = writable
    self.executable = executable
    self.volatile = volatile
    self.description = description
    if extras:
      for k in extras.keys():
        setattr(self, k, extras[k])


class Module(CleanYAMLObject):
  yaml_loader = Loader
  yaml_dumper = Dumper
  yaml_tag = "!Module"

  def __init__(self,
               name: Optional[str] = None,
               base_addr: Optional[int] = None,
               size: Optional[int] = None,
               description: Optional[str] = None,
               registers: Optional[List[Register]] = None,
               extras: Optional[Mapping[str, Any]] = None) -> None:
    self.name = name
    self.description = description
    self.base_addr = HexInt(base_addr) if base_addr else None
    self.size = HexInt(size) if size else None
    if extras:
      for k in extras.keys():
        setattr(self, k, extras[k])

    self.registers = registers if registers else []

  def get_size(self):
    if hasattr(self, 'size'):
      return self.size

    # Calculate based on registers
    if len(self.registers) > 0:
      # TODO: replace this 1 by the actual Device bit width if we have it
      max_addr = max(map(lambda r: r.addr + (math.ceil(r.size_bits/8) if hasattr(r, 'size_bits') else 1), self.registers))
      if max_addr is not None and max_addr > self.base_addr:
        return HexInt(max_addr - self.base_addr)

    return None

  def __str__(self):
    return f"Module '{self.name}': Base address: {hex(self.base_addr)}"

class Device(CleanYAMLObject):
  yaml_loader = Loader
  yaml_dumper = Dumper
  yaml_tag = "!Device"

  def __init__(self,
               manufacturer: str,
               part_number: str,
               architecture: Optional[str] = None,
               bit_width: Optional[int] = None,
               endianness: Optional[Union[Endianness, str]] = None,
               regions: Optional[List[Region]] = None,
               modules: Optional[List[Module]] = None,
               extras: Optional[Mapping[str, Any]] = None) -> None:
    self.manufacturer = manufacturer
    self.part_number = part_number
    self.architecture = architecture
    self.bit_width = bit_width
    self.endianness = endianness
    if extras:
      for k in extras.keys():
        setattr(self, k, extras[k])

    self.regions = regions if regions else []
    self.modules = modules if modules else []

  @classmethod
  def load(self, stream) -> Device:
    dev = yaml.load(stream, Loader=Loader)
    assert isinstance(dev, Device), "Did not load the expected class!"
    return dev

  @classmethod
  def load_file(self, path: str) -> Device:
    with open(path, 'r') as f:
      dev = self.load(f)
      return dev

  def dump(self) -> str:
    return yaml.dump(self, sort_keys=False, Dumper=Dumper)


if __name__ == "__main__":
  p = Device("NXP", "MPC5668x", endianness=Endianness.LITTLE, extras={'flash_size': 1024})

  fr = Module("FlexRay", 0x1000)
  fr.registers.extend([
    Register('REG_A', 0x1000, description="This is register A"),
    Register('REG_B', 0x1004, 32, description="This is register B", fields=[
      Field('FIELD_B1', 0, 2, read_allowed=True, write_allowed=False),
      Field('FIELD_B2', 2, 2, enum_values={0: "enum0", 2: "enum2"}),
    ])
  ])
  p.modules.append(fr)
  p.modules.append(Module("TestModule2", 0x3000, 0x100))

  p.regions.extend([
    Region('FLASH', 0x2000, 0x500, description="This is flash"),
  ])

  d = p.dump()
  print(d)
  dev2 = Device.load(d)

  for m in p.modules:
    print(m.name, m.get_size())

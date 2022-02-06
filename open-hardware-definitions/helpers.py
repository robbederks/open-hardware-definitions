#!/usr/bin/env python3

import yaml

class CleanYAMLObject(yaml.YAMLObject):
  @classmethod
  def to_yaml(cls, dumper, data):
    # Remove None fields from the dump
    data.__dict__ = dict((k, v) for k, v in data.__dict__.items() if v)
    return super().to_yaml(dumper, data)

class HexInt(int):
  def __str__(self):
    return hex(self)

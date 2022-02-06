import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="open_hardware_definitions",
  version="0.0.1",
  author="Robbe Derks",
  author_email="robbe.derks@gmail.com",
  description="Machine-readable hardware definition files for microcontrollers (memory layout, peripheral registers, ...)",
  long_description=long_description,
  long_description_content_type="text/markdown",
  keywords=[],
  url="https://github.com/robbederks/open-hardware-definitions",
  project_urls = {
    'Source Code': 'https://github.com/robbederks/open-hardware-definitions',
    'Bug Tracker': 'https://github.com/robbederks/open-hardware-definitions/issues'
  },
  packages=setuptools.find_packages(),
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      "Development Status :: 4 - Beta"
  ],
  install_requires=[
    'pyyaml'
  ]
)
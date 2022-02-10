# Open Hardware Definitions

In essence, this repository is an attempt to:
1. Collect machine (and human) readable definitions for the memory maps in microcontrollers
2. Make that data easy to use with common reverse-engineering tools such as [Ghidra](https://github.com/NationalSecurityAgency/ghidra)
3. Make that data easy to gather (parse from data sheets, other file formats, ...)


## Contributing definition files

### How can I produce a definition file?
Any means of producing a (valid) definition file is allowed, although some methods are preferable over others. This is due to the fact that we want to keep the amount of errors (due to inaccuracies in the data source, typos, ...) in the submitted definition files low.

For example, from most preferable to less preferable:
1. Conversion from another definition file format (e.g. SVD -> OHD converter in `parsers/svd`)
2. Automatic parsing of a datasheet with a script / notebook (e.g. `parsers/nxp/MPC5668xRM.ipynb`)
3. Manual parsing of a datasheet

If you create a converter script / notebook, please also share this for future reference in the `parsers/` directory!

### Does it matter if the info is not complete?
No! Any (valid) info is always better than no info! If you have a partial definition file, feel free to open a PR!
Also, PRs for extending / fixing existing definition files are certainly welcome!
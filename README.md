# py8disass

Basic disassembler for CHIP8

### Usage

```
usage: py8disass.py [-h] [-o] [-n NAME] path

Disassemble a .c8 into Chip8 asm

positional arguments:
  path                  path to the .c8 file to disassemble

optional arguments:
  -h, --help            show this help message and exit
  -o, --out             disassembler's result will be printed out in a file
  -n NAME, --name NAME  choose a name for the resulting file
```

### Examples

* Download the project
* Type:
  
  ```
  python3 py8disass.py examples/tetris.c8
  ```

It will print something like this:

```
[OFFSET]   [INSTRUCTION]

[0X200]    LD I, 0x2b4
[0X202]    CALL 0x3e6
[0X204]    CALL 0x2b6
[0X206]    ADD V0, 0x1
[0X208]    DRW V0, V1, 0x1
[0X20A]    SE V0, 0x25
[0X20C]    JP 0x206
[0X20E]    ADD V1, 0xff
[0X210]    DRW V0, V1, 0x1
[0X212]    LD V0, 0x1a
[0X214]    DRW V0, V1, 0x1
[0X216]    LD V0, 0x25
[0X218]    SE V1, 0x0
[0X21A]    JP 0x20e
[0X21C]    RND V4, 0x70
[0X21E]    SNE V4, 0x70
[0X220]    JP 0x21c
[0X222]    RND V3, 0x3
[0X224]    LD V0, 0x1e
...
```

### References

* [Cowgod's Chip-8 Technical Reference v1.0](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM) -  Technical reference by Thomas P. Green

""" Basic disassembler for CHIP8 ; by weld, wtfpl
"""	

""" Special thanks to Thomas P. Green's documentation, found at http://devernay.free.fr/hacks/chip8/C8TECH10.HTM
"""

"""
usage: py8disass.py [-h] [-o] [-n NAME] path

Disassemble a .c8 into Chip8 asm

positional arguments:
  path                  path to the .c8 file to disassemble

optional arguments:
  -h, --help            show this help message and exit
  -o, --out             disassembler's result will be printed out in a file
  -n NAME, --name NAME  choose a name for the resulting file

"""
### === IMPORT === ###
try:
    import argparse as argp
    from os import path
except ImportError as err:
     print("[ERROR] ImportError : ", err)
### === CONST === ###
### === CLASS === ###
class Disass:
    def __init__(self, filePath, out, name):
        self._filePath = filePath        # Path file to disassemble
        self._printOrWrite = out
        self._outName = self._filePath.split('.')[0] + "_dump.txt" if name == "" else name # Name of the file output

        self._opcode = 0              # Current opcode
        self._opcodeReadable = None   # Human-readable opcode
        
        self._memory = [0]*4096       # Chip8 supports 4kbytes memory ; 0x200-0xFFF are values used to store the exe
        self._pc = 0                  # Program counter
    
        self._dump = []               # Containing the executable formatted into human readable instructions
    
    def disass_process(self):
        # init values
        self._memory = [0]*4096
        self._pc = 0x200

        # load EXE in mem
        self._load_in_mem()

        # fill dump with (offset, opcode in readable format)
        while True:
            self._opcode = (self._memory[self._pc]<<8) | (self._memory[self._pc+1]) # Instructions are 2 bytes long
            if self._opcode != 0x0:
                self._opcodeReadable = self._readable_opcode(self._opcode)
                self._dump.append((hex(self._pc).upper(), self._opcodeReadable))
                self._pc += 2
            else:
                break
        
        if self._printOrWrite:
            self._out_file()
        else:
            self._print_dump()

    @staticmethod
    def _readable_opcode(opcode):
        if (opcode & 0xF000) == 0x0000:
            if (opcode & 0x00FF) == 0x00E0:     # CLS
                opcode_readable = "CLS"
            elif(opcode & 0x00FF) == 0x00EE:    # RET
                opcode_readable = "RET"
            else:                               # SYS addr
                opcode_readable = "SYS "+ hex(opcode & 0x0FFF)
        elif (opcode & 0xF000) == 0x1000:       # JP NNN
            opcode_readable = "JP "+hex(opcode & 0x0FFF)
        elif (opcode & 0xF000) == 0x2000:       # CALL NNNN
            opcode_readable = "CALL "+hex(opcode & 0x0FFF)
        elif (opcode & 0xF000) == 0x3000:       # SE Vx, byte
            opcode_readable = "SE V"+str((opcode & 0x0F00)>>8)+", "+hex(opcode & 0x00FF)
        elif (opcode & 0xF000) == 0x4000:       # SNE Vx, byte
            opcode_readable = "SNE V"+str((opcode & 0x0F00)>>8)+", "+hex(opcode & 0x00FF)
        elif (opcode & 0xF000) == 0x5000:       # SE Vx, Vy
            opcode_readable = "SE V"+str((opcode & 0x0F00)>>8)+", V"+str((opcode & 0x00F0)>>4)
        elif (opcode & 0xF000) == 0x6000:       # LD Vx, byte
            opcode_readable = "LD V"+str((opcode & 0x0F00)>>8)+", "+hex(opcode & 0x00FF)
        elif (opcode & 0xF000) == 0x7000:       # ADD Vx, byte
            opcode_readable = "ADD V"+str((opcode & 0x0F00)>>8)+", "+hex(opcode & 0x00FF)
        elif (opcode & 0xF000) == 0x8000:
            if (opcode & 0x000F) == 0x0000:     # LD Vx, Vy
                opcode_readable = "LD V"+str((opcode & 0x0F00)>>8)+", V"+str((opcode & 0x00F0)>>4)
            elif (opcode & 0x000F) == 0x0001:   # OR Vx, Vy
                opcode_readable = "OR V"+str((opcode & 0X0F00)>>8)+", V"+str((opcode & 0x00F0)>>4)
            elif (opcode & 0x000F) == 0x0002:   # AND Vx, Vy
                opcode_readable = "AND V"+str((opcode & 0X0F00)>>8)+", V"+str((opcode & 0x00F0)>>4)
            elif (opcode & 0x000F) == 0x0003:   # XOR Vx, Vy
                opcode_readable = "XOR V"+str((opcode & 0X0F00)>>8)+", V"+str((opcode & 0x00F0)>>4)
            elif (opcode & 0x000F) == 0x0004:   # ADD Vx, Vy
                opcode_readable = "ADD V"+str((opcode & 0X0F00)>>8)+", V"+str((opcode & 0x00F0)>>4)
            elif (opcode & 0x000F) == 0x0005:   # SUB Vx, Vy
                opcode_readable = "SUB V"+str((opcode & 0X0F00)>>8)+", V"+str((opcode & 0x00F0)>>4)
            elif (opcode & 0x000F) == 0x0006:   # SHR Vx {, Vy}
                opcode_readable = "SHR V"+str((opcode & 0X0F00)>>8)+"{, V"+str((opcode & 0x00F0)>>4)+"}"
            elif (opcode & 0x000F) == 0x0007:   # SUBN Vx, Vy
                opcode_readable = "SUBN V"+str((opcode & 0X0F00)>>8)+", V"+str((opcode & 0x00F0)>>4)
            elif (opcode & 0x000F) == 0x000E:   # SHL Vx {, Vy}
                opcode_readable = "SHL V"+str((opcode & 0X0F00)>>8)+"{, V"+str((opcode & 0x00F0)>>4)+"}"
            else:
                opcode_readable = hex(opcode)
        elif (opcode & 0xF000) == 0x9000:       # SNE Vx, Vy
            opcode_readable = "SNE V"+str((opcode & 0x0F00)>>8)+", V"+str((opcode & 0x00F0)>>4)
        elif (opcode & 0xF000) == 0xA000:       # LD I, addr
            opcode_readable = "LD I, "+hex(opcode & 0x0FFF)
        elif (opcode & 0xF000) == 0xB000:       # JP V0, addr
            opcode_readable = "LD V0, "+hex(opcode & 0x0FFF)
        elif (opcode & 0xF000) == 0xC000:       # RND Vx, byte
            opcode_readable = "RND V"+str((opcode & 0x0F00)>>8)+", "+hex(opcode & 0x00FF)
        elif (opcode & 0xF000) == 0xD000:       # DRW Vx, Vy, nibble
            opcode_readable = "DRW V"+str((opcode & 0x0F00)>>8)+", V"+str((opcode & 0x00F0)>>4)+", "+hex(opcode & 0x000F)
        elif (opcode & 0xF000) == 0xE000:
            if (opcode & 0x00FF) == 0x009E:     # SKP Vx
                opcode_readable = "SKP V"+str((opcode & 0x0F00)>>8)
            elif (opcode & 0x00FF) == 0x00A1:   # SKNP Vx
                opcode_readable = "SKNP V"+str((opcode & 0x0F00)>>8)
            else:
                opcode_readable = hex(opcode)
        elif (opcode & 0xF000) == 0xF000:
            if (opcode & 0x00FF) == 0x0007:     # LD Vx, DT
                opcode_readable = "LD V"+str((opcode & 0x0F00)>>8)+", DT"
            elif (opcode & 0x00FF) == 0x000A:   # LD Vx, _KEY_
                opcode_readable = "LD V"+str((opcode & 0x0F00)>>8)+", _KEY_"
            elif (opcode & 0x00FF) == 0x0015:   # LD DT, Vx
                opcode_readable = "LD DT, V"+str((opcode & 0x0F00)>>8)
            elif (opcode & 0x00FF) == 0x0018:   # LD ST, Vx
                opcode_readable = "LD ST, V"+str((opcode & 0x0F00)>>8)
            elif (opcode & 0x00FF) == 0x001E:   # ADD I, Vx
                opcode_readable = "ADD I, V"+str((opcode & 0x0F00)>>8)
            elif (opcode & 0x00FF) == 0x0029:   # LD _CHAR_, Vx
                opcode_readable = "LD _CHAR_, V"+str((opcode & 0x0F00)>>8)
            elif (opcode & 0x00FF) == 0x0033:   # LD _BCD_, Vx
                opcode_readable = "LD _BCD_, V"+str((opcode & 0x0F00)>>8)
            elif (opcode & 0x00FF) == 0x0055:   # LD [I], Vx
                opcode_readable = "LD [I], V"+str((opcode & 0x0F00)>>8)
            elif (opcode & 0x00FF) == 0x0065:   #LD Vx, [I]
                opcode_readable = "LD V"+str((opcode & 0x0F00)>>8)+", [I]"
            else:
                opcode_readable = hex(opcode)
        else:
            opcode_readable = hex(opcode)   # To ensure we always have an instruction printed
                                            # even if disass don't handle it

        return opcode_readable

    def _print_dump(self):
        print("[OFFSET]   [INSTRUCTION]\n")
        for i in range(len(self._dump)):
            print("[%s]    %s" % (self._dump[i][0], self._dump[i][1]))
    
    def _out_file(self):
        FILE = open(self._outName, 'w')
        FILE.write("[OFFSET]   [INSTRUCTION]\n")
        for i in range(len(self._dump)):
            FILE.write("["+self._dump[i][0]+"]    "+self._dump[i][1]+"\n")
        FILE.close()
    def _load_in_mem(self):
        ROM = open(self._filePath, mode='rb')
        try:
            size = path.getsize(self._filePath)
            for i in range(size):
                byte = ROM.read(1)
                if byte != "":
                    self._memory[0x200+i] = int(byte.hex(), 16)
        except OSError as err:
            print("Can't read the file at: %s, Error: %s " % (self._filePath, err))
        finally:
            ROM.close()
### === FUNCTIONS === ###
### === ENTRY POINT === ###
if __name__ == '__main__':
    try:
        parser = argp.ArgumentParser(description='Disassemble a .c8 into Chip8 asm')
        parser.add_argument('path', help='path to the .c8 file to disassemble')
        parser.add_argument('-o', '--out', default=False, action='store_true', help='disassembler\'s result will be printed out in a file')
        parser.add_argument('-n', '--name', default="", help='choose a name for the resulting file')
        args = parser.parse_args()

        Disass(args.path, args.out, args.name).disass_process()
    except argp.ArgumentError as err:
        parser.print_help()
    

from compiler import Compiler
from elf import save_as_elf
from itertools import zip_longest
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", type=str, nargs="+", help="output file name", default=[], metavar=("out1", "out2"))
    parser.add_argument("infile", type=str, nargs="+", help="brainfuck source")
    args = parser.parse_args()

    compiler = Compiler()
    for file, out_name in zip_longest(args.infile, args.o):
        with open(file) as f:
            data = f.read()
        binary = compiler.compile(data)
        if out_name is not None:
            save_as_elf(binary, out_name)
        else:
            save_as_elf(binary, file[:file.rfind(".")])

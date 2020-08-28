from ctypes import *
from struct import unpack
import io

class ELFFileHeader(Structure):
    _fields_ = [
        ("e_ident", c_char * 16),
        ("e_type", c_uint16),
        ("e_machine", c_uint16),
        ("e_version", c_uint32),
        ("e_entry", c_uint64),
        ("e_phoff", c_uint64),
        ("e_shoff", c_uint64),
        ("e_flags", c_uint32),
        ("e_ehsize", c_uint16),
        ("e_phentsize", c_uint16),
        ("e_phnum", c_uint16),
        ("e_shentsize", c_uint16),
        ("e_shnum", c_uint16),
        ("e_shstrndx", c_uint16),
    ]

class ELFProgramHeader(Structure):
    _fields_ = [
        ("p_type", c_uint32),
        ("p_flags", c_uint32),
        ("p_offset", c_uint64),
        ("p_vaddr", c_uint64),
        ("p_paddr", c_uint64),
        ("p_filesz", c_uint64),
        ("p_memsz", c_uint64),
        ("p_align", c_uint64),
    ]


def gen_headers(data):
    # generate file header
    file_header = ELFFileHeader()
    # E_IDENT
    e_ident = b"\x7fELF"   # magic number
    e_ident += b"\x02"     # class
    e_ident += b"\x01"     # data
    e_ident += b"\x01"     # version
    e_ident += b"\x00"     # osabi
    e_ident += b"\x00"     # abi version
    e_ident += b"\x00" * 7 # padding
    # ELF header
    file_header.e_ident = e_ident
    file_header.e_type = 2
    file_header.e_machine = 62
    file_header.e_version = 1
    file_header.e_entry = 0x400078
    file_header.e_phoff = 0x40
    file_header.e_shoff = 0
    file_header.e_flags = 0
    file_header.e_ehsize = 0x40
    file_header.e_phentsize = 0x38
    file_header.e_phnum = 1
    file_header.e_shentsize = 0
    file_header.e_shnum = 0
    file_header.e_shstrndx = 0

    # generate program header
    prog_header = ELFProgramHeader() 
    prog_header.p_type = 1
    prog_header.p_offset = 0
    prog_header.p_vaddr = 0x400000
    prog_header.p_paddr = 0x400000
    prog_header.p_filesz = len(data) + 0x80
    prog_header.p_flags = 1 | 4
    prog_header.p_memsz = len(data) + 0x80
    prog_header.p_align = 0x200000
    return file_header, prog_header

def save_as_elf(data, filename):
    file_header, prog_header = gen_headers(data)

    bio = io.BytesIO()
    bio.write(file_header)
    bio.write(prog_header)
    bio.write(data)

    with open(filename, 'wb') as f:
        f.write(bio.getbuffer())

    bio.close()

const std = @import("std");

const MEMORY_MAX = (1 << 16);
var memory: [MEMORY_MAX]u16 = std.mem.zeroes([MEMORY_MAX]u16);

const Register = enum(u16) { R0, R1, R2, R3, R4, R5, R6, R7, PC, COND, COUNT };

var registers: [@intFromEnum(Register.COUNT)]u16 = std.mem.zeroes([@intFromEnum(Register.COUNT)]u16);

const Opcode = enum {
    BR, // branch
    ADD, // add
    LD, // load
    ST, // store
    JSR, // jump register
    AND, // bitwise and
    LDR, // load register
    STR, // store register
    RTI, // unused
    NOT, // bitwise not
    LDI, // load indirect
    STI, // store indirect
    JMP, // jump
    RES, // reserved (unused)
    LEA, // load effective address
    TRAP, // execute trap
};

const ConditionFlag = enum(u16) {
    POS = (1 << 0), // P
    ZRO = (1 << 1), // Z
    NEG = (1 << 2), // N
};

pub fn read_image(image_pathname: []u8) bool {
    // TODO read image file at image_pathname and load into memory
    std.debug.print("reading image: {s}...\n", .{image_pathname});
    return true;
}

pub fn read_memory(addr: u16) u16 {
    return memory[addr];
}

pub fn main() !void {
    if (std.os.argv.len != 1) {
        std.debug.print("lc3 [image-file1] ...\n", .{});
        std.os.exit(1);
    }

    var image_file: []u8 = std.os.argv.next();
    if (!read_image(image_file)) {
        std.debug.print("failed to load image: {s}\n", .{image_file});
        std.os.exit(1);
    }

    registers[@intFromEnum(Register.COND)] = @intFromEnum(ConditionFlag.ZRO);
    const PC_START: u16 = 0x3000; // start address for program counter
    registers[@intFromEnum(Register.PC)] = PC_START;

    var running: bool = true;
    while (running) {
        var instruction: u16 = read_memory(registers[@intFromEnum(Register.PC)]);
        var opcode: Opcode = @enumFromInt(instruction >> 12);

        switch (opcode) {
            Opcode.ADD => {},
            Opcode.AND => {},
            Opcode.NOT => {},
            Opcode.BR => {},
            Opcode.JMP => {},
            Opcode.JSR => {},
            Opcode.LD => {},
            Opcode.LDI => {},
            Opcode.LDR => {},
            Opcode.LEA => {},
            Opcode.ST => {},
            Opcode.STI => {},
            Opcode.STR => {},
            Opcode.TRAP => {},
            Opcode.RES => {},
            Opcode.RTI => {},
        }
    }
}

test "simple test" {}

const std = @import("std");
const expect = std.testing.expect;

test "test while loop" {
    var i: u8 = 2;
    while (i < 100) {
        i *= 2;
    }
    try expect(i == 128);
}

test "test while with continue expression" {
    var i: usize = 0;
    while (i < 10) : (i += 1) {}
    try expect(i == 10);
}

test "test while with continue expression p2" {
    var sum: u8 = 0;
    var i: u8 = 1;

    while (i <= 10) : (i += 1) {
        sum += i;
        std.debug.print("sum is: {}\n", .{sum});
    }
    try expect(sum == 55);
}

test "test while with continue" {
    var sum: u8 = 0;
    var i: u8 = 0;
    while (i <= 3) : (i += 1) {
        if (i == 2) continue;
        sum += i;
    }
    try expect(sum == 4);
}

test "test while with break" {
    var sum: u8 = 0;
    var i: u8 = 0;
    while (i <= 3) : (i += 1) {
        if (i == 2) break;
        sum += i;
    }
    try expect(sum == 1);
}

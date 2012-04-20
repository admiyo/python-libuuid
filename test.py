#!/usr/bin/python

import  sys
import libuuid


print libuuid.UUID('{12345678-1234-5678-1234-567812345678}')
print libuuid.UUID('12345678123456781234567812345678')
print libuuid.UUID('urn:uuid:12345678-1234-5678-1234-567812345678')
print libuuid.UUID(bytes='\x12\x34\x56\x78'*4)
print libuuid.UUID(bytes_le='\x78\x56\x34\x12\x34\x12\x78\x56' +
                      '\x12\x34\x56\x78\x12\x34\x56\x78')
print libuuid.UUID(fields=(0x12345678, 0x1234, 0x5678, 0x12, 0x34, 0x567812345678))
print libuuid.UUID(int=0x12345678123456781234567812345678)





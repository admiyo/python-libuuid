#!/usr/bin/python

import  sys
import _uuid


newUUID = _uuid.uuid_generate()
print newUUID


newUUID = _uuid.uuid_generate_time()
print newUUID


#libuuid.uuid_generate(uuiddef.UUID(int=0x12345678123456781234567812345678))



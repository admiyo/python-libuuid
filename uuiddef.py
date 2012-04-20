class UUID(object):
    """Instances of the UUID class represent UUIDs as specified in RFC 4122.
    UUID objects are immutable, hashable, and usable as dictionary keys.
    Converting a UUID to a string with str() yields something in the form
    '12345678-1234-1234-1234-123456789abc'.  The UUID constructor accepts
    five possible forms: a similar string of hexadecimal digits, or a tuple
    of six integer fields (with 32-bit, 16-bit, 16-bit, 8-bit, 8-bit, and
    48-bit values respectively) as an argument named 'fields', or a string
    of 16 bytes (with all the integer fields in big-endian order) as an
    argument named 'bytes', or a string of 16 bytes (with the first three
    fields in little-endian order) as an argument named 'bytes_le', or a
    single 128-bit integer as an argument named 'int'.

    UUIDs have these read-only attributes:

        bytes       the UUID as a 16-byte string (containing the six
                    integer fields in big-endian byte order)

        bytes_le    the UUID as a 16-byte string (with time_low, time_mid,
                    and time_hi_version in little-endian byte order)

        fields      a tuple of the six integer fields of the UUID,
                    which are also available as six individual attributes
                    and two derived attributes:

            time_low                the first 32 bits of the UUID
            time_mid                the next 16 bits of the UUID
            time_hi_version         the next 16 bits of the UUID
            clock_seq_hi_variant    the next 8 bits of the UUID
            clock_seq_low           the next 8 bits of the UUID
            node                    the last 48 bits of the UUID

            time                    the 60-bit timestamp
            clock_seq               the 14-bit sequence number

        hex         the UUID as a 32-character hexadecimal string

        int         the UUID as a 128-bit integer

        urn         the UUID as a URN as specified in RFC 4122

        variant     the UUID variant (one of the constants RESERVED_NCS,
                    RFC_4122, RESERVED_MICROSOFT, or RESERVED_FUTURE)

        version     the UUID version number (1 through 5, meaningful only
                    when the variant is RFC_4122)
    """

    def __init__(self, hex=None, bytes=None, bytes_le=None, fields=None,
                       int=None, version=None):
        r"""Create a UUID from either a string of 32 hexadecimal digits,
        a string of 16 bytes as the 'bytes' argument, a string of 16 bytes
        in little-endian order as the 'bytes_le' argument, a tuple of six
        integers (32-bit time_low, 16-bit time_mid, 16-bit time_hi_version,
        8-bit clock_seq_hi_variant, 8-bit clock_seq_low, 48-bit node) as
        the 'fields' argument, or a single 128-bit integer as the 'int'
        argument.  When a string of hex digits is given, curly braces,
        hyphens, and a URN prefix are all optional.  For example, these
        expressions all yield the same UUID:

        UUID('{12345678-1234-5678-1234-567812345678}')
        UUID('12345678123456781234567812345678')
        UUID('urn:uuid:12345678-1234-5678-1234-567812345678')
        UUID(bytes='\x12\x34\x56\x78'*4)
        UUID(bytes_le='\x78\x56\x34\x12\x34\x12\x78\x56' +
                      '\x12\x34\x56\x78\x12\x34\x56\x78')
        UUID(fields=(0x12345678, 0x1234, 0x5678, 0x12, 0x34, 0x567812345678))
        UUID(int=0x12345678123456781234567812345678)

        Exactly one of 'hex', 'bytes', 'bytes_le', 'fields', or 'int' must
        be given.  The 'version' argument is optional; if given, the resulting
        UUID will have its variant and version set according to RFC 4122,
        overriding the given 'hex', 'bytes', 'bytes_le', 'fields', or 'int'.
        """

        if [hex, bytes, bytes_le, fields, int].count(None) != 4:
            raise TypeError('need one of hex, bytes, bytes_le, fields, or int')
        if hex is not None:
            hex = hex.replace('urn:', '').replace('uuid:', '')
            hex = hex.strip('{}').replace('-', '')
            if len(hex) != 32:
                raise ValueError('badly formed hexadecimal UUID string')
            int = long(hex, 16)
        if bytes_le is not None:
            if len(bytes_le) != 16:
                raise ValueError('bytes_le is not a 16-char string')
            bytes = (bytes_le[3] + bytes_le[2] + bytes_le[1] + bytes_le[0] +
                     bytes_le[5] + bytes_le[4] + bytes_le[7] + bytes_le[6] +
                     bytes_le[8:])
        if bytes is not None:
            if len(bytes) != 16:
                raise ValueError('bytes is not a 16-char string')
            int = long(('%02x'*16) % tuple(map(ord, bytes)), 16)
        if fields is not None:
            if len(fields) != 6:
                raise ValueError('fields is not a 6-tuple')
            (time_low, time_mid, time_hi_version,
             clock_seq_hi_variant, clock_seq_low, node) = fields
            if not 0 <= time_low < 1<<32L:
                raise ValueError('field 1 out of range (need a 32-bit value)')
            if not 0 <= time_mid < 1<<16L:
                raise ValueError('field 2 out of range (need a 16-bit value)')
            if not 0 <= time_hi_version < 1<<16L:
                raise ValueError('field 3 out of range (need a 16-bit value)')
            if not 0 <= clock_seq_hi_variant < 1<<8L:
                raise ValueError('field 4 out of range (need an 8-bit value)')
            if not 0 <= clock_seq_low < 1<<8L:
                raise ValueError('field 5 out of range (need an 8-bit value)')
            if not 0 <= node < 1<<48L:
                raise ValueError('field 6 out of range (need a 48-bit value)')
            clock_seq = (clock_seq_hi_variant << 8L) | clock_seq_low
            int = ((time_low << 96L) | (time_mid << 80L) |
                   (time_hi_version << 64L) | (clock_seq << 48L) | node)
        if int is not None:
            if not 0 <= int < 1<<128L:
                raise ValueError('int is out of range (need a 128-bit value)')
        if version is not None:
            if not 1 <= version <= 5:
                raise ValueError('illegal version number')
            # Set the variant to RFC 4122.
            int &= ~(0xc000 << 48L)
            int |= 0x8000 << 48L
            # Set the version number.
            int &= ~(0xf000 << 64L)
            int |= version << 76L
        self.__dict__['int'] = int

    def __cmp__(self, other):
        if isinstance(other, UUID):
            return cmp(self.int, other.int)
        return NotImplemented

    def __hash__(self):
        return hash(self.int)

    def __int__(self):
        return self.int

    def __repr__(self):
        return 'UUID(%r)' % str(self)

    def __setattr__(self, name, value):
        raise TypeError('UUID objects are immutable')

    def __str__(self):
        hex = '%032x' % self.int
        return '%s-%s-%s-%s-%s' % (
            hex[:8], hex[8:12], hex[12:16], hex[16:20], hex[20:])

    def get_bytes(self):
        bytes = ''
        for shift in range(0, 128, 8):
            bytes = chr((self.int >> shift) & 0xff) + bytes
        return bytes

    bytes = property(get_bytes)

    def get_bytes_le(self):
        bytes = self.bytes
        return (bytes[3] + bytes[2] + bytes[1] + bytes[0] +
                bytes[5] + bytes[4] + bytes[7] + bytes[6] + bytes[8:])

    bytes_le = property(get_bytes_le)

    def get_fields(self):
        return (self.time_low, self.time_mid, self.time_hi_version,
                self.clock_seq_hi_variant, self.clock_seq_low, self.node)

    fields = property(get_fields)

    def get_time_low(self):
        return self.int >> 96L

    time_low = property(get_time_low)

    def get_time_mid(self):
        return (self.int >> 80L) & 0xffff

    time_mid = property(get_time_mid)

    def get_time_hi_version(self):
        return (self.int >> 64L) & 0xffff

    time_hi_version = property(get_time_hi_version)

    def get_clock_seq_hi_variant(self):
        return (self.int >> 56L) & 0xff

    clock_seq_hi_variant = property(get_clock_seq_hi_variant)

    def get_clock_seq_low(self):
        return (self.int >> 48L) & 0xff

    clock_seq_low = property(get_clock_seq_low)

    def get_time(self):
        return (((self.time_hi_version & 0x0fffL) << 48L) |
                (self.time_mid << 32L) | self.time_low)

    time = property(get_time)

    def get_clock_seq(self):
        return (((self.clock_seq_hi_variant & 0x3fL) << 8L) |
                self.clock_seq_low)

    clock_seq = property(get_clock_seq)

    def get_node(self):
        return self.int & 0xffffffffffff

    node = property(get_node)

    def get_hex(self):
        return '%032x' % self.int

    hex = property(get_hex)

    def get_urn(self):
        return 'urn:uuid:' + str(self)

    urn = property(get_urn)

    def get_variant(self):
        if not self.int & (0x8000 << 48L):
            return RESERVED_NCS
        elif not self.int & (0x4000 << 48L):
            return RFC_4122
        elif not self.int & (0x2000 << 48L):
            return RESERVED_MICROSOFT
        else:
            return RESERVED_FUTURE

    variant = property(get_variant)

    def get_version(self):
        # The version bits are only meaningful for RFC 4122 UUIDs.
        if self.variant == RFC_4122:
            return int((self.int >> 76L) & 0xf)

    version = property(get_version)

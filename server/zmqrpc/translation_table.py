import msgpack
from decimal import Decimal

translation_table = {
    0: (Decimal,
        lambda value: msgpack.packb(str(value)),
        lambda binary: Decimal(msgpack.unpackb(binary).decode())),
}

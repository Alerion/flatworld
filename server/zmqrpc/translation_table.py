import msgpack
import pickle
from decimal import Decimal
from engine import models


translation_table = {
    0: (Decimal,
        lambda value: msgpack.packb(str(value)),
        lambda binary: Decimal(msgpack.unpackb(binary).decode())),
    # FIXME: Write smarted converter
    1: (models.World,
        lambda value: msgpack.packb(pickle.dumps(value)),
        lambda binary: pickle.loads(msgpack.unpackb(binary))),
}

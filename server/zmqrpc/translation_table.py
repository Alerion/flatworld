import msgpack
import pickle
from decimal import Decimal
from engine.base import Model, ModelsDict


translation_table = {
    0: (Decimal,
        lambda value: msgpack.packb(str(value)),
        lambda binary: Decimal(msgpack.unpackb(binary).decode())),
    # FIXME: Write smarted converter
    1: (Model,
        lambda value: msgpack.packb(pickle.dumps(value)),
        lambda binary: pickle.loads(msgpack.unpackb(binary))),
    2: (ModelsDict,
        lambda value: msgpack.packb(pickle.dumps(value)),
        lambda binary: pickle.loads(msgpack.unpackb(binary))),
}

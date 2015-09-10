import msgpack
import pickle
from decimal import Decimal

import engine.exceptions
from engine.models.base import Model, ModelsDict


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


error_table = {}

for name in dir(engine.exceptions):
    val = getattr(engine.exceptions, name)
    if isinstance(val, type) and issubclass(val, Exception):
        error_table['engine.exceptions.'+name] = val

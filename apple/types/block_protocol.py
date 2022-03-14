from typing import List, Optional

from typing_extensions import Protocol

from apple.types.blockchain_format.program import SerializedProgram
from apple.types.blockchain_format.sized_bytes import bytes32
from apple.util.ints import uint32


class BlockInfo(Protocol):
    @property
    def prev_header_hash(self) -> bytes32:
        pass

    @property
    def transactions_generator(self) -> Optional[SerializedProgram]:
        pass

    @property
    def transactions_generator_ref_list(self) -> List[uint32]:
        pass

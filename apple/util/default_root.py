import os
from pathlib import Path

DEFAULT_ROOT_PATH = Path(os.path.expanduser(os.getenv("APPLE_ROOT", "~/.apple/mainnet"))).resolve()
STANDALONE_ROOT_PATH = Path(
    os.path.expanduser(os.getenv("APPLE_STANDALONE_WALLET_ROOT", "~/.apple/standalone_wallet"))
).resolve()

DEFAULT_KEYS_ROOT_PATH = Path(os.path.expanduser(os.getenv("APPLE_KEYS_ROOT", "~/.apple_keys"))).resolve()

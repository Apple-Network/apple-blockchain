from __future__ import annotations

import os
from pathlib import Path

DEFAULT_ROOT_PATH = Path(os.path.expanduser(os.getenv("APPLE_ROOT", "~/.apple/mainnet"))).resolve()

DEFAULT_KEYS_ROOT_PATH = Path(os.path.expanduser(os.getenv("APPLE_KEYS_ROOT", "~/.apple_keys"))).resolve()

SIMULATOR_ROOT_PATH = Path(os.path.expanduser(os.getenv("APPLE_SIMULATOR_ROOT", "~/.apple/simulator"))).resolve()

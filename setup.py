from setuptools import setup

dependencies = [
    "blspy==1.0.6",  # Signature library
    "chiavdf==1.0.3",  # timelord and vdf verification
    "chiabip158==1.0",  # bip158-style wallet filters
    "chiapos==1.0.4",  # proof of space
    "clvm==0.9.7",
    "clvm_rs==0.1.11",
    "clvm_tools==0.4.3",
    "aiohttp==3.7.4",  # HTTP server for full node rpc
    "aiosqlite==0.17.0",  # asyncio wrapper for sqlite, to store blocks
    "bitstring==3.1.9",  # Binary data management library
    "colorama==0.4.4",  # Colorizes terminal output
    "colorlog==5.0.1",  # Adds color to logs
    "concurrent-log-handler==0.9.19",  # Concurrently log and rotate logs
    "cryptography==3.4.7",  # Python cryptography library for TLS - keyring conflict
    "fasteners==0.16.3",  # For interprocess file locking
    "keyring==23.0.1",  # Store keys in MacOS Keychain, Windows Credential Locker
    "keyrings.cryptfile==1.3.4",  # Secure storage for keys on Linux (Will be replaced)
    #  "keyrings.cryptfile==1.3.8",  # Secure storage for keys on Linux (Will be replaced)
    #  See https://github.com/frispete/keyrings.cryptfile/issues/15
    "PyYAML==5.4.1",  # Used for config file format
    "setproctitle==1.2.2",  # Gives the chia processes readable names
    "sortedcontainers==2.3.0",  # For maintaining sorted mempools
    "websockets==8.1.0",  # For use in wallet RPC and electron UI
    "click==7.1.2",  # For the CLI
    "dnspython==2.1.0",  # Query DNS seeds
    "watchdog==2.1.3",  # Filesystem event watching - watches keyring.yaml
]

upnp_dependencies = [
    "miniupnpc==2.2.2",  # Allows users to open ports on their router
]

dev_dependencies = [
    "pytest",
    "pytest-asyncio",
    "flake8",
    "mypy",
    "black",
    "aiohttp_cors",  # For blackd
    "ipython",  # For asyncio debugging
]

kwargs = dict(
    name="apple-blockchain",
    author="applecoin",
    author_email="mariano@applecoin.in",
    description="Apple blockchain full node, farmer, timelord, and wallet.",
    url="https://applecoin.in/",
    license="Apache License",
    python_requires=">=3.7, <4",
    keywords="apple blockchain node",
    install_requires=dependencies,
    setup_requires=["setuptools_scm"],
    extras_require=dict(
        uvloop=["uvloop"],
        dev=dev_dependencies,
        upnp=upnp_dependencies,
    ),
    packages=[
        "build_scripts",
        "apple",
        "apple.cmds",
        "apple.clvm",
        "apple.consensus",
        "apple.daemon",
        "apple.full_node",
        "apple.timelord",
        "apple.farmer",
        "apple.harvester",
        "apple.introducer",
        "apple.plotting",
        "apple.pools",
        "apple.protocols",
        "apple.rpc",
        "apple.server",
        "apple.simulator",
        "apple.types.blockchain_format",
        "apple.types",
        "apple.util",
        "apple.wallet",
        "apple.wallet.puzzles",
        "apple.wallet.rl_wallet",
        "apple.wallet.cc_wallet",
        "apple.wallet.did_wallet",
        "apple.wallet.settings",
        "apple.wallet.trading",
        "apple.wallet.util",
        "apple.ssl",
        "mozilla-ca",
    ],
    entry_points={
        "console_scripts": [
            "apple = apple.cmds.apple:main",
            "apple_wallet = apple.server.start_wallet:main",
            "apple_full_node = apple.server.start_full_node:main",
            "apple_harvester = apple.server.start_harvester:main",
            "apple_farmer = apple.server.start_farmer:main",
            "apple_introducer = apple.server.start_introducer:main",
            "apple_timelord = apple.server.start_timelord:main",
            "apple_timelord_launcher = apple.timelord.timelord_launcher:main",
            "apple_full_node_simulator = apple.simulator.start_simulator:main",
        ]
    },
    package_data={
        "apple": ["pyinstaller.spec"],
        "": ["*.clvm", "*.clvm.hex", "*.clib", "*.clinc", "*.clsp", "py.typed"],
        "apple.util": ["initial-*.yaml", "english.txt"],
        "apple.ssl": ["apple_ca.crt", "apple_ca.key", "dst_root_ca.pem"],
        "mozilla-ca": ["cacert.pem"],
    },
    use_scm_version={"fallback_version": "unknown-no-.git-directory"},
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
)


if __name__ == "__main__":
    setup(**kwargs)

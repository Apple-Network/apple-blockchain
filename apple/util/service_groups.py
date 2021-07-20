from typing import KeysView, Generator

SERVICES_FOR_GROUP = {
    "all": "apple_harvester apple_timelord_launcher apple_timelord apple_farmer apple_full_node apple_wallet".split(),
    "node": "apple_full_node".split(),
    "harvester": "apple_harvester".split(),
    "farmer": "apple_harvester apple_farmer apple_full_node apple_wallet".split(),
    "farmer-no-wallet": "apple_harvester apple_farmer apple_full_node".split(),
    "farmer-only": "apple_farmer".split(),
    "timelord": "apple_timelord_launcher apple_timelord apple_full_node".split(),
    "timelord-only": "apple_timelord".split(),
    "timelord-launcher-only": "apple_timelord_launcher".split(),
    "wallet": "apple_wallet apple_full_node".split(),
    "wallet-only": "apple_wallet".split(),
    "introducer": "apple_introducer".split(),
    "simulator": "apple_full_node_simulator".split(),
}


def all_groups() -> KeysView[str]:
    return SERVICES_FOR_GROUP.keys()


def services_for_groups(groups) -> Generator[str, None, None]:
    for group in groups:
        for service in SERVICES_FOR_GROUP[group]:
            yield service


def validate_service(service: str) -> bool:
    return any(service in _ for _ in SERVICES_FOR_GROUP.values())

from __future__ import annotations

from typing import Generator, Iterable, KeysView

SERVICES_FOR_GROUP = {
    "all": [
        "apple_harvester",
        "apple_timelord_launcher",
        "apple_timelord",
        "apple_farmer",
        "apple_full_node",
        "apple_wallet",
        "apple_data_layer",
        "apple_data_layer_http",
    ],
    # TODO: should this be `data_layer`?
    "data": ["apple_wallet", "apple_data_layer"],
    "data_layer_http": ["apple_data_layer_http"],
    "node": ["apple_full_node"],
    "harvester": ["apple_harvester"],
    "farmer": ["apple_harvester", "apple_farmer", "apple_full_node", "apple_wallet"],
    "farmer-no-wallet": ["apple_harvester", "apple_farmer", "apple_full_node"],
    "farmer-only": ["apple_farmer"],
    "timelord": ["apple_timelord_launcher", "apple_timelord", "apple_full_node"],
    "timelord-only": ["apple_timelord"],
    "timelord-launcher-only": ["apple_timelord_launcher"],
    "wallet": ["apple_wallet"],
    "introducer": ["apple_introducer"],
    "simulator": ["apple_full_node_simulator"],
    "crawler": ["apple_crawler"],
    "seeder": ["apple_crawler", "apple_seeder"],
    "seeder-only": ["apple_seeder"],
}


def all_groups() -> KeysView[str]:
    return SERVICES_FOR_GROUP.keys()


def services_for_groups(groups: Iterable[str]) -> Generator[str, None, None]:
    for group in groups:
        yield from SERVICES_FOR_GROUP[group]


def validate_service(service: str) -> bool:
    return any(service in _ for _ in SERVICES_FOR_GROUP.values())

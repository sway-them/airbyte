#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#

import logging
from typing import Any, Callable, List, MutableMapping, Tuple

import pendulum
import pytest
from airbyte_cdk.models import AirbyteMessage, ConfiguredAirbyteCatalog, Type
from source_instagram.source import SourceInstagram


@pytest.fixture(name="state")
def state_fixture() -> MutableMapping[str, Any]:
    today = pendulum.today()
    return {"user_insights": {"17841451282174033": {"date": (today - pendulum.duration(days=2)).to_datetime_string()}}}


class TestInstagramSource:
    """Custom integration tests should test incremental with nested state"""

    def test_account_user_insights(self, configured_catalog, config, state):
        # catalog = self.slice_catalog(configured_catalog, lambda name: name == "media_insights")
        # catalog = self.slice_catalog(configured_catalog, lambda name: name == "story_insights")
        # catalog = self.slice_catalog(configured_catalog, lambda name: name == "daily_user_insights")
        # catalog = self.slice_catalog(configured_catalog, lambda name: name == "profile_activity_media_insights")
        # catalog = self.slice_catalog(configured_catalog, lambda name: name == "user_demographics_insights")
        # catalog = self.slice_catalog(configured_catalog, lambda name: name == "user_lifetime_insights")
        # catalog = self.slice_catalog(configured_catalog, lambda name: name == "user_insights_with_breakdown")
        # catalog = self.slice_catalog(configured_catalog, lambda name: name == "user_tags")
        catalog = self.slice_catalog(configured_catalog, lambda name: name == "media")

        records, states = self._read_records(config, catalog)
        # import ipdb

        # ipdb.set_trace()

    @staticmethod
    def slice_catalog(catalog: ConfiguredAirbyteCatalog, predicate: Callable[[str], bool]) -> ConfiguredAirbyteCatalog:
        sliced_catalog = ConfiguredAirbyteCatalog(streams=[])
        for stream in catalog.streams:
            if predicate(stream.stream.name):
                sliced_catalog.streams.append(stream)
        return sliced_catalog

    @staticmethod
    def _read_records(conf, catalog, state=None) -> Tuple[List[AirbyteMessage], List[AirbyteMessage]]:
        records = []
        states = []
        for message in SourceInstagram().read(logging.getLogger("airbyte"), conf, catalog, state=state):
            if message.type == Type.RECORD:
                records.append(message)
            elif message.type == Type.STATE:
                states.append(message)

        return records, states

"""
FiftyOne Server /sort route

| Copyright 2017-2024, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""
from dataclasses import asdict

from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request

from fiftyone.core.json import stringify
from fiftyone.core.utils import run_sync_task

from fiftyone.server.decorators import route
import fiftyone.server.events as fose
from fiftyone.server.query import serialize_dataset
import fiftyone.server.view as fosv
from fiftyone.server.filters import GroupElementFilter, SampleFilter


class Sort(HTTPEndpoint):
    @route
    async def post(self, request: Request, data: dict):
        dataset_name = data.get("dataset", None)
        filters = data.get("filters", {})
        stages = data.get("view", None)
        subscription = data.get("subscription", None)
        slice = data.get("slice", None)

        await run_sync_task(
            lambda: fosv.get_view(
                dataset_name,
                stages=stages,
                filters=filters,
                extended_stages={
                    "fiftyone.core.stages.SortBySimilarity": data["extended"]
                },
                sample_filter=SampleFilter(
                    group=GroupElementFilter(slice=slice)
                )
                if slice is not None
                else None,
            )
        )

        state = fose.get_state()
        state.selected = []
        state.selected_labels = []

        await fose.dispatch_event(subscription, fose.StateUpdate(state))

        # empty response
        #
        # /sort is only used to populate a dist_field, if provided
        return {}

import copy

import pytest

from src import app as app_module

_original_activities = copy.deepcopy(app_module.activities)

@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(_original_activities))
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(_original_activities))

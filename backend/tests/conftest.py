"""Shared pytest fixtures — MongoDB collections are fully mocked."""

import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def mock_collections():
    """Return a dict of MagicMock collections keyed by dependency name."""
    return {
        "products": MagicMock(),
        "inventory": MagicMock(),
        "cart": MagicMock(),
        "orders": MagicMock(),
        "payments": MagicMock(),
    }


@pytest.fixture
def client(mock_collections):
    """TestClient with all MongoDB collections replaced by mocks."""
    from app.dependencies import products_col, inventory_col, cart_col, orders_col, payments_col

    app = create_app()
    app.dependency_overrides[products_col] = lambda: mock_collections["products"]
    app.dependency_overrides[inventory_col] = lambda: mock_collections["inventory"]
    app.dependency_overrides[cart_col] = lambda: mock_collections["cart"]
    app.dependency_overrides[orders_col] = lambda: mock_collections["orders"]
    app.dependency_overrides[payments_col] = lambda: mock_collections["payments"]

    with TestClient(app) as c:
        yield c

from page_loader.scripts import page_loader
import pytest


def test_main():
    assert page_loader.main() == 'start'

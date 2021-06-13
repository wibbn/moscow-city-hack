import os
import sys

from flask_script import Manager
from app import create_app

app = create_app('default')
manager = Manager(app)

@manager.command
def test(coverage=False):
    """Run the unit tests."""

    import pytest
    pytest.main()


if __name__ == "__main__":
    manager.run()
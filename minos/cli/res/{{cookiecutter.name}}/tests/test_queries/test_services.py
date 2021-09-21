import sys
import unittest

from src import (
    {{ cookiecutter.aggregate }}QueryService,
)
from tests.utils import (
    build_dependency_injector,
)


class Test{{cookiecutter.aggregate}}QueryService(unittest.IsolatedAsyncioTestCase):
    """Test {{cookiecutter.aggregate}}"""

    def setUp(self) -> None:
        self.injector = build_dependency_injector()

    async def asyncSetUp(self) -> None:
        await self.injector.wire(modules=[sys.modules[__name__]])

    async def asyncTearDown(self) -> None:
        await self.injector.unwire()

    def test_constructor(self):
        obj = {{ cookiecutter.aggregate }}QueryService()
        self.assertIsInstance(obj, {{cookiecutter.aggregate}}QueryService)

if __name__ == '__main__':
    unittest.main()

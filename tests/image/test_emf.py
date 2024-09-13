"""Test suite for docx.image.bmp module."""

import pytest

from docx.image.emf import Emf
from docx.image.constants import MIME_TYPE

from ..unitutil.mock import ANY, initializer_mock
from ..unitutil.file import test_file


class DescribeEmf:
    def it_can_construct_from_an_emf_stream(self, Emf__init__):
        cx, cy, horz_dpi, vert_dpi = 88, 88, 72, 72

        with open(test_file("example.emf"), "rb") as stream:
            emf = Emf.from_stream(stream)

        Emf__init__.assert_called_once_with(ANY, cx, cy, horz_dpi, vert_dpi)
        assert isinstance(emf, Emf)

    def it_knows_its_content_type(self):
        emf = Emf(None, None, None, None)
        assert emf.content_type == MIME_TYPE.EMF

    def it_knows_its_default_ext(self):
        emf = Emf(None, None, None, None)
        assert emf.default_ext == "emf"

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def Emf__init__(self, request):
        return initializer_mock(request, Emf)

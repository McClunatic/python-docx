"""Test suite for docx.image.bmp module."""

import pytest

from docx.image.svg import Svg
from docx.image.constants import MIME_TYPE

from ..unitutil.mock import ANY, initializer_mock
from ..unitutil.file import test_file


class DescribeSvg:
    def it_can_construct_from_an_svg_stream(self, Svg__init__):
        cx, cy, horz_dpi, vert_dpi = 300, 200, 72, 72
        with open(test_file("demo1.svg"), "rb") as stream:
            svg = Svg.from_stream(stream)

        Svg__init__.assert_called_once_with(ANY, cx, cy, horz_dpi, vert_dpi)
        assert isinstance(svg, Svg)

    def it_knows_its_content_type(self):
        svg = Svg(None, None, None, None)
        assert svg.content_type == MIME_TYPE.SVG

    def it_knows_its_default_ext(self):
        svg = Svg(None, None, None, None)
        assert svg.default_ext == "svg"

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def Svg__init__(self, request):
        return initializer_mock(request, Svg)

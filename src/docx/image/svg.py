import math
import re
import xml.etree.ElementTree as ET

from .constants import MIME_TYPE
from .image import BaseImageHeader


class Svg(BaseImageHeader):
    """
    Image header parser for SVG images.
    """

    @classmethod
    def from_stream(cls, stream):
        """
        Return |Svg| instance having header properties parsed from SVG image
        in *stream*.
        """
        px_width, px_height = cls._dimensions_from_stream(stream)
        return cls(px_width, px_height, 72, 72)

    @property
    def content_type(self):
        """
        MIME content type for this image, unconditionally `image/svg+xml` for
        SVG images.
        """
        return MIME_TYPE.SVG

    @property
    def default_ext(self):
        """
        Default filename extension, always 'svg' for SVG images.
        """
        return "svg"

    @classmethod
    def _dimensions_from_stream(cls, stream):
        stream.seek(0)
        data = stream.read()
        root = ET.fromstring(data)

        width = root.attrib["width"]
        height = root.attrib["height"]

        # Treat px and pt the same: presume everywhere a 72 dpi device
        dpi = 72
        if pt_match := re.match(r"(\d+(?:\.\d+)?)\s*p[tx]", width):
            width, = pt_match.groups(1)
        elif mm_match := re.match(r"(d\+(?:\.\d+)?)\s*mm", width):
            dpmm = dpi * 25.4  # mm / in
            width, = mm_match.groups(1) * dpmm
        elif cm_match := re.match(r"(d\+(?:\.\d+)?)\s*cm", width):
            dpcm = dpi * 2.54  # cm / in
            width, = cm_match.groups(1) * dpcm
        elif pc_match := re.match(r"(d\+(?:\.\d+)?)\s*pc", width):
            dppc = dpi / 12  # 12 pt / pc
            width, = pc_match.groups(1) * dppc
        elif in_match := re.match(r"(d\+(?:\.\d+)?)\s*in", width):
            width, = in_match.groups(1) * dpi

        if pt_match := re.match(r"(\d+(?:\.\d+)?)\s*p[tx]", height):
            height, = pt_match.groups(1)
        elif mm_match := re.match(r"(d\+(?:\.\d+)?)\s*mm", height):
            dpmm = dpi * 25.4  # mm / in
            height, = mm_match.groups(1) * dpmm
        elif cm_match := re.match(r"(d\+(?:\.\d+)?)\s*cm", height):
            dpcm = dpi * 2.54  # cm / in
            height, = cm_match.groups(1) * dpcm
        elif pc_match := re.match(r"(d\+(?:\.\d+)?)\s*pc", height):
            dppc = dpi / 12  # 12 pt / pc
            height, = pc_match.groups(1) * dppc
        elif in_match := re.match(r"(d\+(?:\.\d+)?)\s*in", height):
            height, = in_match.groups(1) * dpi

        return math.floor(float(width)), math.floor(float(height))

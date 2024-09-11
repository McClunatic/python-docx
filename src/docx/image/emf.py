import struct

from .constants import MIME_TYPE
from .exceptions import InvalidImageStreamError
from .helpers import BIG_ENDIAN, StreamReader
from .image import BaseImageHeader


class Emf(BaseImageHeader):
    """
    Image header parser for PNG images
    """
    @property
    def content_type(self):
        """
        MIME content type for this image, unconditionally `image/emf` for
        EMF images.
        """
        return MIME_TYPE.EMF

    @property
    def default_ext(self):
        """
        Default filename extension, always 'emf' for EMF images.
        """
        return 'emf'

    @classmethod
    def from_stream(cls, stream,filename=None):
        """
        Return an |Emf| instance having header properties parsed from image in
        *stream*.

        Refer to
        https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-emf/91c257d7-c39d-4a36-9b1f-63e3f73d30ca
        for more information.
        """

        stream.seek(0)
        x = stream.read(40)
        stream.seek(0)
        rcl_frame = struct.unpack("iiii", x[24:40])

        # 1 dpi = 1/25.4 dp millimeter
        horz_dpi = vert_dpi = dpi = 72
        mm_width = (rcl_frame[2] - rcl_frame[0]) / 100.0
        mm_height = (rcl_frame[3] - rcl_frame[1]) / 100.0
        px_width = int(mm_width * dpi / 25.4)
        px_height = int(mm_height * dpi / 25.4)

        return cls(px_width, px_height, horz_dpi, vert_dpi)

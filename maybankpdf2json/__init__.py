from importlib.metadata import PackageNotFoundError, version

from .extractor import MaybankPdf2Json
from .utils import Output, OutputV2

try:
    __version__ = version("maybankpdf2json")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ["MaybankPdf2Json", "Output", "OutputV2", "__version__"]

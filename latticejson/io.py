from typing import Dict
from pathlib import Path
import json
from .convert import elegant_to_latticejson, latticejson_to_elegant
from .validate import validate


def read(text, file_format) -> Dict:
    """Read/validate lattice file and return latticeJSON dict."""

    if file_format == ".json":
        latticejson = json.loads(text)
    elif file_format == ".lte":
        latticejson = elegant_to_latticejson(text)
    else:
        raise NotImplementedError(f"Unkown file file_format {file_format}.")

    validate(latticejson)
    return latticejson


def read_file(path) -> Dict:
    """Read lattice file from path

    :param path path-like: Path to lattice file
    :return: latticeJSON compliant dict.
    """
    path = Path(path)
    suffix = path.suffix
    text = path.read_text()
    return read(text, suffix)


def convert(text, input_format, output_format) -> str:
    """Convert lattice file to format.

    :param text str: Content of the input lattice file.
    :param input_format str: Input format of the source lattice file.
    :param output_format str: Ouput format of the new lattice file.
    :raises NotImplementedError: Is raised for unkown lattice file formats.
    :return: Returns new lattice file as string
    :rtype: str
    """
    lattice_json = read(text, input_format)
    if output_format == "latticejson":
        return json.dumps(lattice_json, indent=4)
    elif output_format == "elegant":
        return latticejson_to_elegant(lattice_json)

    raise NotImplementedError(f"Converting to {output_format} is not implemented!")


def convert_file(path, output_format) -> str:
    """Convert a lattice file into `output_format`

    :param path path-like: Path to lattice file
    :param output_format str: Format of the new lattice file
    :return: Returns the new lattice file as string
    :rtype: str
    """
    path = Path(path)
    suffix = path.suffix
    text = path.read_text()
    return convert(text, suffix, output_format)
#!/usr/bin/env python3
"""
Created on Thu May 9 18:21:58 2021

@author: gonzo
"""
import re
from typing import Any, Optional

import orjson
from pandas import DataFrame

re_pattern = re.compile(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")


def to_dataframe(table: list[dict], key: Optional[str] = None) -> DataFrame:
    """converts a list of dicts to a data frame
    Args:
        table (list(dict())): list of dicts
        key (str, optional): index dict key.
    Returns:
        pd.DataFrame: dataframe
    """
    df = DataFrame(table)
    if key is not None:
        df = df.set_index(keys=key, drop=True).sort_index()
    return df


def to_json(obj: Any, **kwargs) -> bytes:
    """converts to JSON"""
    return orjson.dumps(obj, **kwargs)  # pylint: disable=no-member


def camel_to_snake(camel: str) -> str:
    """Convert CamelCase to snake_case"""
    # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    return re_pattern.sub("_", camel).lower()

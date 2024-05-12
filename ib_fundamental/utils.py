#!/usr/bin/env python3
"""
Created on Thu May 9 18:21:58 2021

@author: gonzo
"""
import re
from typing import Any

import orjson
from pandas import DataFrame, Index

re_pattern = re.compile(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")


def to_dataframe(table: list[dict], key: str = None, index: Index = None) -> DataFrame:
    """converts a list of dicts to a data frame

    Args:
        table (list(dict())): list of dicts
        key (str, optional): index dict key.
        index (pd.Index, optional): index to use. Defaults to None.

    Returns:
        pd.DataFrame: dataframe
    """
    df = DataFrame(table, index=index)
    if key is not None:
        df.set_index(keys=key, drop=True, inplace=True).sort_index()
    return df


def to_json(obj: Any, **kwargs) -> bytes:
    """converts to JSON"""
    return orjson.dumps(obj, **kwargs)


def camel_to_snake(camel: str) -> str:
    """Convert CamelCase to snake_case"""
    # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    return re_pattern.sub("_", camel).lower()

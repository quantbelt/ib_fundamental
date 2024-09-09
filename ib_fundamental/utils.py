#!/usr/bin/env python3
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
ib_fundamental utility functions
"""

import dataclasses
import datetime
import json
import re
from typing import Any, Optional

from ib_async import FundamentalRatios
from pandas import DataFrame, Index, concat

from .objects import StatementCode, StatementData, StatementMapping, statement_type

re_pattern = re.compile(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")


def to_dataframe(table: Any, key: Optional[str] = None) -> DataFrame:
    """converts a list of dicts to a data frame
    Args:
        table (list(dict())): list of dicts/dataclasses
        key (str, optional): index dict key.
    Returns:
        pd.DataFrame: dataframe
    """
    df = DataFrame(table)
    if key is not None:
        df = df.set_index(keys=key, drop=True).sort_index()
    return df


def camel_to_snake(camel: str) -> str:
    """Convert CamelCase to snake_case"""
    # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    return re_pattern.sub("_", camel).lower()


def to_json(obj: Any, **kwargs: Any) -> str:
    """Convert FundamentalData attributes to JSON"""

    class EnhancedJSONEncoder(json.JSONEncoder):
        """JSON encoder for dataclasses and datetime"""

        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            if isinstance(o, (datetime.date, datetime.datetime)):
                return o.isoformat()
            if isinstance(o, FundamentalRatios):
                return vars(o)

            return super().default(o)

    return json.dumps(obj, cls=EnhancedJSONEncoder, **kwargs)


def get_df_header(data: DataFrame, statement_code: StatementCode) -> DataFrame:
    """build header for pp"""
    idx: int = 6
    _header = data.iloc[:idx]
    _header = (
        _header.assign(line_id=range(idx))
        .assign(statement_type=statement_code)
        .reset_index()
        .rename(columns={"index": "map_item"})
    )
    return _header.assign(coa_item=_header["map_item"])


def join_df(data: DataFrame, header: DataFrame, mapping: DataFrame) -> DataFrame:
    """join data to present"""
    _pp = mapping.join(data, on="coa_item")
    _df = concat([header, _pp]).set_index("line_id")

    _names = _df.loc[
        _df.loc[:, "coa_item"] == "end_date", _df.columns[1:-2]
    ].values.tolist()[0]
    _l = _df.columns.to_list()
    _l[1:-2] = _names
    _df.columns = Index(_l)
    _df["statement_type"] = _df["statement_type"].map(lambda x: statement_type[x])
    _df = _df.drop(columns="coa_item").dropna()
    return _df


def build_statement(
    data: StatementData, statement_code: StatementCode, mapping: StatementMapping
) -> DataFrame:
    """build statement pp"""
    _map = to_dataframe(mapping)
    _map.coa_item = _map.coa_item.str.lower()
    #
    _data = to_dataframe(data).T.sort_index(axis=1, ascending=False)  # sort columns
    _header = get_df_header(data=_data, statement_code=statement_code)
    # pp
    return join_df(data=_data, header=_header, mapping=_map)

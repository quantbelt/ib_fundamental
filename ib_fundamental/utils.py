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
from pandas import DataFrame

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

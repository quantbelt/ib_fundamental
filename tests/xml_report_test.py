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

"""Test xml_report module"""

import pytest

from ib_fundamental.ib_client import IBClient
from ib_fundamental.xml_report import Element, XMLReport


class TestXMLReport:
    """Tests for XMLReport class"""

    def test_instantiation(self, xml_report):
        """Test XMLReport instantiation"""
        # act
        _report = xml_report
        # assert
        assert isinstance(_report, XMLReport)
        assert isinstance(_report.client, IBClient)

    def test_xml_report_property(self, xml_report_attrs):
        """Test XMLReport properties"""
        # act
        _attr = xml_report_attrs
        # assert
        assert isinstance(_attr, Element)

    def test_calendar(self, xml_report):
        """Test XMLReport.calendar"""
        # act
        with pytest.raises(ValueError) as exc_info:
            _ = xml_report.calendar()
        # assert
        assert exc_info.type == ValueError

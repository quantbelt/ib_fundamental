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

    def test_fin_statement(self, xml_report):
        """Test XMLReport.fin_statement"""
        # act
        _statement = xml_report.fin_statements
        # assert
        assert isinstance(_statement, Element)

    def test_fin_summary(self, xml_report):
        """Test XMLReport.fin_summary"""
        # act
        _statement = xml_report.fin_summary
        # assert
        assert isinstance(_statement, Element)

    def test_snapshot(self, xml_report):
        """Test XMLReport.snapshot"""
        # act
        _statement = xml_report.snapshot
        # assert
        assert isinstance(_statement, Element)

    def test_ownership(self, xml_report):
        """Test XMLReport.ownership"""
        # act
        _statement = xml_report.ownership
        # assert
        assert isinstance(_statement, Element)

    def test_resc(self, xml_report):
        """Test XMLReport.rest"""
        # act
        _statement = xml_report.resc
        # assert
        assert isinstance(_statement, Element)

    def test_calendar(self, xml_report):
        """Test XMLReport.calendar"""
        # act
        with pytest.raises(ValueError) as exc_info:
            _ = xml_report.calendar()
        # assert
        assert exc_info.type == ValueError

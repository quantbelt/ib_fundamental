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

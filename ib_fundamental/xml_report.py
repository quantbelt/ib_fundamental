#!/usr/bin/env python3
"""
Created on Fri Apr 30 16:21:58 2021

@author: gonzo
"""
# pylint: disable=attribute-defined-outside-init
from xml.etree.ElementTree import Element, fromstring

from .ib_client import IBClient

__all__ = [
    "XMLReport",
]


class XMLReport:
    """XML Report Cache"""

    def __init__(self, ib_client: IBClient):
        self.client = ib_client

    def __repr__(self):
        cls_name = self.__class__.__qualname__
        return f"{cls_name}(ib_client={self.client!r})"

    @property
    def fin_statements(self) -> Element:
        """Request financial statements"""
        try:
            return self.__fin_statements
        except AttributeError:
            self.__fin_statements = fromstring(
                self.client.ib_req_fund("ReportsFinStatements")
            )
            return self.__fin_statements

    @property
    def fin_summary(self) -> Element:
        """request financial summary"""
        try:
            return self.__fin_summary
        except AttributeError:
            self.__fin_summary = fromstring(
                self.client.ib_req_fund("ReportsFinSummary")
            )
            return self.__fin_summary

    @property
    def snapshot(self) -> Element:
        """request snapshot report"""
        try:
            return self.__snapshot
        except AttributeError:
            self.__snapshot = fromstring(self.client.ib_req_fund("ReportSnapshot"))
            return self.__snapshot

    @property
    def resc(self) -> Element:
        """request RESC"""
        try:
            return self.__resc
        except AttributeError:
            self.__resc = fromstring(self.client.ib_req_fund("RESC"))
            return self.__resc

    @property
    def ownership(self) -> Element:
        """request ReportsOwnership"""
        try:
            return self.__ownership
        except AttributeError:
            self.__ownership = fromstring(self.client.ib_req_fund("ReportsOwnership"))
            return self.__ownership

    @property
    def calendar(self) -> Element:
        """Calendar Report"""
        try:
            return self.__calendar
        except AttributeError:
            self.__calendar = fromstring(self.client.ib_req_fund("CalendarReport"))
            return self.__calendar

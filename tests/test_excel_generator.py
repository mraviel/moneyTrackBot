""" Test excel_generator class functions """
import pytest
from excel_generator import ExcelGen


class TestExcelGen:

    def setup_method(self, test_method):
        self.excel = ExcelGen('test_excel.xlsx')

    def teardown_method(self, test_method):
        pass

    def test_create_excel_no_data(self):
        """ Test create excel with no data (bug) """
        months_data = {}
        self.excel.create_excel(months_data)

    def test_create_excel_empty_data(self):
        """ Test create excel with empty data (bug) """
        months_data = {'JAN': [[], []], 'FEB': [[], []], 'MAR': [[], []], 'APR': [[], []], 'MAY': [[], []], 'JUN': [[], []], 'JUL': [[], []], 'AUG': [[], []], 'SEP': [[], []], 'OCT': [[], []]}
        self.excel.create_excel(months_data)

    def test_create_excel_only_income_data(self):
        """ Test create excel with only income data (bug) """
        months_data = {'JAN': [[], []], 'FEB': [[], [['משכורת', 5000]]], 'MAR': [[], []], 'APR': [[], []], 'MAY': [[], []], 'JUN': [[], []], 'JUL': [[], []], 'AUG': [[], []], 'SEP': [[], []], 'OCT': [[], []]}
        self.excel.create_excel(months_data)

    def test_create_excel_only_expenses_data(self):
        """ Test create excel with only expense data (bug) """
        months_data = {'JAN': [[], []], 'FEB': [['מכון', 230], []], 'MAR': [[], []], 'APR': [[], []], 'MAY': [[], []], 'JUN': [[], []], 'JUL': [[], []], 'AUG': [[], []], 'SEP': [[], []], 'OCT': [[], []]}
        self.excel.create_excel(months_data)

    def test_create_excel_one_month_data(self):
        """ Test create excel with one month data """
        months_data = {'JAN': [[], []], 'FEB': [[['אוכל', 230]], [['משכורת', 5000]]], 'MAR': [[], []], 'APR': [[], []], 'MAY': [[], []], 'JUN': [[], []], 'JUL': [[], []], 'AUG': [[], []], 'SEP': [[], []], 'OCT': [[], []]}
        self.excel.create_excel(months_data)

""" Test Processes file functions """
import pytest
import Processes as P


class TestProcesses:

    def test_Expense(self):
        """ Test possible values to Expense function """
        expenses_d = {
            'אוכל: 20 שח': {'subject': 'אוכל', 'total': 20.0, 'is_expense': True},
            'אוכל:20 שח': {'subject': 'אוכל', 'total': 20.0, 'is_expense': True},
            'אוכל: 20': {'subject': 'אוכל', 'total': 20.0, 'is_expense': True},
            'אוכל: ': None,
            'אוכל: שח': None,
            ': שח': None,
            ': 5': {'subject': '', 'total': 5.0, 'is_expense': True},  # Bug
            ':': None
        }

        income_d = {
            '+אוכל: 20 שח': {'subject': 'אוכל', 'total': 20.0, 'is_expense': False},
            '+אוכל:20 שח': {'subject': 'אוכל', 'total': 20.0, 'is_expense': False},
            '+אוכל: 20': {'subject': 'אוכל', 'total': 20.0, 'is_expense': False},
            '+אוכל: ': None,
            '+אוכל: שח': None,
            '+: שח': None,
            '+: 5': {'subject': '', 'total': 5.0, 'is_expense': False},  # Bug
            ':+': None
        }

        for value, expected in expenses_d.items():
            assert P.Expense(value) == expected

        for value, expected in income_d.items():
            assert P.Expense(value) == expected

    def test_create_months_data(self):

        assert P.create_months_data([], []) == {'JAN': [[], []], 'FEB': [[], []], 'MAR': [[], []], 'APR': [[], []], 'MAY': [[], []], 'JUN': [[], []], 'JUL': [[], []], 'AUG': [[], []], 'SEP': [[], []], 'OCT': [[], []]}

    def test_group_data(self):

        assert P.group_data({'אוכל'}, [['אוכל', 20], ['אוכל', 20]]) == [['אוכל', 40]]

        test = P.group_data({'אוכל', 'בית'}, [['אוכל', 20], ['אוכל', 20]])
        assert ['אוכל', 40] in test and ['בית', 0] in test

        test = P.group_data({'אוכל', 'בית'}, [['אוכל', 20], ['אוכל', 20], ['נסיעות', 5]])
        assert ['נסיעות', 5] not in test and ['אוכל', 40] in test and ['בית', 0] in test

        assert P.group_data(set(()), []) == []

    def test_convert_months_data_to_group(self):
        pass

    def test_get_expense_and_income_subjects_set(self):
        pass



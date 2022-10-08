import pandas as pd
import Processes as P
import math
from datetime import datetime
import os


def add_to_format(existing_format, dict_of_properties, workbook):
    """ Give a format you want to extend and a dict of the properties you want to
    extend it with, and you get them returned in a single format """
    new_dict = {}
    for key, value in existing_format.__dict__.items():
        if (value != 0) and (value != {}) and (value is not None):
            new_dict[key] = value
    del new_dict['escapes']

    l_new_dict_items = list(new_dict.items())
    l_dict_of_prp_items = list(dict_of_properties.items())

    format_dict = dict(l_new_dict_items + l_dict_of_prp_items)
    return workbook.add_format(format_dict)


def box(workbook, worksheet, row_start, col_start, row_stop, col_stop, fill=False):
    """ Makes an RxC box. Use integers, not the 'A1' format """

    rows = row_stop - row_start + 1
    cols = col_stop - col_start + 1

    # Total number of cells in the rectangle
    total = rows * cols

    for x in range(total):

        box_form = workbook.add_format()   # The format resets each loop
        row = row_start + (x // cols)
        column = col_start + (x % cols)

        if fill:
            box_form = add_to_format(box_form, {'border': 1}, workbook)
            worksheet.write(row, column, "", box_form)
            continue

        if x < cols:                     # If it's on the top row
            box_form = add_to_format(box_form, {'top': 2}, workbook)
        if x >= ((rows * cols) - cols):    # If it's on the bottom row
            box_form = add_to_format(box_form, {'bottom': 2}, workbook)
        if x % cols == 0:                  # If it's on the left column
            box_form = add_to_format(box_form, {'left': 2}, workbook)
        if x % cols == (cols - 1):         # If it's on the right column
            box_form = add_to_format(box_form, {'right': 2}, workbook)

        worksheet.write(row, column, "", box_form)


class ExcelGen:

    """ Create Excel file.
        To Create the file use only the function create_excel with months_data as argument """

    def __init__(self, file_location):

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        self.writer = pd.ExcelWriter(f'{file_location}', engine='xlsxwriter')

        self.workbook = self.writer.book

        # Define all formats
        self.month_title_format = self.workbook.add_format()
        self.subject_amount_title_format = self.workbook.add_format({'border': 1})
        self.subject_format = self.workbook.add_format({'border': 1})
        self.amount_format = self.workbook.add_format({'border': 1, 'num_format': '0.00'})
        self.expense_income_title_format = self.workbook.add_format({'border': 1, 'font_size': 20, 'bg_color': 'yellow'})
        self.expense_income_format = self.workbook.add_format()
        self.total_format = self.workbook.add_format()
        self.color_row = self.workbook.add_format({'bg_color': 'gray'})
        self.month_year_format = self.workbook.add_format({'border': 1})
        self.addition_data_format = self.workbook.add_format({'border': 1, 'num_format': '0.00'})
        self.percent_format = self.workbook.add_format({'num_format': '0%', 'border': 1})

        # Generate formats
        self.generate_formats()

    def generate_formats(self):
        """ Generate all formats to use """
        self.month_title_format.set_font_size(20)
        self.subject_amount_title_format.set_bold()
        self.addition_data_format.set_bold()
        self.percent_format.set_bold()

    def write_month_expenses(self, l_exp, month):
        """ Args: l_exp: list of expenses [[subject, amount], [...], ...]
                  month: short month name, ex: AUG ...
                  Add the data from l_exp to month sheet expenses section """

        worksheet = self.writer.sheets[month]

        # Add box border
        box(self.workbook, worksheet, 2, 0, len(l_exp) + 7, 3, fill=True)

        # Add Subject and Amount again
        worksheet.write('A3', 'Subjects', self.subject_amount_title_format)
        worksheet.write('B3', 'Amount', self.subject_amount_title_format)

        index = 4
        for exp in l_exp:
            subject = exp[0]
            amount = exp[1]
            worksheet.write(index, 0, subject, self.subject_format)
            worksheet.write(index, 1, amount, self.amount_format)

            index += 1

        # Color final row
        worksheet.merge_range(f'A{index+1}:D{index+1}', "Total", self.color_row)

        # Sum all expenses
        worksheet.write(index+2, 0, 'סה״כ הוצאות', self.subject_format)
        worksheet.write(index+2, 1, f'=SUM(B5:B{index})', self.amount_format)

    def write_month_income(self, l_inc, month):
        """ Args: l_inc: list of income [[subject, amount], [...], ...]
                  month: short month name, ex: AUG ...
                  Add the data from l_inc to month sheet income section """

        worksheet = self.writer.sheets[month]

        # Add box border
        box(self.workbook, worksheet, 2, 7, len(l_inc) + 7, 10, fill=True)

        # Add Subject and Amount again
        worksheet.write('H3', 'Subjects', self.subject_amount_title_format)
        worksheet.write('I3', 'Amount', self.subject_amount_title_format)

        index = 4
        for exp in l_inc:
            subject = exp[0]
            amount = exp[1]
            worksheet.write(index, 7, subject, self.subject_format)
            worksheet.write(index, 8, amount, self.amount_format)

            index += 1

        # Color final row
        worksheet.merge_range(f'H{index + 1}:K{index + 1}', "Total", self.color_row)

        # Sum all income
        worksheet.write(index + 2, 7, 'סה״כ הכנסות', self.subject_format)
        worksheet.write(index + 2, 8, f'=SUM(I5:I{index})', self.amount_format)

    def write_year_expenses(self, months_data_group: dict, subjects_index: dict):
        """ Args: months_data_group: (dict)
                 subjects_index: (dict) store subjects and there y pos index ex: {subject: 5}
                 Add the data from months_data_group to year sheet expenses section """

        worksheet = self.writer.sheets['YEAR']
        months_list = ["YEAR", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
        months_with_data = months_data_group.keys()

        # Write the shield which will be over writen
        x_limit = len(months_list)
        y_limit = max(list(subjects_index.values())) + 4
        y_min = min(list(subjects_index.values()))
        for x in range(1, x_limit):
            for y in range(y_min, y_limit + 1):
                worksheet.write(y, x, "", self.amount_format)

        # Write the shield which will be over writen
        x_limit = len(months_list)
        y_limit = max(list(subjects_index.values()))
        y_min = min(list(subjects_index.values()))
        for x in range(1, x_limit):
            for y in range(y_min, y_limit + 1):
                worksheet.write(y, x, 0.00, self.amount_format)

        # Fill the data
        index_x = 0
        for month in months_list:
            if month in months_with_data:
                for expense in months_data_group[month][0]:
                    subject = expense[0]
                    amount = expense[1]
                    index_y = subjects_index[subject]
                    worksheet.write(index_y, index_x, amount, self.amount_format)

            # each month on different x pos
            index_x += 1

    def write_year_income(self, months_data_group: dict, subjects_index: dict):
        """ Args: months_data_group: (dict)
                 subjects_index: (dict) store subjects and there y pos index ex: {subject: 5}
                 Add the data from months_data_group to year sheet income section """

        worksheet = self.writer.sheets['YEAR']
        months_list = ["YEAR", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
        months_with_data = months_data_group.keys()

        # Write the shield which will be over writen
        x_limit = len(months_list)
        y_limit = max(list(subjects_index.values())) + 4
        y_min = min(list(subjects_index.values()))
        for x in range(1, x_limit):
            for y in range(y_min, y_limit + 1):
                worksheet.write(y, x, "", self.amount_format)

        # Write the shield which will be over writen
        x_limit = len(months_list)
        y_limit = max(list(subjects_index.values()))
        y_min = min(list(subjects_index.values()))
        for x in range(1, x_limit):
            for y in range(y_min, y_limit+1):
                worksheet.write(y, x, 0.00, self.amount_format)

        index_x = 0
        for month in months_list:
            if month in months_with_data:
                for income in months_data_group[month][1]:
                    subject = income[0]
                    amount = income[1]
                    index_y = subjects_index[subject]
                    worksheet.write(index_y, index_x, amount, self.amount_format)

            # each month on different x pos
            index_x += 1

    def write_year_summary(self, index_y: int, sum_y: list):
        """ Args: index_y: (int) y pos for summary location
                  sum_y: (list) [income_sum_y_pos, expense_sum_y_pos]
                  Add the data from months_data_group to year sheet expenses section """

        worksheet = self.writer.sheets['YEAR']
        months_list = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

        # Write the shield which will be over writen
        x_limit = len(months_list) + 3
        y_limit = index_y + 5
        y_min = index_y
        for x in range(0, x_limit):
            for y in range(y_min, y_limit + 1):
                worksheet.write(y, x, "", self.amount_format)

        # Inset months to table
        index_x = 1
        for month in months_list:
            worksheet.write(y_min, index_x, month, self.month_year_format)
            index_x += 1

        worksheet.write(y_min, index_x, 'סה״כ השנה', self.month_year_format)
        worksheet.write(y_min, index_x+1, 'ממוצע חודשי', self.month_year_format)

        # Color final row
        # worksheet.merge_range(f'B{y_min+2}:O{y_min+2}', "Total", self.color_row)

        subjects = ['סה״כ הכנסות', 'סה״כ הוצאות', 'סה״כ חסכון', 'אחוז חיסכון']

        for subject in subjects:
            y_pos = subjects.index(subject) + 1 + y_min
            worksheet.write(y_pos, 0, subject, self.subject_format)

        # Insert the summary data
        income_sum_y = sum_y[0]
        expense_sum_y = sum_y[1]
        l = ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]

        for x_pos in l:
            worksheet.write(y_min+1, l.index(x_pos)+1, f'={x_pos}{income_sum_y}', self.addition_data_format)

        for x_pos in l:
            worksheet.write(y_min+2, l.index(x_pos)+1, f'={x_pos}{expense_sum_y}', self.addition_data_format)

        for x_pos in l:
            formula = f'={x_pos}{income_sum_y}-{x_pos}{expense_sum_y}'
            worksheet.write(y_min+3, l.index(x_pos)+1, formula, self.addition_data_format)

        revenue_y = y_min + 4
        for x_pos in l:
            formula = f'=IFERROR({x_pos}{revenue_y}/{x_pos}{income_sum_y}, 0)'
            worksheet.write(y_min+4, l.index(x_pos)+1, formula, self.percent_format)

    def additional_year_data(self, index_y, min_y, max_y, len_subjects, main_type):
        """ Args: index_y, min_y, max_y: y positions
                   len_subjects: len of subjects
                   main_type: income/expense
                   Add additional year data such as SUM/AVG of expenses or income """

        worksheet = self.writer.sheets['YEAR']

        d = {"Income": 4, "Expense": 18}
        self.add_sum_year(len_subjects, d[main_type])
        self.add_avg_year(len_subjects, d[main_type])

        # Write sum
        worksheet.write(index_y, 0, "סה״כ", self.subject_format)
        l = ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]
        index_x = 1
        for i in l:
            sum_formula = f'=SUM({i}{min_y}:{i}{max_y})'
            worksheet.write(index_y, index_x, sum_formula, self.addition_data_format)
            index_x += 1

    def add_sum_year(self, len_subjects, y_pos):
        """ Args: len_subjects: (int), y_pos: (int)
            Write the sum year addition data """

        worksheet = self.writer.sheets['YEAR']
        x_pos = 13
        # Write the head AVG
        worksheet.write(y_pos-1, x_pos, "סה״כ", self.subject_format)
        for i in range(len_subjects):
            sum_formula = f'=SUM(B{y_pos+1}:M{y_pos+1})'
            worksheet.write(y_pos, x_pos, sum_formula, self.addition_data_format)
            y_pos += 1

    def add_avg_year(self, len_subjects, y_pos):
        """ Args: len_subjects: (int), y_pos: (int)
            Write the sum year addition data """

        worksheet = self.writer.sheets['YEAR']
        x_pos = 14
        # Write the head AVG
        worksheet.write(y_pos-1, x_pos, "ממוצע חודשי", self.subject_format)
        for i in range(len_subjects):
            sum_formula = f'=AVERAGE(B{y_pos+1}:M{y_pos+1})'
            worksheet.write(y_pos, x_pos, sum_formula, self.addition_data_format)
            y_pos += 1

    def current_worksheet(self, sheet_name):
        """ Return the current worksheet """
        return self.writer.sheets[sheet_name]

    def create_all_sheets(self):
        """ Create all the template sheets for each month + year + analysis"""

        list_name = ["YEAR", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

        for sheet_name in list_name:
            worksheet = self.workbook.add_worksheet(sheet_name)
            worksheet.write('N1', sheet_name, self.month_title_format)

            if sheet_name == "YEAR":
                continue

            # Expenses Section
            worksheet.merge_range('A1:B1', "Expenses", self.expense_income_title_format)
            worksheet.write('A3', 'Subjects', self.subject_amount_title_format)
            worksheet.write('B3', 'Amount', self.subject_amount_title_format)
            # Income Section
            worksheet.merge_range('H1:I1', "Income", self.expense_income_title_format)
            worksheet.write('H3', 'Subjects', self.subject_amount_title_format)
            worksheet.write('I3', 'Amount', self.subject_amount_title_format)

        # Create Analysis Sheet
        worksheet = self.workbook.add_worksheet("Analysis")

    def create_month_excel(self, month: str, l_exp: list, l_inc: list, subjects_set: dict):
        """ Args: month: (str),
                  l_exp, l_inc: (list) of expenses/ income ex: [[subject: amount], [...], ...]
                  subjects_set: (dict) store all group subjects for income and expenses (income/expenses_set)
            Generate month Excel sheet for current month"""

        month = month.upper()
        self.write_month_expenses(l_exp, month)
        self.write_month_income(l_inc, month)

        # Write Total Income - Total expenses
        total_expenses_y = len(l_exp) + 7
        total_income_y = len(l_inc) + 7

        worksheet = self.writer.sheets[month]
        worksheet.write(total_income_y + 2, 7, 'סה״כ הכנסות פחות הוצאות', self.addition_data_format)
        worksheet.write(total_income_y + 2, 8, f'=SUM(-B{total_expenses_y}, I{total_income_y})', self.addition_data_format)

        # Create month charts only if there is data to present
        if l_exp or l_inc:
            chart1 = self.create_month_chart1(month, l_exp, l_inc, subjects_set)
            chart2 = self.create_month_chart2(month, l_exp, l_inc)
            worksheet.insert_chart(f'F{total_income_y + 6}', chart1)
            worksheet.insert_chart(f'P{total_income_y + 6}', chart2)

    def create_month_chart1(self, month: str, exp_subjects, inc_subjects, subjects_set: dict):
        """ Args: month: (str)
                  subjects_set: (dict) store all group subjects for income and expenses (income/expenses_set)
        Return chart object for month sheet """

        months = ["YEAR", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

        # Get the year len of expenses subjects for values pos chart
        expenses_subjects_set = subjects_set['expense_set']
        income_subjects_set = subjects_set['income_set']
        total_year_expenses_subjects = len(expenses_subjects_set)
        total_year_income_subjects = len(income_subjects_set)

        start_y_pos = total_year_income_subjects + 17
        end_y_pos = start_y_pos + total_year_expenses_subjects - 1

        chart = self.workbook.add_chart({'type': 'column'})

        chart.add_series({
            'name': 'סה״כ הוצאות לפי נושא',
            'categories': ['YEAR', start_y_pos, 0, end_y_pos, 0],
            'values': ['YEAR', start_y_pos, months.index(month), end_y_pos, months.index(month)]
        })

        return chart

    def create_month_chart2(self, month, exp_subjects: list, inc_subjects: list):

        """ Args: month: (str)
                  exp_subjects: (list) store all group subjects for expenses
                  inc_subjects: (list) store all group subjects for income
            Return chart object for month sheet """

        total_inc_pos = len(inc_subjects) + 6
        total_exp_pos = len(exp_subjects) + 6
        total_saving_pos = total_inc_pos + 3

        chart = self.workbook.add_chart({'type': 'column'})

        chart.add_series({
            'name': 'סה״כ הוצאות',
            'values': [month, total_exp_pos, 1, total_exp_pos, 1],
            'color': 'red'
        })
        chart.add_series({
            'name': 'סה״כ הכנסות',
            'values': [month, total_inc_pos, 8, total_inc_pos, 8],
            'color': 'blue'
        })
        chart.add_series({
            'name': 'סה״כ חיסכון',
            'values': [month, total_saving_pos, 8, total_saving_pos, 8],
            'color': 'green'
        })

        return chart

    def create_year_excel(self, months_data_group: dict):
        """ Args: months_data_group (dict): months as keys, Like the var: months_data but as a group subjects,
                months_data_group = total for each subject
            Create the year Excel sheet """

        # Can use for keep track of where expense is located (list is organize)
        d = P.get_expense_and_income_subjects_set(months_data_group)
        data_for_charts = {}

        months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

        # months = months_data_group.keys()
        worksheet = self.writer.sheets['YEAR']

        # Income Section
        worksheet.merge_range('A1:B1', "Income", self.expense_income_title_format)

        index_x = 1
        for month in months:
            worksheet.write(3, index_x, month, self.month_year_format)
            index_x += 1

        subjects_indexes = {}
        index_y = 4
        for income in d['income_set']:
            worksheet.write(index_y, 0, income, self.subject_format)
            subjects_indexes[income] = index_y
            index_y += 1

        # Fill income data here
        self.write_year_income(months_data_group, subjects_indexes)

        # Color final row
        worksheet.merge_range(f'B{index_y + 2}:O{index_y + 2}', "Total", self.color_row)

        # Save data for charts column
        data_for_charts['Income'] = [3, d['income_set']]

        index_y += 2
        min_y = min(list(subjects_indexes.values())) + 1
        max_y = max(list(subjects_indexes.values())) + 1
        len_subjects = len(subjects_indexes)
        income_sum_y_pos = index_y+1
        self.additional_year_data(index_y, min_y, max_y, len_subjects, 'Income')

        index_y += 8
        # Expenses Section
        worksheet.merge_range(f'A{index_y}:B{index_y}', "Expenses", self.expense_income_title_format)

        index_y += 2
        index_x = 1
        months_y = index_y
        for month in months:
            worksheet.write(months_y, index_x, month, self.month_year_format)
            index_x += 1

        subjects_indexes = {}
        index_y += 1
        for expenses in d['expense_set']:
            worksheet.write(index_y, 0, expenses, self.subject_format)
            subjects_indexes[expenses] = index_y
            index_y += 1

        # Fill expenses data here
        self.write_year_expenses(months_data_group, subjects_indexes)

        # Color final row
        worksheet.merge_range(f'B{index_y +2}:O{index_y + 2}', "Total", self.color_row)

        # Save data for charts column
        data_for_charts['Expense'] = [months_y, d['expense_set']]

        index_y += 2
        min_y = min(list(subjects_indexes.values())) + 1
        max_y = max(list(subjects_indexes.values())) + 1
        len_subjects = len(subjects_indexes)
        expense_sum_y_pos = index_y+1
        self.additional_year_data(index_y, min_y, max_y, len_subjects, 'Expense')

        # Write the summary section
        # Income Section
        index_y += 7
        worksheet.merge_range(f'A{index_y}:B{index_y}', "Summary", self.expense_income_title_format)

        index_y += 2
        self.write_year_summary(index_y, [income_sum_y_pos, expense_sum_y_pos])

        # Save data for charts column
        total_subjects = ['סה״כ הכנסות', 'סה״כ הוצאות', 'סה״כ חסכון', 'אחוז חיסכון']
        data_for_charts['Summary'] = [index_y, total_subjects]

        # Create year chart in Analysis Sheet
        self.create_year_charts(data_for_charts)

    def create_year_charts(self, d: dict):
        """ Create charts with info from year sheet in Analysis sheet
            Args: dict {'Income': [months_index_y, subjects], 'Expense':[...], 'Summary':[...]} """

        # Income Charts
        income_y_pos, income_total_subjects = d['Income']
        income_charts = self._generate_year_chart(income_y_pos, income_total_subjects)

        # Expense Charts
        expense_y_pos, expense_total_subjects = d['Expense']
        expenses_charts = self._generate_year_chart(expense_y_pos, expense_total_subjects)

        # Summary Charts
        summary_y_pos, summary_total_subjects = d['Summary']
        summary_charts = self._generate_year_chart(summary_y_pos, summary_total_subjects)

        # Merge Charts
        merge_expenses_chart = self._generate_merge_year_chart(expense_y_pos, expense_total_subjects, 'הוצאות לפי חודש')
        merge_income_charts = self._generate_merge_year_chart(income_y_pos, income_total_subjects, 'הכנסות לפי חודש')

        all_charts = income_charts + expenses_charts + summary_charts
        all_charts.append(merge_expenses_chart)
        all_charts.append(merge_income_charts)

        # Insert chart to Analysis sheet
        worksheet = self.writer.sheets['Analysis']
        x_pos = ['B', 'K', 'T']
        for y in range(0, math.ceil(len(all_charts) / 3)):
            for x in x_pos:
                if not all_charts:
                    break
                chart = all_charts.pop()
                worksheet.insert_chart(f'{x}{(y+1)*20}', chart)

    def _generate_year_chart(self, year_y_pos, subjects):
        """ Generate charts with info from year sheet
                    Args: year_y_pos, subjects
                    Return list with charts objects """

        charts = []
        month_index_y = year_y_pos
        for subject in subjects:
            chart = self.workbook.add_chart({'type': 'line'})

            chart.add_series({
                'categories': ['YEAR', month_index_y, 1, month_index_y, 12],
                'values': ['YEAR', year_y_pos + 1, 1, year_y_pos + 1, 12]
            })

            chart.set_x_axis(
                {'name': 'Months', 'position_axis': 'on_tick', 'text_axis': True})
            chart.set_y_axis({'name': f'{subject}', 'major_gridlines': {'visible': False}})

            chart.set_legend({'position': 'none'})

            charts.append(chart)
            year_y_pos += 1

        return charts

    def _generate_merge_year_chart(self, year_y_pos, subjects, chart_name):

        month_index_y = year_y_pos

        chart = self.workbook.add_chart({'type': 'line'})

        for subject in subjects:
            chart.add_series({
                'name': ['YEAR', year_y_pos + 1, 0, year_y_pos + 1, 0],
                'categories': ['YEAR', month_index_y, 1, month_index_y, 12],
                'values': ['YEAR', year_y_pos + 1, 1, year_y_pos + 1, 12],
                'marker': {'type': 'circle'},
            })

            year_y_pos += 1

        chart.set_x_axis(
            {'name': 'Months', 'position_axis': 'on_tick', 'text_axis': True})
        chart.set_y_axis({'name': chart_name, 'major_gridlines': {'visible': False}})

        chart.set_legend({'position': 'none'})

        return chart

    def create_excel(self, months_data: dict):
        """ Args: months_data: (dict) months as keys, each month store list with income and expenses
                  ex: {..., 'AUG': [[[subject, amount], [...], ...], [subject, amount], ...], 'SEP': ..., ...}
            Generate all data and insert to Excel file """

        # Create the template excel
        self.create_all_sheets()

        months_data_group = P.convert_months_data_to_group(months_data=months_data)
        subjects_set = P.get_expense_and_income_subjects_set(months_data_group)

        for month, data in months_data.items():
            l_exp = data[0]
            l_inc = data[1]

            # Generate all months
            self.create_month_excel(month, l_exp, l_inc, subjects_set)

        # Generate year excel
        self.create_year_excel(months_data_group)

        # Close the Pandas Excel writer and output the Excel file.
        self.workbook.close()


if __name__ == '__main__':
    pass

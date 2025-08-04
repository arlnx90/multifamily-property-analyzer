import numpy
import pandas as pd
import matplotlib.pyplot as plt
import csv
import math
import requests
import os
array_zip_code_usps = numpy.genfromtxt('zip_code_info_usps.csv', delimiter=',', usecols=numpy.arange(0, 10))
list_zip = array_zip_code_usps[:, 4]
array_zcta = numpy.genfromtxt('zip_to_zcta_hrsa.csv', delimiter= ',', usecols= numpy.arange(0,5))
list_fordict_zip = array_zcta[:, 0]
list_fordict_zcta = array_zcta[:, 4]
dict_zip_to_zcta = dict(zip(list_fordict_zip, list_fordict_zcta))
zcta = None
folder_path = None
apikey = None
line_prop_info = []
period_type = None
list_prop_line_item_det = ['Year',
                           'Revenue - Rental',
                           'Revenue - Other',
                           'Property Tax',
                           'Insurance',
                           'General & Administrative Expense',
                           'Management Expense',
                           'Salaries/Wages',
                           'Advertising & Marketing',
                           'Utilities',
                           'Repairs & Maintenance',
                           'Other Operating Expense',
                           'Reserves',
                           'Non-Operating Expense',
                           'Datevalue',
                           'Year',
                           'Month']
dict_val_to_month = {
    '01': 'Jan',
    '02': 'Feb',
    '03': 'Mar',
    '04': 'Apr',
    '05': 'May',
    '06': 'Jun',
    '07': 'Jul',
    '08': 'Aug',
    '09': 'Sep',
    '1': 'Jan',
    '2': 'Feb',
    '3': 'Mar',
    '4': 'Apr',
    '5': 'May',
    '6': 'Jun',
    '7': 'Jul',
    '8': 'Aug',
    '9': 'Sep',
    '10': 'Oct',
    '11': 'Nov',
    '12': 'Dec'}
row_y0 = []
row_m0 = []
num_periods = 0
line_item_num_ref = numpy.arange(0, 14)
dict_line_item_ref = dict(zip(line_item_num_ref, list_prop_line_item_det))
color_main = 'darkcyan'
color_secondary = 'paleturquoise'


def welcome():
    print('''
Hello and welcome to Multifamily Project Analyzer

This program is a CRE analyzer for
multifamily property performance and valuation.

The program will produce charts, tables,
and analysis for internal and external
use.

Further information can be found in the 
txt file in the download folder.

Let's get started. 
____________________________________________________''')


def csv_blank_property_inc():
    global period_type
    global num_periods
    global row_y0
    global row_m0
    dict_month_valid = {
        'January': 'Jan',
        'JANUARY': 'Jan',
        'january': 'Jan',
        'Jan': 'Jan',
        'JAN': 'Jan',
        'jan': 'Jan',
        '1': 'Jan',
        '01': 'Jan',
        'February': 'Feb',
        'FEBRUARY': 'Feb',
        'february': 'Feb',
        'Feb': 'Feb',
        'FEB': 'Feb',
        'feb': 'Feb',
        '2': 'Feb',
        '02': 'Feb',
        'March': 'Mar',
        'MARCH': 'Mar',
        'march': 'Mar',
        'Mar': 'Mar',
        'MAR': 'Mar',
        'mar': 'Mar',
        '3': 'Mar',
        '03': 'Mar',
        'April': 'Apr',
        'APRIL': 'Apr',
        'april': 'Apr',
        'Apr': 'Apr',
        'APR': 'Apr',
        'apr': 'Apr',
        '4': 'Apr',
        '04': 'Apr',
        'May': 'May',
        'MAY': 'May',
        'may': 'May',
        '5': 'May',
        '05': 'May',
        'June': 'Jun',
        'JUNE': 'Jun',
        'june': 'Jun',
        'Jun': 'Jun',
        'JUN': 'Jun',
        'jun': 'Jun',
        '6': 'Jun',
        '06': 'Jun',
        'July': 'Jul',
        'JULY': 'Jul',
        'july': 'Jul',
        'Jul': 'Jul',
        'JUL': 'Jul',
        'jul': 'Jul',
        '7': 'Jul',
        '07': 'Jul',
        'August': 'Aug',
        'AUGUST': 'Aug',
        'august': 'Aug',
        'Aug': 'Aug',
        'AUG': 'Aug',
        'aug': 'Aug',
        '8': 'Aug',
        '08': 'Aug',
        'September': 'Sep',
        'SEPTEMBER': 'Sep',
        'september': 'Sep',
        'Sep': 'Sep',
        'SEP': 'Sep',
        'sep': 'Sep',
        '9': 'Sep',
        '09': 'Sep',
        'October': 'Oct',
        'OCTOBER': 'Oct',
        'october': 'Oct',
        'Oct': 'Oct',
        'OCT': 'Oct',
        'oct': 'Oct',
        '10': 'Oct',
        'November': 'Nov',
        'NOVEMBER': 'Nov',
        'november': 'Nov',
        'Nov': 'Nov',
        'NOV': 'Nov',
        'nov': 'Nov',
        '11': 'Nov',
        'December': 'Dec',
        'DECEMBER': 'Dec',
        'december': 'Dec',
        'Dec': 'Dec',
        'DEC': 'Dec',
        'dec': 'Dec',
        '12': 'Dec'}
    dict_month_to_val = {
        'Jan': '1',
        'Feb': '2',
        'Mar': '3',
        'Apr': '4',
        'May': '5',
        'Jun': '6',
        'Jul': '7',
        'Aug': '8',
        'Sep': '9',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'}
    while True:
        dict_period_type = {
            'M': 'monthly',
            'm': 'monthly',
            'A': 'annual',
            'a': 'annual'
        }
        while True:
            period_choice = input('''
    What type of data do you have:
        [M] - Monthly
        [A] - Annual

        Please choose one. ''')
            if period_choice in dict_period_type:
                break
            else:
                print('''
    (ERROR) Invalid Response - Please type either M or A and press enter.''')
        print('''
    Now you will input the date range for your data.
    You must have at least 3 periods of data. ''')
        period_type = dict_period_type[period_choice]
        year_start = None  # year and month values used for generation of blank inc statement
        year_end = None
        #month_start = None
        #month_end = None
        month_start_val = None
        month_end_val = None
        month_year_start_val = None  # month_year_xx_val year integer with 0.xx float representing month
        month_year_end_val = None
        if period_type == 'annual':  # annual periodization
            while True:
                year_start = input('''
        What is the START year (oldest) for your data? ''')
                try:
                    int(year_start)
                except ValueError:
                    print('''
    Invalid Response - Year must be an integer between 1900 - 2050. ''')
                    continue
                if 1900 <= int(year_start) <= 2050:
                    break
                else:
                    print('''
    Invalid Response - Year must be an integer between 1900 - 2050. ''')
            while True:
                year_end = input('''
        What is the END year (newest) for your data? ''')
                try:
                    int(year_end)
                except ValueError:
                    print('''
    Invalid Response - Year must be an integer between 1900 - 2050. ''')
                    continue
                if 1900 <= int(year_end) <= 2050 and int(year_end) > int(year_start):
                    break
                else:
                    print('''
    Invalid Response - Year must be an integer between 1900 - 2050, and
    End Year must be greater than Start Year''')
        if period_type == 'monthly':  # monthly periodization
            while True:
                while True:
                    year_start = input('''
        What is the START year (oldest) for your data? ''')
                    try:
                        int(year_start)
                    except ValueError:
                        print('''
    Invalid Response - Year must be an integer between 1900 - 2050. ''')
                        continue
                    if 1900 <= int(year_start) <= 2050:
                        break
                    else:
                        print('''
    Invalid Response - Year must be an integer between 1900 - 2050. ''')
                while True:
                    month_start_inp = input('''
        What is the START month (oldest) for your data? ''')
                    try:
                        dict_month_valid[month_start_inp]
                    except KeyError:
                        print('''
    Invalid Response - Must be a valid month. ''')
                        continue
                    month_start = dict_month_valid[month_start_inp]
                    month_start_val = dict_month_to_val[month_start]
                    month_year_start_val = float(year_start) + (float(int(month_start_val) / 100))
                    break
                while True:
                    year_end = input('''
        What is the END year (newest) for your data? ''')
                    try:
                        int(year_end)
                    except ValueError:
                        print('''
    Invalid Response - Year must be an integer between 1900 - 2050. ''')
                    if 1900 <= int(year_end) <= 2050 and int(year_end) >= int(year_start):
                        break
                    else:
                        print('''
    Invalid Response - Year must be an integer between 1900 - 2050, and
    End Year must be greater than Start Year ''')
                while True:
                    month_end_inp = input('''
        What is the END month (newest) for your data?''')
                    try:
                        dict_month_valid[month_end_inp]
                    except KeyError:
                        print('''
    Invalid Response - Must be a valid month. ''')
                        continue
                    month_end = dict_month_valid[month_end_inp]
                    month_end_val = dict_month_to_val[month_end]
                    month_year_end_val = float(year_end) + float(int(month_end_val) / 100)
                    break
                if month_year_start_val <= month_year_end_val:
                    break
                else:
                    print('''
    Invalid input. End date must be after start date. ''')
        #num_periods = None  # number of total periods for monthly & annual; used for appending 0's for line items; used for validation user filled csv
        #list_periods_yy = []  # all list_periods_xx used for header rows in either annual (1 row) or monthly (3 rows)
        list_periods_my = []
        list_periods_mm = []
        list_periods_mdval = []
        row_1 = [(list_prop_line_item_det[1])] # rows defined for blank csv to be written
        row_2 = [(list_prop_line_item_det[2])]
        row_3 = [(list_prop_line_item_det[3])]
        row_4 = [(list_prop_line_item_det[4])]
        row_5 = [(list_prop_line_item_det[5])]
        row_6 = [(list_prop_line_item_det[6])]
        row_7 = [(list_prop_line_item_det[7])]
        row_8 = [(list_prop_line_item_det[8])]
        row_9 = [(list_prop_line_item_det[9])]
        row_10 = [(list_prop_line_item_det[10])]
        row_11 = [(list_prop_line_item_det[11])]
        row_12 = [(list_prop_line_item_det[12])]
        row_13 = [(list_prop_line_item_det[13])]
        list_rows_prop_inc_det = [row_1, row_2, row_3, row_4, row_5, row_6, row_7,
                                  row_8, row_9, row_10, row_11, row_12, row_13]
        row_y0 = []
        row_m0 = []
        row_y0.extend([(list_prop_line_item_det[0])])
        row_m0.extend([(list_prop_line_item_det[14])])
        row_m1 = []
        row_m2 = []
        row_m1.extend([(list_prop_line_item_det[15])])
        row_m2.extend([(list_prop_line_item_det[16])])
        num_periods = 0
        if period_type == 'annual':  # annual number of periods and period headers
            num_periods = int(year_end) - int(year_start) + 1
            list_periods_yy = (numpy.arange(int(year_start), (int(year_end) + 1))).tolist()
            row_y0.extend(list_periods_yy)
        if period_type == 'monthly':  # monthly number of periods and period headers
            num_periods = ((int(year_end) - int(year_start)) * 12) + (int(month_end_val)) - (int(month_start_val)) + 1
            checksum_periods = 0
            last_value_monthyearval = month_year_start_val
            while checksum_periods < num_periods:
                list_periods_my.append(str(math.trunc(last_value_monthyearval)))
                list_periods_mm.append(dict_val_to_month[str(round(
                    (last_value_monthyearval - math.trunc(last_value_monthyearval)) * 100))])
                list_periods_mdval.append(str(last_value_monthyearval))
                if dict_val_to_month[
                    str(round((last_value_monthyearval - math.trunc(last_value_monthyearval)) * 100))] == 'Dec':
                    last_value_monthyearval = last_value_monthyearval - 0.11 + 1
                else:
                    last_value_monthyearval = last_value_monthyearval + 0.01
                checksum_periods += 1
            row_m0.extend(list_periods_mdval)
            row_m1.extend(list_periods_my)
            row_m2.extend(list_periods_mm)
        if num_periods >= 3:
            break
        else:
            print('''
Error - Data must include at least 3 time periods. ''')
    zeroes = list((str(0) * num_periods))
    for row in list_rows_prop_inc_det:
        row.extend(zeroes)
    with open('property_inc_stmnt.csv', 'w') as f_prop_inc:
        writer = csv.writer(f_prop_inc, delimiter=',')
        if period_type == 'annual':
            writer.writerow(row_y0)
        if period_type == 'monthly':
            writer.writerow(row_m0)
            writer.writerow(row_m1)
            writer.writerow(row_m2)
        writer.writerows(list_rows_prop_inc_det)
    print('''
_________________________________________________________________________________________________________________
A CSV file has been created in this folder with the name:
<<< property_inc_stmnt.csv >>>

Please open this file and input your data.
Use whole dollar amounts.

If you are not familiar with CSV format, the easiest way
to input your data is to open the file with a spreadsheet
program (such as MS Excel, LibreOffice Calc, etc.).

Do NOT choose "fixed width" under delimiter/separator options.
The option should be selected for "comma" under a "separated by" or similarly titled category.

Do NOT delete or modify line item labels or period labels.
0's have been automatically filled into each cell. You do not have to change or delete these 0's.
Any cells left blank will be interpreted as 0. 

_________________________________________________________________________________________________________________
<<< After Entering Your Data >>>
Save the file. Do NOT change the name of the file. Make sure the file is saved as a CSV file (ending in .csv)
Then, respond to the following question:
_________________________________________________________________________________________________________________''')
    return period_type, row_y0, row_m0, num_periods


def property_info(): #prop name, zip, unit mix, expected rent
    global zcta
    global line_prop_info
    global folder_path
    while True:
        prop_name = input('''
    What is the name of your property of interest?
    The name can be any name or number you want, except a blank space. ''')
        if prop_name != '':
            break
        else:
            print('''
Invalid Input - Name cannot be a blank space. ''')
            continue
    while True:
        prop_zip = input('''
    What is the zip code of the property?
    Must be five (5) digit zip code. ''')
        try:
            int(prop_zip)
        except ValueError:
            print('''
Invalid Input - Zip Code must be a number''')
            continue
        if len(prop_zip) == 5:
            pass
        else:
            print('''
Invalid Input - Zip code must be 5 characters long.''')
            continue
        if int(prop_zip) in list_zip:
            break
        else:
            print('''
Invalid Input - Zip code not found in USPS list. ''')
            continue
    print('''
Now, we will input information on the unit types and expected rent. ''')
    list_unit_types = ['Studio', '1 Bedroom', '2 Bedroom', '3 Bedroom', 'Other']
    list_num_units = []
    list_exp_rents = []
    for type_u in list_unit_types:
        while True:
            num_unit = input(f'''
    How many {type_u} units are in the property? ''')
            try:
                int(num_unit)
            except ValueError:
                print('''
Invalid Input - Number of units must be an integer''')
                continue
            if int(num_unit) >= 0:
                break
            else:
                print('''
Invalid Input - Number of units cannot be negative. ''')
                continue
        exp_rent = '0'
        if int(num_unit) > 0:
            while True:
                exp_rent = input(f'''
    What is your expected monthly rent ($ per month) for one (1) {type_u} unit? ''')
                try:
                    int(exp_rent)
                except ValueError:
                    print('''
Invalid Input - Monthly rent must be an integer. ''')
                    continue
                if int(exp_rent) >= 0:
                    break
                else:
                    print('''
Invalid Input - Monthly rent cannot be negative. ''')
                    continue
        list_num_units.append(int(num_unit))
        list_exp_rents.append(int(exp_rent))
    dict_num_units = dict(zip(list_unit_types, list_num_units))
    dict_exp_rents = dict(zip(list_unit_types, list_exp_rents))
    prop_zcta = dict_zip_to_zcta[int(prop_zip)]
    line_prop_info.append(prop_name)
    line_prop_info.append(int(prop_zcta))
    line_prop_info.append(dict_num_units)
    line_prop_info.append(dict_exp_rents)
    zcta = int(prop_zcta)
    folder_output = f'{str(prop_name).replace(" ", "")}_output'
    folder_path = os.path.abspath(folder_output)
    return line_prop_info, zcta, folder_path


def property_analysis():
    def lid(x): #dict lookup line item names
        li = dict_line_item_ref[x]
        return li


    if period_type == 'annual':
        column_to_index = 'Year'
    else:
        column_to_index = 'Datevalue'
    pd_inc_stmnt = pd.read_csv('property_inc_stmnt.csv', sep=',', index_col = column_to_index)
    df_is = pd_inc_stmnt.fillna(0)
    df_is_int = df_is[lid(1): lid(13)].astype(int)
    df_is_tra = df_is_int.T
    #Calculate Income Statement Line Items (inc)
    inc_rev_rent = df_is_tra[lid(1)]
    inc_rev_other = df_is_tra[lid(2)]
    inc_total_revenue = df_is_tra[lid(1)] + df_is_tra[lid(2)]
    inc_prop_tax = df_is_tra[lid(3)]
    inc_insurance = df_is_tra[lid(4)]
    inc_total_fixed_exp = df_is_tra[lid(3)] + df_is_tra[lid(4)]
    inc_ganda = df_is_tra[lid(5)]
    inc_mgmt = df_is_tra[lid(6)]
    inc_salandwage = df_is_tra[lid(7)]
    inc_advandmkt = df_is_tra[lid(8)]
    inc_utilities = df_is_tra[lid(9)]
    inc_repair = df_is_tra[lid(10)]
    inc_other_op_exp = df_is_tra[lid(11)]
    inc_reserves = df_is_tra[lid(12)]
    inc_nonop = df_is_tra[lid(13)]
    inc_total_variable_exp = (df_is_tra[lid(5)] + df_is_tra[lid(6)] + df_is_tra[lid(7)] +
                              df_is_tra[lid(8)] + df_is_tra[lid(9)] + df_is_tra[lid(10)] +
                              df_is_tra[lid(11)] +  df_is_tra[lid(12)])
    inc_total_op_exp = inc_total_fixed_exp + inc_total_variable_exp
    inc_total_exp = inc_total_op_exp + df_is_tra[lid(13)]
    inc_ebitda = inc_total_revenue - inc_total_exp
    inc_noi = inc_total_revenue - inc_total_op_exp
    #Calculate Common Size (cs)
    divisor_common_size = inc_total_revenue
    cs_rev_rent = df_is_tra[lid(1)] / divisor_common_size
    cs_rev_other = df_is_tra[lid(2)] / divisor_common_size
    cs_tot_rev = inc_total_revenue / divisor_common_size
    cs_prop_tax = df_is_tra[lid(3)] / divisor_common_size
    cs_insurance = df_is_tra[lid(4)] / divisor_common_size
    cs_tot_fix_exp = inc_total_fixed_exp / divisor_common_size
    cs_ganda = df_is_tra[lid(5)] / divisor_common_size
    cs_mgmt = df_is_tra[lid(6)] / divisor_common_size
    cs_salandwage = df_is_tra[lid(7)] / divisor_common_size
    cs_advandmkt = df_is_tra[lid(8)] / divisor_common_size
    cs_utilities = df_is_tra[lid(9)] / divisor_common_size
    cs_repair = df_is_tra[lid(10)] / divisor_common_size
    cs_other_op_exp = df_is_tra[lid(11)] / divisor_common_size
    cs_reserves = df_is_tra[lid(12)] / divisor_common_size
    cs_tot_op_exp = inc_total_op_exp / divisor_common_size
    cs_nonop = inc_nonop / divisor_common_size
    cs_tot_exp = inc_total_exp / divisor_common_size
    cs_ebitda = inc_ebitda / divisor_common_size
    cs_noi = inc_noi / divisor_common_size
    #Calculate Operating Expense (Excluding Reserves) Breakdown (oeb)
    divisor_op_exp_breakdown = inc_total_op_exp - inc_reserves
    oeb_prop_tax = df_is_tra[lid(3)] / divisor_op_exp_breakdown
    oeb_insurance = df_is_tra[lid(4)] / divisor_op_exp_breakdown
    oeb_ganda = df_is_tra[lid(5)] / divisor_op_exp_breakdown
    oeb_mgmt = df_is_tra[lid(6)] / divisor_op_exp_breakdown
    oeb_salandwage = df_is_tra[lid(7)] / divisor_op_exp_breakdown
    oeb_advandmkt = df_is_tra[lid(8)] / divisor_op_exp_breakdown
    oeb_utilities = df_is_tra[lid(9)] / divisor_op_exp_breakdown
    oeb_repair = df_is_tra[lid(10)] / divisor_op_exp_breakdown
    oeb_other_op_exp = df_is_tra[lid(11)] / divisor_op_exp_breakdown
    #Create New Dataframes
    columns_iscs = ['Revenue, Rental', 'Revenue, Other', 'Total Revenue', 'Property Tax', 'Insurance Exp.',
                      'Total Fixed Expense', 'G&A Exp.', 'Management Exp.', 'Salaries/Wages',
                      'Advertising & Marketing', 'Utilities', 'R&M', 'Other Operating Exp.', 'Reserves',
                      'Total Operating Expense', 'Non-Op. Exp.', 'Total Expense', 'EBITDA', 'NOI']
    columns_oeb = ['Property Tax', 'Insurance Exp.', 'G&A Exp.', 'Management Exp.', 'Salaries/Wages',
                          'Advertising & Marketing', 'Utilities', 'R&M', 'Other Operating Exp.']
    df_is_full = pd.concat([inc_rev_rent, inc_rev_other, inc_total_revenue, inc_prop_tax, inc_insurance,
                            inc_total_fixed_exp, inc_ganda, inc_mgmt, inc_salandwage, inc_advandmkt,
                            inc_utilities, inc_repair, inc_other_op_exp, inc_reserves, inc_total_op_exp, inc_nonop,
                            inc_total_exp, inc_ebitda, inc_noi], axis= 1)
    df_cs_full = pd.concat([cs_rev_rent, cs_rev_other, cs_tot_rev, cs_prop_tax, cs_insurance, cs_tot_fix_exp,
                            cs_ganda, cs_mgmt, cs_salandwage, cs_advandmkt, cs_utilities, cs_repair,
                            cs_other_op_exp, cs_reserves, cs_tot_op_exp, cs_nonop, cs_tot_exp, cs_ebitda,
                            cs_noi], axis= 1)
    df_oeb_full = pd.concat([oeb_prop_tax, oeb_insurance, oeb_ganda, oeb_mgmt, oeb_salandwage, oeb_advandmkt,
                             oeb_utilities, oeb_repair, oeb_other_op_exp], axis= 1)
    df_is_full.columns = columns_iscs
    df_cs_full.columns = columns_iscs
    df_oeb_full.columns = columns_oeb
    #Calculate for Figures
    last_period_label = None
    if period_type == 'annual':
        len_period_names = len(row_y0)
        last_period_label = str(row_y0[len_period_names - 1])
    else:
        len_period_names = len(row_m0)
        last_period_label = str(row_m0[len_period_names - 1])
    last_period_inc_series = df_is_full.T[last_period_label]
    df_last_period_all_expenses = last_period_inc_series.drop(labels=['Revenue, Rental', 'Revenue, Other',
                                                                      'Total Revenue', 'Total Fixed Expense',
                                                                      'Reserves', 'Total Operating Expense',
                                                                      'Non-Op. Exp.', 'Total Expense', 'EBITDA',
                                                                      'NOI'])
    columns_is = list(df_is_full.columns)
    columns_cs = list(df_cs_full.columns)
    columns_oeb = list(df_oeb_full.columns)
    all_periods = []
    last_3_periods = []
    if period_type == 'annual':
        last_3_periods = df_is_full.T.columns.values[-3:]
        all_periods = df_is_full.T.columns.values
    else:
        last_3_datevalue = df_is_full.T.columns.values[-3:] #returns strings in form of YYYY.MM
        for x_datevalue in last_3_datevalue:
            year_datevalue = x_datevalue[0:4]
            month_datevalue = x_datevalue[-2:]
            x_new_year_month = str(year_datevalue) + ' ' + dict_val_to_month[str(month_datevalue)]
            last_3_periods.append(x_new_year_month)
        all_periods_datevalue = df_is_full.T.columns.values
        for z_datevalue in all_periods_datevalue:
            year_datevalue = z_datevalue[0:4]
            month_datevalue = z_datevalue[-2:]
            z_new_year_month = str(year_datevalue) + ' ' + dict_val_to_month[str(month_datevalue)]
            all_periods.append(z_new_year_month)
    #Create Figures
    color_pie = ['mistyrose', 'lightcoral', 'tomato',  'red', 'indianred', 'peru', 'crimson', 'firebrick', 'maroon']
    #Figure 1 - Revenue and NOI Each Period
    fig_1 = plt.figure(1, figsize= (20,10))
    xaxis_1 = all_periods
    ymax_1_rev = max(inc_total_revenue.values) / 1000 * 1.1
    ymin_1_rev = min(inc_total_revenue.values) / 1000 * 0.9
    ymax_1_noi = max(inc_noi.values) / 1000 * 1.1
    ymin_1_noi = min(inc_noi.values) / 1000
    graph_rev_fig_1 = fig_1.add_subplot(211)
    graph_noi_fig_1 = fig_1.add_subplot(212)
    graph_rev_fig_1.plot(xaxis_1, inc_total_revenue.values / 1000, label='Total Revenue')
    graph_rev_fig_1.set_title('Total Revenue')
    graph_rev_fig_1.set_ylabel("$000's")
    graph_rev_fig_1.set_ylim(ymin_1_rev, ymax_1_rev)
    graph_rev_fig_1.grid(axis= 'y')
    for label_x_tot_rev in graph_rev_fig_1.get_xticklabels():
        label_x_tot_rev.set_rotation(-45)
    graph_noi_fig_1.plot(xaxis_1, inc_noi.values / 1000, label='NOI')
    graph_noi_fig_1.set_title('NOI')
    graph_noi_fig_1.set_ylabel("$000's")
    graph_noi_fig_1.set_ylim(ymin_1_noi, ymax_1_noi)
    graph_noi_fig_1.grid(axis= 'y')
    for label_x_noi in graph_noi_fig_1.get_xticklabels():
        label_x_noi.set_rotation(-45)
    fig_1.savefig(os.path.join(folder_path,'fig_rev_noi.png'))
    #Figure 2 - Op. Exp. Breakdown Last Period
    fig_2, ax2 = plt.subplots(figsize=(7,6))
    ax2.set_title('''Operating Expense (Excl. Reserves) 
Breakdown for Last Available Period''')
    ax2.pie(df_last_period_all_expenses, colors=color_pie, radius= 0.75)
    ax2.legend(loc= (0,-0.1), fontsize= 10, ncol= 2,
               labels= [str(opexp) + ' - ' + f'{pct:.2f}' + ' %' for opexp,
               pct in zip(df_last_period_all_expenses.index.values.tolist(),
                          df_last_period_all_expenses.values / sum(df_last_period_all_expenses.values) * 100)])
    fig_2.savefig(os.path.join(folder_path,'fig_opex_last.png'))
    #Figure 3 - Inc. Stmnt. Last 3 Periods
    fig_3, ax3 = plt.subplots(figsize= (20, 10))
    ax3.table(cellText=df_is_full[-3:].T.values // 1000, colLabels= last_3_periods, rowLabels= columns_is,loc= 'center', colWidths=(0.1,0.1,0.1))
    ax3.patch.set_visible(False)
    ax3.axis('off')
    ax3.axis('tight')
    ax3.set_title("Income Statement - Latest 3 Periods Available ($000's)")
    fig_3.savefig(os.path.join(folder_path,'inc_stmnt_last3.png'))
    #Figure 4 - Common Size Inc Last 3 Periods
    fig_4, ax4 = plt.subplots(figsize= (20, 10))
    ax4.table(cellText=(df_cs_full[-3:].T.values * 100).astype(int), colLabels= last_3_periods, rowLabels= columns_cs,loc= 'center', colWidths=(0.1,0.1,0.1))
    ax4.patch.set_visible(False)
    ax4.axis('off')
    ax4.axis('tight')
    ax4.set_title("Income Statement Common Size - Latest 3 Periods Available (%)")
    fig_4.savefig(os.path.join(folder_path,'common_size_last3.png'))
    #Figure 5 - Op. Exp. Last 3 Periods
    fig_5, ax5 = plt.subplots(figsize= (20, 10))
    ax5.table(cellText=(df_oeb_full[-3:].T.values * 100).astype(int), colLabels= last_3_periods, rowLabels= columns_oeb,loc= 'center', colWidths=(0.1,0.1,0.1))
    ax5.patch.set_visible(False)
    ax5.axis('off')
    ax5.axis('tight')
    ax5.set_title("Operational Expense Items (Excl. Reserves) as Percentage of Total Operational Expenses - Latest 3 Periods Available (%)")
    fig_5.savefig(os.path.join(folder_path,'opex_last3.png'))
    #Figure 6 - Valuation by Period
    fig_6, ax6 = plt.subplots(figsize=(10, 10), sharex= True)
    if period_type == 'annual':
        cap_multiplier = 1
    else:
        cap_multiplier = 12
    cap_high = 0.01
    cap_low = 0.15
    high = ((df_is_full['NOI'] * cap_multiplier) / cap_high / 1000).astype(int)
    cap_02 = ((df_is_full['NOI'] * cap_multiplier) / 0.02 / 1000).astype(int)
    cap_03 = ((df_is_full['NOI'] * cap_multiplier) / 0.03 / 1000).astype(int)
    cap_04 = ((df_is_full['NOI'] * cap_multiplier) / 0.04 / 1000).astype(int)
    cap_05 = ((df_is_full['NOI'] * cap_multiplier) / 0.05 / 1000).astype(int)
    cap_06 = ((df_is_full['NOI'] * cap_multiplier) / 0.06 / 1000).astype(int)
    cap_07 = ((df_is_full['NOI'] * cap_multiplier) / 0.07 / 1000).astype(int)
    cap_08 = ((df_is_full['NOI'] * cap_multiplier) / 0.08 / 1000).astype(int)
    cap_09 = ((df_is_full['NOI'] * cap_multiplier) / 0.09 / 1000).astype(int)
    cap_10 = ((df_is_full['NOI'] * cap_multiplier) / 0.10 / 1000).astype(int)
    cap_11 = ((df_is_full['NOI'] * cap_multiplier) / 0.11 / 1000).astype(int)
    cap_12 = ((df_is_full['NOI'] * cap_multiplier) / 0.12 / 1000).astype(int)
    cap_13 = ((df_is_full['NOI'] * cap_multiplier) / 0.13 / 1000).astype(int)
    cap_14 = ((df_is_full['NOI'] * cap_multiplier) / 0.14 / 1000).astype(int)
    low = ((df_is_full['NOI'] * cap_multiplier) / cap_low / 1000).astype(int)
    xaxis_5 = all_periods
    #ax6.fill_between(xaxis_5, low, high, color=color_main)
    ax6.fill_between(xaxis_5, low, cap_14, color= color_secondary)
    ax6.fill_between(xaxis_5, cap_14, cap_13, color=color_main)
    ax6.fill_between(xaxis_5, cap_13, cap_12, color=color_secondary)
    ax6.fill_between(xaxis_5, cap_12, cap_11, color=color_main)
    ax6.fill_between(xaxis_5, cap_11, cap_10, color=color_secondary)
    ax6.fill_between(xaxis_5, cap_10, cap_09, color=color_main)
    ax6.fill_between(xaxis_5, cap_09, cap_08, color=color_secondary)
    ax6.fill_between(xaxis_5, cap_08, cap_07, color=color_main)
    ax6.fill_between(xaxis_5, cap_07, cap_06, color=color_secondary)
    ax6.fill_between(xaxis_5, cap_06, cap_05, color=color_main)
    ax6.fill_between(xaxis_5, cap_05, cap_04, color=color_secondary)
    ax6.fill_between(xaxis_5, cap_04, cap_03, color=color_main)
    ax6.fill_between(xaxis_5, cap_03, cap_02, color=color_secondary)
    ax6.fill_between(xaxis_5, cap_02, high, color=color_main)
    ymax_6 = max(high) * 1.1
    if min(low) < 0:
        ymin_6 = 0
    else:
        ymin_6 = min(low)
    ax6.set_ylim(ymin_6, ymax_6)
    ax6.grid(axis= 'y')
    ax6.set_title(f'''
Valuation ($000's) Range
Based on Period NOI and Cap Rate between {cap_high:.1%} and {cap_low:.1%}
1.0% Increments''')
    fig_6.savefig(os.path.join(folder_path,'valuation_noi.png'))


def get_api_key():
    global apikey
    print('''
The program will scrape census data from the target property's area.
You will need an API key from the Census website.

Go to https://api.census.gov/data/key_signup.html
Input your information. You can enter "Personal" in the company box.
You should receive your API key in your email with a few minutes.''')
    apikey = input('''
Please type or copy in the API key you received and hit Enter. ''')
    return apikey


def market_info():
    def url_census(c_group):
        url = f'https://api.census.gov/data/2023/acs/acs5/subject?get=NAME,group({c_group})&for=zip%20code%20tabulation%20area:{zcta}&key={str(apikey).strip()}'
        return url


    def dataframe_census(url_ind):
        response = requests.get(url_ind)
        c_data = response.json()
        c_df = pd.DataFrame(c_data)
        c_df.rename(columns= c_df.iloc[0], inplace= True)
        c_df.drop(c_df.index[0], inplace= True)
        return c_df


    #Desired Categories
    census_group = ['S0101', 'S1901']
    census_category = ['Population', 'Household Income']
    dict_census = dict(zip(census_category, census_group))
    url_population = url_census(dict_census['Population'].strip("'"))
    url_hhinc = url_census(dict_census['Household Income'].strip("'"))
    df_population = dataframe_census(url_population)
    df_hhinc = dataframe_census(url_hhinc)
    dict_c_items = {'S0101_C01_001E': 'Total Population',
                    'S0101_C01_022E': 'Under 18',
                    'S0101_C01_026E': 'Over 18',
                    'S0101_C01_032E': 'Median Age',
                    'S1901_C01_002E': 'Less than $10,000',
                    'S1901_C01_003E': '$10,000-14,999',
                    'S1901_C01_004E': '$15,000-24,999',
                    'S1901_C01_005E': '$25,000-34,999',
                    'S1901_C01_006E': '$34,000-49,999',
                    'S1901_C01_007E': '$50,000-74,999',
                    'S1901_C01_008E': '$75,000-99,999',
                    'S1901_C01_009E': '$100,000-149,999',
                    'S1901_C01_010E': '$150,000-199,999',
                    'S1901_C01_011E': '$200,000 and Greater'}
    #Census Data Line Items
    pop_total = df_population['S0101_C01_001E']
    pop_u18 = df_population['S0101_C01_022E']
    pop_o18 = df_population['S0101_C01_026E']
    pop_med_age = df_population['S0101_C01_032E']
    hhi_u10 = df_hhinc['S1901_C01_002E']
    hhi_10_15 = df_hhinc['S1901_C01_003E']
    hhi_15_25 = df_hhinc['S1901_C01_004E']
    hhi_25_35 = df_hhinc['S1901_C01_005E']
    hhi_35_50 = df_hhinc['S1901_C01_006E']
    hhi_50_75 = df_hhinc['S1901_C01_007E']
    hhi_75_100 = df_hhinc['S1901_C01_008E']
    hhi_100_150 = df_hhinc['S1901_C01_009E']
    hhi_150_200 = df_hhinc['S1901_C01_010E']
    hhi_o200 = df_hhinc['S1901_C01_011E']
    #Construct New Dataframes for Figures
    df_g_hhinc_raw = pd.concat([hhi_u10, hhi_10_15, hhi_10_15, hhi_15_25, hhi_25_35, hhi_35_50, hhi_50_75, hhi_75_100,
                            hhi_100_150, hhi_150_200, hhi_o200], axis= 1 )
    df_g_hhinc = df_g_hhinc_raw.rename(columns= dict_c_items)
    df_g_pop_raw = pd.concat([pop_u18, pop_o18], axis= 1)
    df_g_pop = df_g_pop_raw.rename(columns= dict_c_items)
    #Create Figures
    #Figure Household Income
    fig_hhinc, ax_hhinc = plt.subplots(figsize= (20,10))
    y_max_hhinc = max(df_g_hhinc.T[1].astype(float)) + 0.1
    ax_hhinc.bar(df_g_hhinc.columns, df_g_hhinc.T[1].values.astype(float), color= color_main)
    ax_hhinc.set_ylim(0, y_max_hhinc)
    ax_hhinc.grid(axis= 'y')
    ax_hhinc.set_title('Household Income Distribution (%)')
    for label_x_hhinc in ax_hhinc.get_xticklabels():
        label_x_hhinc.set_rotation(-30)
    fig_hhinc.savefig(os.path.join(folder_path,'hh_inc.png'))
    #Figure Population
    fig_pop, ax_pop = plt.subplots(figsize= (7,6))
    ax_pop.pie(df_g_pop.T[1].values, labels= df_g_pop.columns.values ,colors= [color_secondary, color_main],
               autopct= '%1.1f%%')
    ax_pop.set_title(f'''
Age Distribution
Total Population - {pop_total[1]}
Median Age - {pop_med_age[1]}''')
    fig_pop.savefig(os.path.join(folder_path,'population.png'))


class Property:
    def __init__(self, prop_name, prop_zcta, unit_mix, exp_rents):
        self.prop_name = prop_name
        self.prop_zcta = prop_zcta
        self.unit_mix = unit_mix
        self.exp_rents = exp_rents
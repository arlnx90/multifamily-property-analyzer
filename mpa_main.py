import numpy
from mpa_functions import (welcome, property_info, csv_blank_property_inc, Property, property_analysis, market_info,
                           get_api_key)
import os
array_zip_code_usps = numpy.genfromtxt('zip_code_info_usps.csv', delimiter=',', usecols=numpy.arange(0, 10))
list_zip = array_zip_code_usps[:, 4]
array_zcta = numpy.genfromtxt('zip_to_zcta_hrsa.csv', delimiter= ',', usecols= numpy.arange(0,5))
list_fordict_zip = array_zcta[:, 0]
list_fordict_zcta = array_zcta[:, 4]
dict_zip_to_zcta = dict(zip(list_fordict_zip, list_fordict_zcta))
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
line_item_num_ref = numpy.arange(0, 14)
dict_line_item_ref = dict(zip(line_item_num_ref, list_prop_line_item_det))
color_main = 'darkcyan'
color_secondary = 'paleturquoise'
#Start Main
welcome()
line_prop_info, zcta, folder_path = property_info()
property_target = Property(line_prop_info[0], line_prop_info[1], line_prop_info[2], line_prop_info[3])
period_type, row_y0, row_m0, num_periods = csv_blank_property_inc()
while True:
    answer_data_saved = input('''
    Please hit enter after you have saved your data. ''')
    break
apikey = get_api_key()
while True:
    folder_output_test = f'{str(property_target.prop_name).replace(" ", "")}_output'
    answer_ready_save = input(f'''
    The program will now analyze your data and save output to
    a folder named {folder_output_test}.
    If a folder with this name already exists in the current working directory, an error
    will occur, and you will be prompted to try again. 
    
    Hit enter to proceed. ''')
    try:
        os.mkdir(folder_output_test)
        break
    except FileExistsError:
        print('''
Error - Directory already exists. ''')
        continue
    except PermissionError:
        print('''
Error - Permission denied to create directory. ''')
        continue
property_analysis()
print('''
Analysis complete.''')
market_info()
print('''
Market data scraping complete.''')
print('''
The program has completed. Check your directory for output. ''')
from datetime import datetime
from datetime import date

# reference:
# https://www.datacamp.com/tutorial/converting-strings-datetime-objects


x = datetime.today().replace(microsecond=0,second=0,minute=0,hour=0)
print(x)
print(type(x))

# 17 Nov 2024
y = date(2024,11,17)
print(y)

# date_string = "17-11-2024"
# date_format = '%d-%m-%Y'
# date_object = date.isoformat(date_string,date_format)
# print(date_object)


date_str = '17-11-2024'

date_object = datetime.strptime(date_str, '%d-%m-%Y').date()
print(type(date_object))
print(date_object)  # printed in default format

from datetime import datetime

current_data_and_time = datetime.now()

current_time = current_data_and_time.strftime('%H:%M:%S')

print(current_data_and_time)
print(current_time)

print(str(current_data_and_time))
print(type(str(current_data_and_time)))


new_curr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(new_curr)
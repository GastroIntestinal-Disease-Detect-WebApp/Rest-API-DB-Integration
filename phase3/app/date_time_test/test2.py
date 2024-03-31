from datetime import datetime, timedelta

stored_data_and_time = datetime.now()

current_data_and_time = datetime.now()

time_difference= current_data_and_time-stored_data_and_time

if time_difference > timedelta(minutes=60):
    print("More than 60 minutes have passed.")
else:
    print("Less than 60 minutes have passed.")


# if current time - logout time (stored in db) is more than 60 minutes then remove the token from database
# the token expires after 60 minutes

# edge case: just login and then just logout
# thus 1hr more for token to be in logged out state but still be in db


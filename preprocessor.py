import pandas as pd
import re
def preprocessor(data):
    pattern = r'\d{1,2}\/\d{1,2}\/\d{2},\s*\d{1,2}:\d{2}\s*[APap][Mm]'
    message = re.split(pattern, data, maxsplit=0, flags=0)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': message, 'message_date': dates})
    # convert message_data type
    df['message_date'] = df['message_date'].apply(lambda x: re.sub(r'[^ -~]+', '', x))

    df['message_date'] = df['message_date'].apply(lambda x: re.sub(r'(\d)([APap][Mm])', r'\1\\u202f\2', x))

    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M\\u202f%p', errors='coerce')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # separate users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("group_notification")
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['per_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # finding time on wich user are active
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df


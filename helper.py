from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji
from wordcloud import WordCloud

extractor = URLExtract()
def fetch_starts(selected_user,df):

    if selected_user != "OverAll":
        df = df[df['user'] == selected_user]
        #1.fetch number of message
    num_messages = df.shape[0] # number of messages
    #2 .number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    #3.fetch the number of media
    num_media =df[df['message'] == '<Media omitted>\n'].shape[0]

    #4. fetch the numbers of links shared
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages , len(words),num_media,len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df=round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent%'})
    return x,df

'''def create_wordcloud(selected_user,df):
    if selected_user != "OverAll":
        df = df[df['user'] == selected_user]

        wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
        #generate the image
        df_wc = wc.generate(df['message'].str.cat(sep=" "))
        return df_wc'''
#for most common words
def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != "OverAll":
        df = df[df['user'] == selected_user]

        # remove group message
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != "<Media omitted>\n"]

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

#emoji analysis
def emoji_helper(selected_user,df):
    if selected_user != "OverAll":
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        if message:
            emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

#function for the monthly time line
def time_Line(selected_user,df):
    if selected_user != "OverAll":
        df = df[df['user'] == selected_user]

    #df['month_num'] = df['date'].dt.month

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

#daily time line
def daily_TimeLine(selected_user,df):
    if selected_user != "OverAll":
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('per_date').count()['message'].reset_index()

    return daily_timeline

#activity map
def week_activity_map(selected_user,df):
    if selected_user != "OverAll":
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def monthly_activity_map(selected_user,df):
    if selected_user != "OverAll":
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

# finding time on wich user are active
def activity_heatmap(selected_user,df):
    if selected_user != "OverAll":
        df = df[df['user'] == selected_user]

    activity_pivot_table=df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return activity_pivot_table
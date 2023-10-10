import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import seaborn as sns



st.sidebar.title("WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    #conerting into string
    data= bytes_data.decode("utf-8")
    df = preprocessor.preprocessor(data)

    # st.dataframe(df)

    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"OverAll")


    selected_user =st.sidebar.selectbox("Show analysis wrt",user_list)

    #add button to show analysis
    if st.sidebar.button("Show Analysis"):
        #stats Area
        num_messages,words,num_media,links=helper.fetch_starts(selected_user,df)

        st.title("Top Statistics")
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total Media Shared ")
            st.title(num_media)

        with col4:
            st.header("Total Links Shared")
            st.title(links)

        #monthly timeline 0f the user
        st.title("Monthly Time Line ")
        timeline = helper.time_Line(selected_user,df)

        fig , ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        plt.xlabel('monthly_timeline')
        plt.ylabel('no_of_messages')
        st.pyplot(fig)
        #st.dataframe(timeline)

        #daily timeline
        st.title("Daily Time Line")
        daily_timeline= helper.daily_TimeLine(selected_user,df)

        fig,ax=plt.subplots()
        ax.plot(daily_timeline['per_date'],daily_timeline['message'],color='yellow')
        plt.xlabel('per_date')
        plt.ylabel('no_of_messages')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title("Activity Map")
        col1,col2=st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='orange')
            plt.xlabel("busy_day_index")
            plt.ylabel("busy_day_value")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month=helper.monthly_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='pink')
            plt.xlabel("busy_month_index")
            plt.ylabel("busy_month_value")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #activity heatmap
        st.title("Weekly Activity Map")
        activity_pivot_table=helper.activity_heatmap(selected_user,df)
        fig,ax= plt.subplots()
        ax=sns.heatmap(activity_pivot_table)
        st.pyplot(fig)






        #finding the busiest users in group(group level)
        if selected_user =="OverAll":
            st.title("Most Busy Users")
            x,new_df= helper.most_busy_users(df)
            fig,ax=plt.subplots()

            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)



        #most common words
        st.title("Most Common Words")
        most_common_df=helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
         #st.dataframe(most_common_df)

        #emoji analysis
        st.title("Emoji Analysis")
        emoji_df=helper.emoji_helper(selected_user,df)

        col1,col2=st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig.ax=plt.subplots()
            #ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct='%0.2f')
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct='%0.2f')

            st.pyplot(fig)


        
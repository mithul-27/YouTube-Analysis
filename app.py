import pandas as pd
from googleapiclient.discovery import build
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import isodate
import datetime
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import base64

icon = "https://avatars.githubusercontent.com/u/4052902?v=4"
st.set_page_config(page_title='YouTube Analysis ',page_icon=icon,initial_sidebar_state='expanded',
                        layout='wide')

# Function to load image and convert to base64
def load_image_as_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

# Load the local YouTube icon
icon_base64 = load_image_as_base64("youtube_icon.png")  # Replace with your local image path

# Define the HTML code for YouTube Analysis with a local icon
html_code = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@700&display=swap');
        .youtube-container {{
            display: flex;
            align-items: center;
        }}
        .youtube-icon {{
            width: 50px;
            margin-right: 10px;
        }}
        .youtube-text {{
            font-weight: bold;
            font-size: 50px;
            font-family: 'Roboto', sans-serif;
        }}
        .youtube-red {{
            color: #FF0000;
        }}
        .youtube-grey {{
            color: #606060;
        }}
    </style>
    <div class="youtube-container">
        <img src="data:image/png;base64,{icon_base64}" alt="YouTube" class="youtube-icon">
        <h1 class="youtube-text">
            <span class="youtube-red">YouTube</span>
            <span class="youtube-grey">Analysis</span>
        </h1>
    </div>
"""

API_KEY = 'AIzaSyCqiU_jxcLNsgP32P8iP7BMQoGx7WjYsGY'
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_category_mapping():
    request = youtube.videoCategories().list(
        part='snippet',
        regionCode='IN'
    )
    response = request.execute()
    category_mapping = {}
    for item in response['items']:
        category_id = int(item['id'])
        category_name = item['snippet']['title']
        category_mapping[category_id] = category_name
    return category_mapping

# get the category mapping
category_mapping = get_category_mapping()

# Display the custom HTML using st.markdown
st.markdown(html_code, unsafe_allow_html=True)

tabs = option_menu("",options=["Trending Videos","Home","Channel Videos"],
                        icons=["fire","house-door-fill","collection-play"],
                        default_index=1,
                        orientation="horizontal",
                            styles={ "container": {   "width": "100%", "border": "none",    "background-color": "#FFFFFF", "padding": "50px", "display": "flex", "justify-content": "space-around", "align-items": "center"},
                                        "icon": {"color": "#FF0000", "font-size": "30px"},
                                    "nav-link": { "font-size": "18px", "text-align": "center", "margin": "0px 15px", "color": "#606060", "font-weight": "bold", "text-decoration": "none", "transition": "color 0.3s ease", "flex-grow": "1",
                                                    "padding": "10px 20px", "white-space": "nowrap", "min-width": "150px"},
                                "nav-link:hover": { "color": "#FF0000"},
                            "nav-link-selected": { "background-color": "transparent", "color": "#FF0000", "font-weight": "bold", "border-bottom": "2px solid #FF0000", "white-space": "nowrap", "min-width": "150px"}
                                })

#************************************************************************************************************************************************************************************************************************************************************************************************************#

if tabs == "Home":

    html_code = """
        <style>
            .container {
                max-width: 1200px;
                margin: 20px auto;
                padding: 20px;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                font-family: 'Arial', sans-serif;
                color: #333;
            }
            h2 {
                font-size: 32px;
                color: #FF0000; /* YouTube red */
                margin-bottom: 20px;
            }
            p {
                font-size: 20px;
                color: #000080; /* Dark blue for subheadings */
                margin-top: 20px;
                margin-bottom: 10px;
            }
            ul {
                font-size: 20px;
                color: #000080; /* Dark blue for subheadings */
                margin-top: 20px;
                margin-bottom: 10px;
            }
            .footer {
            font-size: 14px;
            color: #606060; /* Grey color for the footer */
            position: absolute;  /* Position the footer absolutely */
            bottom: 10px;  /* Distance from the bottom */
            right: 90px;   /* Distance from the right */
            }
        </style>

        <div class="container">
            <h2>Project Overview</h2>
            <p>This project aims to analyze trending videos and channel performance on YouTube. I've leveraged data visualization techniques to provide insights into video metrics, audience engagement, overall channel health, etc.</p>
            <h2>Trending Videos Analysis</h2>
            <p>In this section, we perform an in-depth analysis of the top trending videos on YouTube. Examined metrics such as views, likes, comments, category analysis, and other metrics to understand what makes a video successful.</p>
            <h2>Channel Videos Analysis</h2>
            <p>This part of the project focuses on analyzing individual channel performance of user choice. User has to paste the channel id to derive the data. We explore various metrics including total views, top videos, and engagement based on views, likes and comments to gauge overall channel effectiveness.</p>
            <h2>Libraries Used</h2>
            <p>Utilized API feature and several popular visualization libraries to create insightful charts and graphs:</p>
            <ul>
                <li><strong>Google API:</strong> For extracting the necessary data related to trending videos and scripting the data of a particular YouTube channel</li>
                <li><strong>Seaborn:</strong> For statistical data visualization.</li>
                <li><strong>Matplotlib:</strong> For creating static, animated, and interactive visualizations.</li>
                <li><strong>Plotly Express:</strong> For quick and easy interactive visualizations.</li>
            </ul>
            <div class="footer">
            This page is created by Mithul C B
            </div>
        </div>
        """

    st.markdown(html_code, unsafe_allow_html=True)

#************************************************************************************************************************************************************************************************************************************************************************************************************#

if tabs == "Trending Videos":

    def get_trending_videos(api_key, max_results=200):
                # build the youtube service
                youtube = build('youtube', 'v3', developerKey=api_key)

                # initialize the list to hold video details
                trending_videos = []

                # fetch the most popular videos
                request = youtube.videos().list(
                    part='snippet,contentDetails,statistics',
                    chart='mostPopular',
                    regionCode='IN',
                    maxResults=50
                )

                # paginate through the results if max_results > 50
                while request and len(trending_videos) < max_results:
                    response = request.execute()
                    for item in response['items']:
                        thumbnail_url = item['snippet']['thumbnails'].get('standard', {}).get('url')
                        video_details = {
                            'video_id': item['id'],
                            'title': item['snippet']['title'],
                            'description': item['snippet']['description'],
                            'published_at': item['snippet']['publishedAt'],
                            'channel_id': item['snippet']['channelId'],
                            'channel_title': item['snippet']['channelTitle'],
                            'category_id': item['snippet']['categoryId'],
                            'tags': item['snippet'].get('tags', []),
                            'duration': item['contentDetails']['duration'],
                            'definition': item['contentDetails']['definition'],
                            'thumbnail': thumbnail_url,
                            'caption': item['contentDetails'].get('caption', 'false'),
                            'view_count': item['statistics'].get('viewCount', 0),
                            'like_count': item['statistics'].get('likeCount', 0),
                            'dislike_count': item['statistics'].get('dislikeCount', 0),
                            'favorite_count': item['statistics'].get('favoriteCount', 0),
                            'comment_count': item['statistics'].get('commentCount', 0)
                        }
                        trending_videos.append(video_details)

                    # get the next page token
                    request = youtube.videos().list_next(request, response)

                return trending_videos[:max_results]
    

    trending_videos=pd.DataFrame(get_trending_videos(API_KEY))

    # Convert numerical columns to int data type
    trending_videos[['category_id','view_count','like_count','favorite_count','comment_count']]=trending_videos[['category_id','view_count','like_count','favorite_count','comment_count']].fillna(0).astype(int)

    # fill missing descriptions with "No description"
    trending_videos['description'].fillna('No description', inplace=True)

    # convert `published_at` to datetime
    trending_videos['published_at'] = pd.to_datetime(trending_videos['published_at'])

    # convert tags from string representation of list to actual list
    trending_videos['tags'] = trending_videos['tags'].apply(lambda x: eval(x) if isinstance(x, str) else x)

    top3 = trending_videos[['title','channel_title','view_count','like_count','comment_count','thumbnail',"published_at"]].head(3)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    with st.container():
            st.markdown("""<div style="font-family: Arial; line-height: 1.6; padding: 20px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
        <h1 style="color: #FF0000; font-size: 30px; ">Top 3 Trending Videos</h1>
        </div>""", unsafe_allow_html=True)
            
            cols = st.columns(3)
            
            for i in range(3):
                with cols[i]:
                    st.image(top3['thumbnail'][i], use_column_width=True)
                    st.subheader(top3['title'][i])
                    st.markdown(f"<p style='font-size: 20px; text-align: center;'><strong>Channel:</strong> {top3['channel_title'][i]}</p>", 
                        unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 20px; text-align: center;'><strong>Views:</strong> {top3['view_count'][i]}</p>", 
                        unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 20px; text-align: center;'><strong>Likes:</strong> {top3['like_count'][i]}</p>", 
                        unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 20px; text-align: center;'><strong>Comments:</strong> {top3['comment_count'][i]}</p>", 
                        unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 20px; text-align: center;'><strong>Uploaded on:</strong> {top3.iloc[i]['published_at'].strftime('%d/%m/%Y %H:%M:%S')}</p>", 
                        unsafe_allow_html=True)
                    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    st.markdown(" ")
    st.markdown(" ")
    st.markdown("""<div style="font-family: Arial; line-height: 1.6; padding: 20px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
        <h1 style="color: #FF0000; font-size: 30px;">Distribution of Views, Likes and Comments</h1>
        </div>""", unsafe_allow_html=True)

    sns.set_theme(style="whitegrid")

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # view count distribution
    sns.histplot(trending_videos['view_count'], bins=15, kde=True, ax=axes[0], color='blue')
    axes[0].set_title('View Count Distribution')
    axes[0].set_xlabel('View Count')
    axes[0].set_ylabel('Frequency')

    # like count distribution
    sns.histplot(trending_videos['like_count'], bins=15, kde=True, ax=axes[1], color='green')
    axes[1].set_title('Like Count Distribution')
    axes[1].set_xlabel('Like Count')
    axes[1].set_ylabel('Frequency')

    # comment count distribution
    sns.histplot(trending_videos['comment_count'], bins=15, kde=True, ax=axes[2], color='red')
    axes[2].set_title('Comment Count Distribution')
    axes[2].set_xlabel('Comment Count')
    axes[2].set_ylabel('Frequency')

    plt.tight_layout()
    st.pyplot(fig)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    st.markdown(" ")
    st.markdown(" ")
    st.markdown("""
    <div style="font-family: Arial; line-height: 1.6; padding: 20px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
        <h1 style="color: #FF0000; font-size: 30px;">Correlation Matrix of Views, Likes and Comments</h1>
    </div>
    """, unsafe_allow_html=True)

    # correlation matrix
    correlation_matrix = trending_videos[['view_count', 'like_count', 'comment_count']].corr()

    fig = px.imshow(correlation_matrix,
                    labels=dict( color="Correlation"),
                    title='Correlation Matrix', text_auto=True,
                    color_continuous_scale='RdBu')
    fig.update_layout(width=800, height=600)

    st.plotly_chart(fig)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    # Map category id with category name
    trending_videos['category_name'] = trending_videos['category_id'].map(category_mapping)
    st.markdown(" ")
    st.markdown(" ")
    st.markdown("""
    <div style="font-family: Arial; line-height: 1.6; padding: 20px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
        <h1 style="color: #FF0000; font-size: 30px;">Videos in Each Category</h1>
    </div>
    """, unsafe_allow_html=True)

    video_count = trending_videos['category_name'].value_counts()
    video_count = video_count.sort_values(ascending=True)
    fig = px.bar(
        x=video_count.values,
        y=video_count.index,
        labels={'x':'Number of Videos', 'y':'Category'},
        title='Number of Videos per Category', orientation='h',
        height=800,color=video_count.values, color_continuous_scale="thermal"
    )
    fig.update_layout(width=1200, height=800)
    st.plotly_chart(fig)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    st.markdown(" ")
    st.markdown(" ")
    st.markdown("""
    <div style="font-family: Arial; line-height: 1.6; padding: 20px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
        <h1 style="color: #FF0000; font-size: 30px;">Videos in Each Category</h1>
    </div>
    """, unsafe_allow_html=True)

    category_engagement = trending_videos.groupby('category_name')[['view_count', 'like_count', 'comment_count']].mean()
    category_engagement1 = category_engagement.sort_values(by='view_count', ascending=True)
    category_engagement2 = category_engagement.sort_values(by='like_count', ascending=True)
    category_engagement3 = category_engagement.sort_values(by='comment_count', ascending=True)

    fig = make_subplots(rows=1, cols=3, subplot_titles=['Average View Count by Category', 'Average Like Count by Category','Average Comment Count by Category'])

    fig.add_trace(go.Bar(
        x=category_engagement1['view_count'],
        y=category_engagement1.index,
        orientation='h', marker=dict(color=category_engagement1['view_count'], colorscale='Viridis'), showlegend=False
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        x=category_engagement2['like_count'],
        y=category_engagement2.index,
        orientation='h', marker=dict(color=category_engagement2['like_count'], colorscale='Cividis'), showlegend=False
    ), row=1, col=2)

    fig.add_trace(go.Bar(
        x=category_engagement3['comment_count'],
        y=category_engagement3.index,
        orientation='h', marker=dict(color=category_engagement3['comment_count'], colorscale='Magma'), showlegend=False
    ), row=1, col=3)


    fig.update_layout(
        xaxis_title='Average View Count',
        yaxis_title='Category',
        xaxis2_title='Average Like Count',
        yaxis2_title='Category',
        xaxis3_title='Average Comment Count',
        yaxis3_title='Category',
        height=600, width=1300
    )

    st.plotly_chart(fig)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    # convert ISO 8601 duration to seconds
    trending_videos['duration_seconds'] = trending_videos['duration'].apply(lambda x: isodate.parse_duration(x).total_seconds())

    trending_videos['duration_range'] = pd.cut(trending_videos['duration_seconds'], bins=[0, 300, 600, 1200, 3600, 7200,10800,14400, 36000], labels=['0-5 min', '5-10 min', '10-20 min', '20-60 min', '60-120 min','120-180 min', '180-240 min','>3 Hours'])


    st.markdown(" ")
    st.markdown(" ")
    st.markdown("""
    <div style="font-family: Arial; line-height: 1.6; padding: 20px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
        <h1 style="color: #FF0000; font-size: 30px;">Comparing Views with Video Duration</h1>
    </div>
    """, unsafe_allow_html=True)

    fig = px.scatter(trending_videos, x='duration_seconds', y='view_count', color="view_count", hover_data={'Title':trending_videos['title'],'Duration Range':trending_videos['duration_range'],'Views':trending_videos['view_count'],
                                                                                                            'Duration(in sec)':trending_videos['duration_seconds'], 'view_count':False, 'duration_seconds':False}, color_continuous_scale="Agsunset")
    fig.update_layout(
        xaxis_title='Video Duration (seconds)',
        yaxis_title='View Count',
        title='Video Duration vs View Count', height=600, width=1300
    )
    st.plotly_chart(fig)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    # bar chart for engagement metrics by duration range
    length_engagement = trending_videos.groupby('duration_range')[['view_count', 'like_count', 'comment_count']].mean()
    length_engagement1 = length_engagement.sort_values(by='view_count', ascending=True)
    length_engagement2 = length_engagement.sort_values(by='like_count', ascending=True)
    length_engagement3 = length_engagement.sort_values(by='comment_count', ascending=True)

    st.markdown(" ")
    st.markdown(" ")
    st.markdown("""
    <div style="font-family: Arial; line-height: 1.6; padding: 20px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
        <h1 style="color: #FF0000; font-size: 30px;">Average Views, Likes and Comments by Video Duration</h1>
    </div>
    """, unsafe_allow_html=True)

    fig = make_subplots(rows=1, cols=3, subplot_titles=['Average View Count by Duration Range', 'Average Like Count by Duration Range','Average Comment Count by Duration Range'])

    fig.add_trace(go.Bar(
        y=length_engagement1.index, x=length_engagement1['view_count'],
        orientation='h', marker=dict(color=length_engagement1['view_count'], colorscale='mint'), showlegend=False
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        y=length_engagement2.index, x=length_engagement2['like_count'],
        orientation='h', marker=dict(color=length_engagement2['like_count'], colorscale='deep'), showlegend=False
    ), row=1, col=2)

    fig.add_trace(go.Bar(
        y=length_engagement3.index, x=length_engagement3['comment_count'], hovertext=length_engagement3['comment_count'],
        orientation='h', marker=dict(color=length_engagement3['comment_count'], colorscale='darkmint'), showlegend=False
    ), row=1, col=3)


    fig.update_layout(
        xaxis_title='Average View Count',
        yaxis_title='Duration Range',
        xaxis2_title='Average Like Count',
        yaxis2_title='Duration Range',
        xaxis3_title='Average Comment Count',
        yaxis3_title='Duration Range',
        height=600, width=1300
    )
    st.plotly_chart(fig)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    st.markdown(" ")
    st.markdown(" ")
    st.markdown("""
    <div style="font-family: Arial; line-height: 1.6; padding: 20px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
        <h1 style="color: #FF0000; font-size: 30px;">Comparing Views with Tag Count</h1>
    </div>
    """, unsafe_allow_html=True)

    trending_videos['tag_count'] = trending_videos['tags'].apply(len)

    fig = px.scatter(trending_videos, x='tag_count', y='view_count', color="view_count", hover_data={'Title':trending_videos['title'],'Views':trending_videos['view_count'],
                                                                                                     'Tag Count':trending_videos['tag_count'], 'tag_count':False, 'view_count':False}, color_continuous_scale='Turbo')
    fig.update_layout(
        xaxis_title='Number of Tags',
        yaxis_title='View Count',
        title='Number of Tags vs View Count', height=600, width=1300
    )
    st.plotly_chart(fig)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


    # bar chart for publish hour distribution
    trending_videos['publish_hour'] = trending_videos['published_at'].dt.hour
    publish_hour_counts = trending_videos['publish_hour'].value_counts()

    st.markdown(" ")
    st.markdown(" ")
    st.markdown("""
    <div style="font-family: Arial; line-height: 1.6; padding: 20px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
        <h1 style="color: #FF0000; font-size: 30px;">Number of Vidoes Uploaded in Each Hour</h1>
    </div>
    """, unsafe_allow_html=True)
    fig = px.bar(
        x=publish_hour_counts.index,
        y=publish_hour_counts.values,
        color=publish_hour_counts.values, color_continuous_scale='Viridis',
        labels={'x':'Uploaded Hour', 'y':'Number of Videos'},
        title='Number of Videos Uploaded by Published Hour', text=publish_hour_counts.values,
        height=600, width=1300
    )
    fig.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=publish_hour_counts.index,
        ticktext=[f'{hour}:00' for hour in publish_hour_counts.index]
    ))

    st.plotly_chart(fig)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    st.markdown(" ")
    st.markdown(" ")
    st.markdown("""
    <div style="font-family: Arial; line-height: 1.6; padding: 20px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
        <h1 style="color: #FF0000; font-size: 30px;">Comparing Views with Video Uploaded Hour</h1>
    </div>
    """, unsafe_allow_html=True)

    fig = px.scatter(trending_videos, x='publish_hour', y='view_count', color="view_count", hover_data={'Title':trending_videos['title'],'Views':trending_videos['view_count'],
                                                                                                     'Published Hour':trending_videos['publish_hour'], 'publish_hour':False, 'view_count':False}, color_continuous_scale='Turbo')
    fig.update_layout(
        xaxis_title='Publish Hour',
        yaxis_title='View Count',
        title='Publish Hour vs View Count', height=600, width=1300
    )
    st.plotly_chart(fig)

#************************************************************************************************************************************************************************************************************************************************************************************************************#

if tabs == "Channel Videos":
     
    def get_channel_data(channel_id):
            try:
                # Requesting channel data from YouTube API
                request = youtube.channels().list(
                    part="snippet,contentDetails,statistics",
                    id=channel_id
                )
                response = request.execute()

                # Checking if the channel exists
                if 'items' not in response or len(response['items']) == 0:
                    return None  # Invalid channel ID
                
                # Extracting channel data
                for i in response['items']:
                    channel_data = {
                        "channel_name": i['snippet']['title'],
                        "channel_id": i['id'],
                        "subscriber_count": i['statistics']['subscriberCount'],
                        "channel_views": i['statistics']['viewCount'],
                        "thumbnail": i['snippet']['thumbnails']['medium']['url'],
                        "total_videos": i['statistics']['videoCount'],
                        "channel_description": i['snippet']['description'],
                        "playlist_id": i['contentDetails']['relatedPlaylists']['uploads']
                    }
                return channel_data

            except Exception as e:
                return f"An error occurred: {e}" 
    
    def get_videos_ids(channel_id):
        videos_ids=[]
        np_token=None
        response = youtube.channels().list(part="contentDetails",
                                           id=channel_id).execute()
        playlist_id=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        while True:
            response= youtube.playlistItems().list(
                    part="snippet",
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=np_token).execute()

            for i in range(len(response['items'])):
                    videos_ids.append(response['items'][i]['snippet']['resourceId']['videoId'])

            np_token=response.get('nextPageToken')

            if np_token is None:
                break
        return videos_ids
    
    def get_video_data(videos_ids):
        videos_data=[]
        for i in videos_ids:
                response=youtube.videos().list(part='snippet,contentDetails,statistics',
                                         id=i).execute()
                for j in response['items']:
                    data={"channel_name":j['snippet']['channelTitle'],
                         "video_id":j['id'],
                          "video_name":j['snippet']['title'],
                         "video_description":j['snippet'].get('description'),
                         "tags":j['snippet'].get('tags'),
                         "published_at":j['snippet']['publishedAt'],
                         "view_count":j['statistics']['viewCount'],
                         "like_count":j['statistics'].get('likeCount'),
                         "comment_count":j['statistics'].get('commentCount'),
                         "duration":j['contentDetails'].get('duration'),
                         "thumbnails":j['snippet']['thumbnails']['medium']['url'],
                         "category_id":j['snippet']['categoryId']
                    }
                videos_data.append(data)
        return videos_data
    
     


    st.markdown("""
    <style>
    .search-box {
        width: 500px;
        height: 40px;
        border-radius: 20px;
        border: 1px solid #cccccc;
        padding-left: 15px;
        font-size: 18px;
    }
    .search-button {
        background-color: #FF0000;
        color: white;
        border: none;
        border-radius: 20px;
        height: 40px;
        width: 80px;
        font-size: 16px;
        cursor: pointer;
        margin-left: 10px;
    }
    </style>
        """, unsafe_allow_html=True)

    # Search input and button
    channel_id = st.text_input("Enter YouTube Channel ID:")

    # Button to fetch the data
    if st.button("Search"):
        if channel_id:
            channel_data = get_channel_data(channel_id)
            
            if channel_data is None:
                st.error("Invalid Channel ID! Please enter a valid YouTube Channel ID.")
            elif isinstance(channel_data, str):
                st.error(channel_data) 
            else:
                st.success("Channel Found")
                video_ids=get_videos_ids(channel_id)
                videos_data=pd.DataFrame(get_video_data(video_ids))
                videos_data[['view_count','like_count','comment_count','category_id']]=videos_data[['view_count','like_count','comment_count','category_id']].fillna(0).astype(int)
                videos_data['published_at'] = pd.to_datetime(videos_data['published_at'])
                videos_data['duration'] = pd.to_timedelta(videos_data['duration'], errors='coerce')
                def get_category_mapping():
                    request = youtube.videoCategories().list(
                        part='snippet',
                        regionCode='IN'
                    )
                    response = request.execute()
                    category_mapping = {}
                    for item in response['items']:
                        category_id = int(item['id'])
                        category_name = item['snippet']['title']
                        category_mapping[category_id] = category_name
                    return category_mapping
                
                # get the category mapping
                category_mapping = get_category_mapping()
                videos_data['category_name'] = videos_data['category_id'].map(category_mapping)

                col1,col2=st.columns([2,2])
                with col1:
                     st.image(channel_data['thumbnail'],width=400)
                with col2:
                    st.markdown(f"""
                                    <style>
                                        .custom-font {{
                                            font-family: Arial, sans-serif;
                                            font-size: 30px;
                                        }}
                                        .bold {{
                                            font-weight: bold;
                                        }}
                                    </style>
                                    <div class="custom-font">
                                        <span class="bold">Channel Name:</span> {channel_data['channel_name']}
                                    </div>
                                """, unsafe_allow_html=True)
                    st.markdown(" ")
                    st.markdown(f"""
                                    <style>
                                        .custom-font {{
                                            font-family: Arial, sans-serif;
                                            font-size: 30px;
                                        }}
                                        .bold {{
                                            font-weight: bold;
                                        }}
                                    </style>
                                    <div class="custom-font">
                                        <span class="bold">Subscribers:</span> {channel_data['subscriber_count']}
                                    </div>
                                """, unsafe_allow_html=True)
                    st.markdown(" ")
                    st.markdown(f"""
                                    <style>
                                        .custom-font {{
                                            font-family: Arial, sans-serif;
                                            font-size: 30px;
                                        }}
                                        .bold {{
                                            font-weight: bold;
                                        }}
                                    </style>
                                    <div class="custom-font">
                                        <span class="bold">Channel Views:</span> {channel_data['channel_views']}
                                    </div>
                                """, unsafe_allow_html=True)
                    st.markdown(" ")
                    st.markdown(f"""
                                    <style>
                                        .custom-font {{
                                            font-family: Arial, sans-serif;
                                            font-size: 30px;
                                        }}
                                        .bold {{
                                            font-weight: bold;
                                        }}
                                    </style>
                                    <div class="custom-font">
                                        <span class="bold">Total Videos:</span> {channel_data['total_videos']}
                                    </div>
                                """, unsafe_allow_html=True)
                    


                    st.markdown(" ")
                    st.markdown(f"""
                        <style>
                            .custom-font {{
                                font-family: Arial, sans-serif;
                                font-size: 30px;
                            }}
                            .bold {{
                                font-weight: bold;
                            }}
                        </style>
                        <div class="custom-font">
                            <span class="bold">Average Views:</span> {videos_data['view_count'].mean():.2f}
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown(" ")
                    st.markdown(f"""
                        <style>
                            .custom-font {{
                                font-family: Arial, sans-serif;
                                font-size: 30px;
                            }}
                            .bold {{
                                font-weight: bold;
                            }}
                        </style>
                        <div class="custom-font">
                            <span class="bold">Average Likes:</span> {videos_data['like_count'].mean():.2f}
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown(" ")
                    st.markdown(f"""
                        <style>
                            .custom-font {{
                                font-family: Arial, sans-serif;
                                font-size: 30px;
                            }}
                            .bold {{
                                font-weight: bold;
                            }}
                        </style>
                        <div class="custom-font">
                            <span class="bold">Average Comments:</span> {videos_data['comment_count'].mean():.2f}
                        </div>
                    """, unsafe_allow_html=True)

  #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

                top3 = videos_data[['video_name','published_at','duration','view_count','thumbnails','like_count','comment_count']].sort_values(by='view_count', ascending=False).head(3)

                with st.container():
                        st.markdown("""<div style="font-family: Arial; line-height: 1.6; padding: 20px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
                    <h1 style="color: #FF0000; font-size: 30px; ">Top 3 Viewed Videos</h1>
                    </div>""", unsafe_allow_html=True)
                        
                        cols = st.columns(3)
                                
                        for i in range(3):
                            with cols[i]:
                                st.image(top3.iloc[i]['thumbnails'], use_column_width=True)
                                st.subheader(top3.iloc[i]['video_name'])
                                st.markdown(f"<p style='font-size: 20px; text-align: center;'><strong>Views:</strong> {top3.iloc[i]['view_count']}</p>", 
                                    unsafe_allow_html=True)
                                st.markdown(f"<p style='font-size: 20px; text-align: center;'><strong>Likes:</strong> {top3.iloc[i]['like_count']}</p>", 
                                    unsafe_allow_html=True)
                                st.markdown(f"<p style='font-size: 20px; text-align: center;'><strong>Comments:</strong> {top3.iloc[i]['comment_count']}</p>", 
                                    unsafe_allow_html=True)
                                st.markdown(f"<p style='font-size: 20px; text-align: center;'><strong>Upoaded on:</strong> {top3.iloc[i]['published_at'].strftime('%d/%m/%Y %H:%M:%S')}</p>", 
                                    unsafe_allow_html=True)
                
                videos_data['publish_date'] = videos_data['published_at'].dt.date

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

                st.markdown(" ")
                st.markdown(" ")
                st.markdown("""
                <div style="font-family: Arial; line-height: 1.6; padding: 20px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
                    <h1 style="color: #FF0000; font-size: 30px;">Views of Recent 20 Videos</h1>
                </div>
                """, unsafe_allow_html=True)
                # View Count of Recent 20 Videos

                by_date=videos_data.sort_values(by='publish_date', ascending=False).head(20)
                fig = px.bar(by_date,
                    x='publish_date',
                    y='view_count',
                    title='Views with upload date', hover_data={'Title':by_date['video_name'], 'Uploaded Date':by_date['publish_date'], 'Views':by_date['view_count'],
                                                                'publish_date':False, 'view_count':False}, text='publish_date',
                    height=700, width=1400, color=by_date['view_count'], color_continuous_scale='matter'
                )
                fig.update_layout(xaxis_title='Uploaded Date', yaxis_title='View Count')
                st.plotly_chart(fig)


  #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

                st.markdown(" ")
                st.markdown(" ")
                st.markdown("""
                <div style="font-family: Arial; line-height: 1.6; padding: 20px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
                    <h1 style="color: #FF0000; font-size: 30px;">Videos in Each Category</h1>
                </div>
                """, unsafe_allow_html=True)

                category_counts = videos_data['category_name'].value_counts()
                fig = px.pie(
                    category_counts,
                    names=category_counts.index,  # Categories
                    values=category_counts.values,  # Proportions (number of videos)
                    title='Proportion of Videos by Category',
                    labels={'category_name': 'Category', 'values': 'Video Count'}, color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig.update_layout(title='Proportion of Videos in Each Category', height=600, width=800)

                st.plotly_chart(fig)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

                st.markdown(" ")
                st.markdown(" ")
                st.markdown("""
                <div style="font-family: Arial; line-height: 1.6; padding: 20px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
                    <h1 style="color: #FF0000; font-size: 30px;">Heat Map of View, Likes and Comments</h1>
                </div>
                """, unsafe_allow_html=True)

                # Compute correlation matrix
                correlation_matrix = videos_data[['view_count', 'like_count', 'comment_count']].corr()

                # Plot the correlation heatmap
                fig = ff.create_annotated_heatmap(
                    z=correlation_matrix.values,
                    x=['View Count', 'Like Count', 'Comment Count'],
                    y=['View Count', 'Like Count', 'Comment Count'],
                    annotation_text=correlation_matrix.round(2).values,
                    colorscale='Viridis'
                )
                fig.update_layout(title='Correlation Between Views, Likes, and Comments', height=600, width=800)

                st.plotly_chart(fig)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#                
                
                st.markdown(" ")
                st.markdown(" ")
                st.markdown("""
                <div style="font-family: Arial; line-height: 1.6; padding: 20px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
                    <h1 style="color: #FF0000; font-size: 30px;">Views and Likes over Time</h1>
                </div>
                """, unsafe_allow_html=True)

                # View, Like, and Comment Trends Over Time
                fig = px.line(videos_data,
                     x='published_at',
                     y=['view_count', 'like_count'], hover_data={'Title':videos_data['video_name'], 'Likes': videos_data['like_count'], 'Views':videos_data['view_count'],
                                                                 'value':False, 'variable':False},
                     title='View, Like, and Comment Trends Over Time')
                fig.update_layout(legend_title_text='Metric', xaxis_title='Published Date', yaxis_title='Views Count', height=600, width=1300)

                st.plotly_chart(fig)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

                st.markdown(" ")
                st.markdown(" ")
                st.markdown("""
                <div style="font-family: Arial; line-height: 1.6; padding: 20px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
                    <h1 style="color: #FF0000; font-size: 30px;">Comparing  Views with Duration of Video</h1>
                </div>
                """, unsafe_allow_html=True)

                def convert_to_hms(duration):
                    if pd.isnull(duration):
                        return "00:00:00"
                    duration_str = duration.isoformat()
                    seconds = isodate.parse_duration(duration_str).total_seconds()
                    hours = int(seconds // 3600)
                    minutes = int((seconds % 3600) // 60)
                    seconds = int(seconds % 60)
                    return f"{hours:02}:{minutes:02}:{seconds:02}"

                videos_data['duration_hms'] = videos_data['duration'].apply(convert_to_hms)

                # Video Duration vs. View Count
                fig = px.scatter(videos_data,
                                                x='duration',
                                                y='view_count', color='view_count', hover_data={'Title':videos_data['video_name'],'Duration': videos_data['duration_hms'], 'duration':False},
                                                color_continuous_scale='Inferno',
                                                labels={'duration_minutes': 'Duration (minutes)', 'view_count': 'View Count'},
                                                title='Video Duration vs. View Count', height=600, width=1300)
                
                st.plotly_chart(fig)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

                st.markdown(" ")
                st.markdown(" ")
                st.markdown("""
                <div style="font-family: Arial; line-height: 1.6; padding: 20px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
                    <h1 style="color: #FF0000; font-size: 30px;">Comparing  Likes with Duration of Video</h1>
                </div>
                """, unsafe_allow_html=True)

                # Video Duration vs. Like Count
                fig = px.scatter(videos_data,
                                x='duration',
                                y='like_count', color='like_count', hover_data={'Title':videos_data['video_name'],'Duration': videos_data['duration_hms'], 'duration':False},
                                color_continuous_scale='Inferno',
                                labels={'duration_minutes': 'Duration (minutes)', 'like_count': 'Like Count'},
                                title='Video Duration vs. Like Count', height=600, width=1300)
                
                st.plotly_chart(fig)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

                st.markdown(" ")
                st.markdown(" ")
                st.markdown("""
                <div style="font-family: Arial; line-height: 1.6; padding: 20px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
                    <h1 style="color: #FF0000; font-size: 30px;">Comparing  Comments with Duration of Video</h1>
                </div>
                """, unsafe_allow_html=True)

                # Video Duration vs. Comment Count
                fig = px.scatter(videos_data,
                                x='duration',
                                y='comment_count', color='comment_count', hover_data={'Title':videos_data['video_name'],'Duration': videos_data['duration_hms'], 'duration':False},
                                color_continuous_scale='Inferno',
                                labels={'duration_minutes': 'Duration (minutes)', 'comment_count': 'Comment Count'},
                                title='Video Duration vs. Comment Count', height=600, width=1300)
                
                st.plotly_chart(fig)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

                st.markdown(" ")
                st.markdown(" ")
                st.markdown("""
                <div style="font-family: Arial; line-height: 1.6; padding: 20px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
                    <h1 style="color: #FF0000; font-size: 30px;">Number of Uploads in Each Month</h1>
                </div>
                """, unsafe_allow_html=True)

                videos_data['month'] = videos_data['published_at'].dt.to_period('M')
                monthly_uploads = videos_data['month'].value_counts().sort_index()
                fig = px.bar(monthly_uploads,
                                    x=monthly_uploads.index.astype(str),
                                    y=monthly_uploads.values, color_continuous_scale='Turbo', hover_data={'Month':monthly_uploads.index.astype(str), 'Uploads':monthly_uploads.values},
                                    labels={'x': 'Month', 'y': 'Uploads'},
                                    title='Video Upload Frequency by Month', text=monthly_uploads.values, color=monthly_uploads.values, height=600, width=1300)
                
                st.plotly_chart(fig)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

                st.markdown(" ")
                st.markdown(" ")
                st.markdown("""
                <div style="font-family: Arial; line-height: 1.6; padding: 20px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
                    <h1 style="color: #FF0000; font-size: 30px;">Number of Uploads in Each Month</h1>
                </div>
                """, unsafe_allow_html=True)

                # Top 10 Liked Videos
                top_liked = videos_data.nlargest(10, 'like_count')
                top_liked = top_liked.sort_values(by='like_count', ascending=True)
                # Top 10 Commented Videos
                top_comment = videos_data.nlargest(10, 'comment_count')
                top_comment = top_comment.sort_values(by='comment_count', ascending=True)

                fig = make_subplots(rows=2, cols=1, subplot_titles=['Top 10 Liked Videos', 'Top 10 Commented Videos'])

                fig.add_trace(go.Bar(
                    y=top_liked['video_name'], x=top_liked['like_count'], hovertext=top_liked['like_count'],
                    orientation='h', marker=dict(color=top_liked['like_count'], colorscale='mint'), showlegend=False
                ), row=1, col=1)

                fig.add_trace(go.Bar(
                    y=top_comment['video_name'], x=top_comment['comment_count'], hovertext=top_comment['comment_count'],
                    orientation='h', marker=dict(color=top_comment['comment_count'], colorscale='mint'), showlegend=False
                ), row=2, col=1)

                fig.update_layout(
                    xaxis_title='Like Count',
                    yaxis_title='Video Name',
                    xaxis2_title='Comment Count',
                    yaxis2_title='Video Name', height=1200, width=1300
                )

                st.plotly_chart(fig)


        else:
            st.warning("Please enter a YouTube Channel ID.")

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

    

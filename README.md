# YouTube Analysis

Visit: https://youtube-analysis-st.streamlit.app/

This project provides an in-depth analysis of YouTube trending videos and channel data using various Python libraries like `Pandas`, `Matplotlib`, `Seaborn`, and `Plotly`. It pulls data using the YouTube Data API and displays interactive visualizations with the help of `Streamlit`. The project offers insights into video performance, viewership patterns, and channel statistics in an easy-to-navigate web app.

## 🔍 Features

- **Trending Video Analysis**: Pulls and analyzes trending video data such as views, likes, comments, and more.
- **Channel Performance**: Examines the performance of specific YouTube channels, including subscribers, video count, and total views.
- **Visualizations**: Dynamic charts using `Seaborn`, `Matplotlib`, and `Plotly` to visualize data trends like:
  - View count distribution
  - Like and comment count distributions
  - Correlation matrix between metrics
  - Video upload patterns by date and time
- **Streamlit Web App**: Interactive web interface to easily view and analyze data.

## 🚀 Installation

### Prerequisites

- Python 3.7+
- YouTube Data API Key

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YourUsername/YouTube-Analysis.git
   cd YouTube-Analysis
   ```

2. **Install required libraries**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API key**:
   - Get a YouTube Data API key [here](https://console.cloud.google.com/apis/credentials).
   - Add your API key in the `youtube_analysis.py` file:
     ```python
     API_KEY = 'YOUR_API_KEY'
     ```

4. **Run the Streamlit app**:
   ```bash
   streamlit run youtube_analysis.py
   ```

## 📈 Visualizations

- **View Count Distribution**: Displays how often different view counts occur.
- **Like & Comment Count**: Shows distributions of likes and comments for the trending videos.
- **Correlation Analysis**: Analyze correlations between video performance metrics.
- **Upload Patterns**: Visualizes video upload frequency by date and time.

## 🛠️ Technologies Used

- **Pandas**: For data manipulation and cleaning.
- **Matplotlib & Seaborn**: For generating static plots.
- **Plotly**: For interactive visualizations.
- **Streamlit**: For building the web-based interface.

## 💡 How It Works

1. **Data Collection**: The YouTube Data API is used to retrieve data about trending videos and channel statistics.
2. **Data Cleaning**: Pandas is used to process and clean the raw data.
3. **Visualization**: Seaborn, Matplotlib, and Plotly are used to create interactive and informative visualizations.
4. **Web App**: Streamlit is used to create a simple and intuitive web app for exploring the data.

## 🤔 Future Improvements

- Add more detailed visualizations for channel comparisons.
- Integrate additional metrics such as video tags, video length, and region-based analysis.
- Include predictive analysis for video success.

## 👨‍💻 Author

- **Mithul C B**

Feel free to contribute or reach out with any suggestions or improvements!

---

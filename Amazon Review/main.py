import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import plotly.express as px
from sklearn.metrics import accuracy_score, classification_report

# Streamlit configuration
st.set_page_config(page_title="Sentiment Analysis System", page_icon="https://cdn3.iconfinder.com/data/icons/artificial-intelligence-123/24/sentiment_analysis_feeling_emotion_emoji_recognition_expression-512.png")
st.title("AMAZON REVIEW SENTIMENT ANALYSIS SYSTEM")

# Sidebar for navigation
choice = st.sidebar.selectbox("Navigation", ("HOME", "ANALYSIS", "RESULTS"))

if choice == "HOME":
    st.image("https://i.gifer.com/7SpK.gif")
    st.write("1. This is a Natural Language Processing application for analyzing text sentiment.")
    st.write("2. It classifies sentiments into Positive, Negative, and Neutral.")
    st.write("3. Visualize results based on review title and body.")

elif choice == "ANALYSIS":
    st.subheader("Analyze Sentiment")
    sid = st.text_input("Google Sheet ID")
    r = st.text_input("Range (e.g., A:D)")
    c = st.text_input("Column to Analyze")
    
    if st.button("Analyze"):
        if 'cred' not in st.session_state:
            f = InstalledAppFlow.from_client_secrets_file("key.json", ["https://www.googleapis.com/auth/spreadsheets"])
            st.session_state['cred'] = f.run_local_server(port=0)
        
        mymodel = SentimentIntensityAnalyzer()
        service = build("sheets", "v4", credentials=st.session_state['cred']).spreadsheets().values()
        result = service.get(spreadsheetId=sid, range=r).execute()
        data = result['values']
        
        df = pd.DataFrame(data[1:], columns=data[0])
        sentiments = []
        
        for i in range(len(df)):
            text = df._get_value(i, c)
            pred = mymodel.polarity_scores(text)
            if pred['compound'] > 0.5:
                sentiments.append("Positive")
            elif pred['compound'] < -0.5:
                sentiments.append("Negative")
            else:
                sentiments.append("Neutral")
        
        df['Sentiment'] = sentiments
        df.to_csv("results.csv", index=False)
        st.success("Analysis completed and results saved to results.csv")

elif choice == "RESULTS":
    st.subheader("View Results")
    df = pd.read_csv("results.csv")
    st.dataframe(df)

    # Visualization options
    visualization = st.selectbox("Choose Visualization", ("NONE", "PIE CHART", "HISTOGRAM", "SCATTER PLOT"))
    
    if 'ActualSentiment' in df.columns:
        # Accuracy metrics
        accuracy = accuracy_score(df['ActualSentiment'], df['Sentiment'])
        report = classification_report(df['ActualSentiment'], df['Sentiment'])
        
        st.subheader("Accuracy Metrics")
        st.write(f"**Accuracy**: {accuracy:.2f}")
        st.text("**Classification Report**:")
        st.text(report)
    
    if visualization == "PIE CHART":
        pos_perc = (len(df[df['Sentiment'] == 'Positive']) / len(df)) * 100
        neg_perc = (len(df[df['Sentiment'] == 'Negative']) / len(df)) * 100
        neu_perc = (len(df[df['Sentiment'] == 'Neutral']) / len(df)) * 100
        fig = px.pie(values=[pos_perc, neg_perc, neu_perc], names=['Positive', 'Negative', 'Neutral'])
        st.plotly_chart(fig)
    
    elif visualization == "HISTOGRAM":
        col = st.selectbox("Select Column for Histogram", df.columns)
        if col:
            fig = px.histogram(df, x=col, color='Sentiment')
            st.plotly_chart(fig)
    
    elif visualization == "SCATTER PLOT":
        col = st.text_input("Enter Column for Scatter Plot")
        if col and col in df.columns:
            fig = px.scatter(df, x=col, y='Sentiment')
            st.plotly_chart(fig)

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

# Initialize Sentiment Analyzer
mymodel = SentimentIntensityAnalyzer()

# Authenticate and build the Google Sheets service
f = InstalledAppFlow.from_client_secrets_file("key.json", ["https://www.googleapis.com/auth/spreadsheets"])
cred = f.run_local_server(port=0)
service = build("sheets", "v4", credentials=cred).spreadsheets().values()

# Fetch data from Google Sheets
sheet_id = "1nrJ0kYiVs_Dvm-1YYEFOpOmihamE4Q8vzEUEA0s8l_Q"
range_name = "A:D"
result = service.get(spreadsheetId=sheet_id, range=range_name).execute()
data = result.get('values', [])

# Convert to DataFrame
df = pd.DataFrame(data[1:], columns=data[0])

# Analyze sentiment based on 'ReviewBody'
sentiments = []
for i in range(len(df)):
    text = df._get_value(i, "ReviewBody")
    pred = mymodel.polarity_scores(text)
    if pred['compound'] > 0.5:
        sentiments.append("Positive")
    elif pred['compound'] < -0.5:
        sentiments.append("Negative")
    else:
        sentiments.append("Neutral")

# Update DataFrame with sentiments
df['Feedback'] = sentiments

# Convert DataFrame back to list of lists for Google Sheets update
updated_data = [df.columns.values.tolist()] + df.values.tolist()

# Update Google Sheets
body = {'values': updated_data}
service.update(spreadsheetId=sheet_id, range="A:E", valueInputOption="USER_ENTERED", body=body).execute()

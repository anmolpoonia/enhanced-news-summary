# Enhanced-News-Summary
A project that fetches news, analyzes trends, forecasts sentiment, and updates GitHub automatically.

## **Project Purpose**
This project is designed to automate the process of fetching, summarizing, and analyzing news from multiple sources. By leveraging Python scripts, Natural Language Processing (NLP) models, and data visualization techniques, the system provides insights into the latest news trends. It automatically updates twice a day using GitHub Actions.

---

## **Key Features**

### **1. Automated News Fetching**
- Pulls the latest articles from:
  - **VentureBeat**: Technology-focused news.
  - **NewsAPI**: News from multiple sources like TechCrunch and Reuters.

### **2. Summarization and Sentiment Analysis**
- **Summarization**: Generates concise summaries of the news headlines.
- **Sentiment Analysis**: Classifies news sentiments (Positive, Neutral, Negative).

### **3. Data Storage and Visualization**
- **News History**: Stores all fetched news in `news_history.csv` for historical tracking.
- **Word Cloud**: Visualizes the most frequent words from recent headlines (example below).
- **Leaderboard**: Lists the top 5 most discussed words in the headlines.

### **4. Sentiment Forecasting**
- Uses **Prophet** to predict future sentiment trends based on historical data.

### **5. Automated Updates with GitHub Actions**
- Runs twice daily (at 9 AM and 6 PM UTC) to fetch the latest news and push updates to the GitHub repository.

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/daily-news-summary.git
cd daily-news-summary
```

### **2. Install Dependencies**
Ensure you have Python 3.9+ installed, then run:
```bash
pip install -r requirements.txt
```

### **3. Run the Script Locally**
```bash
python daily_news.py
```
Check the output files in the project directory:
- `news_summary.txt`
- `word_cloud.png`
- `leaderboard.txt`
- `news_history.csv`

### **4. Deploy Automation**
1. Ensure the `.github/workflows/news_update.yml` file is correctly set up for GitHub Actions.
2. Push the repository to GitHub:
   ```bash
   git add .
   git commit -m "Deploy automation"
   git push origin main
   ```
3. GitHub Actions will run automatically twice daily.

---

## **Example Outputs**

### **Word Cloud**
Below is an example of the word cloud generated from recent news headlines:

![word_cloud](https://github.com/user-attachments/assets/b9e52a14-204d-4164-85f7-fa928212cf02)


### **Leaderboard**
Example of the leaderboard output (`leaderboard.txt`):
```
Top 5 Words in News Titles:
AI: 15 mentions
Nvidia: 12 mentions
Justin: 8 mentions
Trudeau: 8 mentions
Platform: 7 mentions
```

---

## **Workflow Description**

### **Automated Updates with GitHub Actions**

#### **Workflow Configuration**
The workflow file `.github/workflows/news_update.yml` is configured to:
1. Run twice daily (9 AM and 6 PM UTC).
2. Perform the following steps:
   - Clone the repository.
   - Set up Python and install dependencies.
   - Execute the `daily_news.py` script.
   - Commit and push the updated files back to the repository.

#### **Example Workflow File**
```yaml
name: Daily News Update

on:
  schedule:
    - cron: "0 9,18 * * *"
  workflow_dispatch:

jobs:
  update-news:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.9

    - name: Install dependencies
      run: |
        pip install requests beautifulsoup4 pandas matplotlib wordcloud transformers prophet sklearn

    - name: Run daily news script
      run: python daily_news.py

    - name: Commit and push changes
      run: |
        git config --global user.email "youremail@example.com"
        git config --global user.name "Your Name"
        git add .
        git commit -m "Automated daily update"
        git push
```

---

## **How to Monitor the Automation**

1. **GitHub Actions Tab**:
   - Go to the **Actions** tab in your repository.
   - Check the logs for the `Daily News Update` workflow.

2. **Repository Updates**:
   - Ensure files (`news_summary.txt`, `word_cloud.png`, etc.) are updated twice daily.
   - Look for commit messages like "Automated daily update."

---

## **Future Enhancements**
1. **Interactive Dashboard**:
   - Use tools like Streamlit or Dash to create a live news and sentiment dashboard.
2. **Additional Data Sources**:
   - Integrate more APIs (e.g., Google News API, BBC News API).
3. **Email Notifications**:
   - Send daily news summaries to a mailing list.
4. **Advanced NLP Models**:
   - Upgrade summarization and sentiment analysis using fine-tuned Transformer models.

---

For any questions or contributions, feel free to raise an issue or submit a pull request!


import aiohttp  # For data fetching
import os
import asyncio
import json  # For returning results as JSON
from agentex import Swarm, CentralHub, Agent, AsyncAgentTask
from agentex.logging.logger import LoggerWrapper
from textblob import TextBlob

# --------- Task Implementations --------- #

# 1. Asynchronous RSS News Fetch Task
class RSSNewsFetchTask(AsyncAgentTask):
    def __init__(self, task_name, description, rss_url, logger=None):
        super().__init__(task_name, description, logger)
        self.rss_url = rss_url

    async def execute(self):
        """Fetches RSS feed articles asynchronously and returns as JSON."""
        self.logger.dprint(f"[RSS NEWS FETCH TASK] Fetching articles from {self.rss_url}...", level="info")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.rss_url, timeout=10) as response:
                    if response.status == 200:
                        text = await response.text()
                        import feedparser
                        feed = feedparser.parse(text)
                        articles = [{"title": entry.title, "summary": entry.get("summary", "")} for entry in feed.entries]

                        self.result = json.dumps({
                            "status": "success",
                            "num_articles_fetched": len(articles),
                            "articles": articles
                        }) if articles else json.dumps({
                            "status": "error",
                            "message": "No articles found."
                        })

                        self.logger.dprint(f"[RSS NEWS FETCH TASK] Success! Articles fetched: {len(articles)}", level="debug")
                        return self.result
                    else:
                        self.result = json.dumps({
                            "status": "error",
                            "message": f"Failed to fetch articles (status code: {response.status})"
                        })
                        self.logger.dprint(f"[ERROR] Failed to fetch articles (status code: {response.status})", level="error")
        except Exception as e:
            self.result = json.dumps({
                "status": "error",
                "message": f"Exception during RSS fetch: {str(e)}"
            })
            self.logger.dprint(f"[ERROR] Exception during RSS fetch: {str(e)}", level="error")


# 2. Asynchronous Sentiment Analysis Task
class SentimentAnalysisTask(AsyncAgentTask):
    def __init__(self, task_name, description, logger=None, articles=None):
        super().__init__(task_name, description, logger)
        self.articles = articles or []  # Store articles as an instance attribute

    def analyze_sentiment(self, text):
        """
        Analyze the sentiment of the given text using TextBlob and categorize it.
        Returns:
        - "Positive" for positive sentiment
        - "Neutral" for neutral sentiment
        - "Negative" for negative sentiment
        """
        analysis = TextBlob(text)
        sentiment_score = analysis.sentiment.polarity  # Polarity ranges from -1 to 1

        if sentiment_score > 0.1:
            return "Positive"
        elif sentiment_score < -0.1:
            return "Negative"
        else:
            return "Neutral"

    async def execute(self):
        """
        Perform sentiment analysis on a list of articles by combining title and summary.
        """
        if not self.articles:
            self.result = json.dumps({
                "status": "error",
                "message": "No articles available for sentiment analysis."
            })
            self.logger.dprint("[SENTIMENT ANALYSIS TASK] No articles available for sentiment analysis.", level="error")
            return self.result

        self.logger.dprint(f"[SENTIMENT ANALYSIS TASK] Analyzing sentiment of {len(self.articles)} articles...", level=0)

        sentiments = []
        for article in self.articles:
            title = article.get('title', 'Untitled')
            summary = article.get('summary', '')

            if not summary:
                self.logger.dprint(f"[WARNING] Article '{title}' has no summary text.", level="warning")
                combined_text = title  # Use only title if no summary is available
            else:
                combined_text = f"{title}. {summary}"  # Concatenate title and summary

            sentiment_label = self.analyze_sentiment(combined_text)  # Get sentiment category

            sentiments.append({
                'title': title,
                'sentiment': sentiment_label,
                'analyzed_text': combined_text  # Include analyzed text for transparency
            })

        self.result = json.dumps({
            "status": "success",
            "num_articles_analyzed": len(sentiments),
            "results": sentiments
        })
        return self.result


# --------- Workflow Execution --------- #
async def run_rss_news_analysis_workflow():
    logger = LoggerWrapper(log_level="info", use_exlog=True)
    silent_logger = LoggerWrapper(log_level=0, use_exlog=True)  # Silent for BaseTask.log()

    central_hub = CentralHub(logger=logger)
    swarm = Swarm("RSSNewsAnalysisSwarm", central_hub=central_hub, logger=logger)

    # Agents
    agent_fetch = Agent("RSSNewsFetcherAgent", logger=logger)
    agent_sentiment = Agent("SentimentAnalyzerAgent", logger=logger)
    swarm.add_agent(agent_fetch)
    swarm.add_agent(agent_sentiment)

    # RSS Fetch Task
    rss_url = "http://rss.cnn.com/rss/edition.rss"
    rss_fetch_task = RSSNewsFetchTask("rss_news_fetch_task", "Fetches news articles", rss_url, logger=silent_logger)

    # Fetch articles
    await agent_fetch.async_assign_task(rss_fetch_task, print_full_result=False)
    articles_json = rss_fetch_task.get_result()  # Properly fetch result
    articles = json.loads(articles_json).get("articles", [])

    if not articles:
        logger.dprint("[ERROR] No articles fetched from the RSS feed.", level="error")
        return

    # Sentiment Analysis Task
    sentiment_task = SentimentAnalysisTask("sentiment_analysis_task", "Analyze sentiment of news articles", logger=silent_logger, articles=articles)

    # Perform sentiment analysis
    await agent_sentiment.async_assign_task(sentiment_task, print_full_result=False)
    sentiment_results_json = sentiment_task.get_result()
    sentiment_results = json.loads(sentiment_results_json)

    if sentiment_results.get("status") == "error":
        logger.dprint("[ERROR] Sentiment analysis returned no results.", level="error")
    else:
        logger.dprint("[SUCCESS] Sentiment Analysis Completed. Below are the results:", level="info")
        for result in sentiment_results['results']:
            print(f"[RESULT] {result['title']} -> Sentiment: {result['sentiment']}")

def main():
    print("[STARTING RSS NEWS SENTIMENT WORKFLOW]")
    asyncio.run(run_rss_news_analysis_workflow())


if __name__ == "__main__":
    main()

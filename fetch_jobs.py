import os
import requests

# Slack Webhook URL（GitHub Secrets から読み込まれる想定）
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

# 🔍 検索条件（ここを変えるだけで自由に検索可能）
SEARCH_KEYWORDS = ["事務", "施工管理"]

def get_jobs():
    """
    本来はスクレイピングやAPIで取得する部分。
    今はサンプルデータを用意して、検索キーワードでフィルタリングする。
    """

    sample_jobs = [
        {
            "title": "【60代活躍中】半導体製造装置の立ち上げ・プロセス技術支援",
            "company": "株式会社〇〇テクノロジー",
            "location": "熊本県",
            "age_target": "60歳代活躍中・定年退職者歓迎",
            "salary": "年収 800万円〜1,200万円",
            "url": "https://example.com"
        },
        {
            "title": "【経験者優遇・シニア歓迎】プラント建設の電気計装施工管理",
            "company": "〇〇建設エンジニアリング",
            "location": "神奈川県川崎市",
            "age_target": "60歳代活躍中（1級資格者）",
            "salary": "日給 18,000円〜25,000円",
            "url": "https://example.com"
        },
        {
            "title": "一般事務スタッフ（データ入力・書類作成）",
            "company": "〇〇オフィスサービス",
            "location": "東京都港区",
            "age_target": "シニア歓迎",
            "salary": "時給 1,400円〜1,800円",
            "url": "https://example.com"
        }
    ]

    # 🔎 キーワードでフィルタリング
    filtered_jobs = [
        job for job in sample_jobs
        if any(keyword in job["title"] for keyword in SEARCH_KEYWORDS)
    ]

    return filtered_jobs


def send_to_slack(jobs):
    if not jobs:
        print("新規求人はありませんでした。")
        return

    # Slack Block Kit
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "📋 本日の新着求人（事務・施工管理）"
            }
        },
        {"type": "divider"}
    ]

    for job in jobs:
        job_text = (
            f"*{job['title']}*\n"
            f"🏢 企業名: {job['company']}\n"
            f"📍 勤務地: {job['location']}\n"
            f"🎯 ターゲット: {job['age_target']}\n"
            f"💰 給与: {job['salary']}\n"
            f"🔗 <{job['url']}|求人詳細はこちら>"
        )

        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": job_text}
        })
        blocks.append({"type": "divider"})

    payload = {"blocks": blocks}

    response = requests.post(SLACK_WEBHOOK_URL, json=payload)

    if response.status_code == 200:
        print("Slackへの通知が成功しました。")
    else:
        print(f"Slackへの通知に失敗しました: {response.status_code}")


if __name__ == "__main__":
    job_list = get_jobs()
    send_to_slack(job_list)

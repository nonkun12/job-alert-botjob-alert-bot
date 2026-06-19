import os
import requests

# 💡 ここはそのまま。本物のURLはGitHubの隠し部屋（Secrets）から自動で読み込まれます
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

def get_jobs():
    # テスト用のサンプルデータです
    return [
        {"title": "Pythonエンジニア（リモート可）", "company": "Tech Corp", "url": "https://example.com/job1"},
        {"title": "データサイエンティスト", "company": "AI Lab", "url": "https://example.com/job2"}
    ]

def send_to_slack(jobs):
    if not jobs:
        print("新規求人はありませんでした。")
        return

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "🔔 本日の新着求人情報"}
        }
    ]

    for job in jobs:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*【{job['company']}】*\n<{job['url']}|{job['title']}>"
            }
        })

    payload = {"blocks": blocks}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    
    if response.status_code == 200:
        print("Slackへの通知が成功しました。")
    else:
        print(f"Slackへの通知に失敗しました: {response.status_code}")

if __name__ == "__main__":
    job_list = get_jobs()
    send_to_slack(job_list)

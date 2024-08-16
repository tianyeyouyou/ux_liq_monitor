import requests
import json
import time
import traceback

# URL to send the GET request to
url = "https://testnet-client-bff-ocstrhuppq-uc.a.run.app/inspect/75"

# DingTalk webhook URLs (replace with your actual webhook URLs)
startup_webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_ACCESS_TOKEN_STARTUP"
notification_webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_ACCESS_TOKEN_NOTIFICATION"

# Function to send a notification to DingTalk
def send_dingtalk_notification(message, webhook_url):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print("Notification sent successfully")
        else:
            print(f"Failed to send notification. HTTP Status code: {response.status_code}")
    except Exception as e:
        print(f"Exception occurred while sending notification: {e}")
        traceback.print_exc()

# Function to perform the main task
def main_task():
    try:
        # Send the GET request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Iterate through the borrowers
            for borrower in data.get("borrowers", []):
                analysis = borrower.get("analysis", {})
                value = float(analysis.get("Value", 0))

                # Check if the value is greater than 100
                if value > 100:
                    borrowed_list = borrower.get("position", {}).get("borrowed", [])
                    symbols = [borrowed_item.get("symbol", "Unknown") for borrowed_item in borrowed_list]
                    symbols_str = ", ".join(symbols)
                    message = f"new ux liqudation > 100, symbols: {symbols_str}"

                    # Send notification to the notification group
                    send_dingtalk_notification(message, notification_webhook_url)
        else:
            print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")
    except Exception as e:
        print(f"Exception occurred during main task: {e}")
        traceback.print_exc()

# Send startup notification to the startup group
send_dingtalk_notification("ux liq monitor started", startup_webhook_url)

# Loop to run the main task every minute
while True:
    main_task()
    # Sleep for 60 seconds
    time.sleep(60)
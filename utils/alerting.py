import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

THRESHOLD = 1000  # BTC
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
ALERT_EMAIL = os.getenv("ALERT_EMAIL")

def check_alerts_and_send_email(df):
    alerts = []
    if 'Delta (BTC)' not in df.columns:
        return alerts

    significant_moves = df[abs(df['Delta (BTC)']) > THRESHOLD]
    for _, row in significant_moves.iterrows():
        alerts.append(row['Address'])
        send_email_alert(row)
    return alerts

def send_email_alert(row):
    if SENDGRID_API_KEY and ALERT_EMAIL:
        message = Mail(
            from_email='whaletracker@example.com',
            to_emails=ALERT_EMAIL,
            subject=f"Whale Alert: {row['Delta (BTC)']} BTC movement",
            html_content=f"""
            <strong>Wallet:</strong> {row['Address']}<br>
            <strong>Balance Change:</strong> {row['Delta (BTC)']} BTC<br>
            <strong>New Balance:</strong> {row['Balance (BTC)']} BTC<br>
            """
        )
        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            sg.send(message)
        except Exception as e:
            print(f"Error sending email: {e}")


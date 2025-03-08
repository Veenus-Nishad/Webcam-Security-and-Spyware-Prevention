import logging
import smtplib
from email.mime.text import MIMEText

#Log events and send alerts.

class Logger:
    def __init__(self):
        logging.basicConfig(
            filename='webcam_security.log',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def log_alert(self, message):
        logging.critical(message)
        self._send_email_alert(message)

    def _send_email_alert(self, message):
        # Configure email settings (example using Gmail)
        sender = "your_email@gmail.com"
        receiver = "admin@example.com"
        password = "your_app_password"  # Use app-specific password

        msg = MIMEText(message)
        msg['Subject'] = "Webcam Security Alert"
        msg['From'] = sender
        msg['To'] = receiver

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender, password)
                server.sendmail(sender, receiver, msg.as_string())
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
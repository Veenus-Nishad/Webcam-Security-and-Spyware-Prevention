import logging

class Logger:
    def __init__(self):
        """
        Initializes the logger.
        """
        logging.basicConfig(
            filename='webcam_security.log',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def log_alert(self, message):
        """
        Logs an alert message.
        """
        logging.critical(message)
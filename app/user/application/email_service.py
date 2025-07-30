import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import get_settings

settigs = get_settings()

class EmailService:
    def send_email(
        self,
        receiver_email: str,
    ):
        send_semail = "toquf2611@gmail.com"
        password = settigs.EMAIL_PASSWORD

        message = MIMEMultipart()
        message["From"] = send_semail
        message["To"] = receiver_email
        message['Subject'] = "회원 가입을 환영합니다."

        body = "새별 서비스를 이용해주셔서 감사합니다."
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(send_semail, password)
            server.send_message(message)
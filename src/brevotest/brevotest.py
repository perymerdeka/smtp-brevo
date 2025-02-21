import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv, dotenv_values
from pathlib import Path
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BrevoSMTPTest:
    def __init__(self, env_path=None):
        """
        Inisialisasi konfigurasi SMTP Brevo dari file .env.
        """
        # Menentukan path ke file .env
        if env_path is None:
            BASE_DIR = Path(__file__).resolve().parent.parent
            env_path = BASE_DIR / ".env"
        
        # Memuat variabel lingkungan
        self.env = dotenv_values(env_path)
        load_dotenv(env_path)
        
        # Konfigurasi SMTP Brevo
        self.smtp_server = os.getenv("SMTP_HOST")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")  # Master Password

        # Validasi konfigurasi
        if not all([self.smtp_server, self.smtp_port, self.smtp_username, self.smtp_password]):
            raise ValueError("Semua variabel lingkungan SMTP harus diatur.")

    def send_email(self, receiver_emails, subject, body_text, body_html=None):
        """
        Mengirim email ke satu atau banyak penerima.
        
        :param receiver_emails: List atau string email penerima
        :param subject: Subjek email
        :param body_text: Isi email dalam format teks biasa
        :param body_html: Isi email dalam format HTML (opsional)
        :return: Boolean indicating success
        """
        if isinstance(receiver_emails, str):
            receiver_emails = [receiver_emails]
        
        sender_email = os.getenv("SENDER_EMAIL", self.smtp_username)
        
        # Membuat pesan email dengan format multipart (plain text dan HTML jika disediakan)
        message = MIMEMultipart("alternative")
        message["From"] = sender_email
        message["To"] = ", ".join(receiver_emails)
        message["Subject"] = subject

        # Membuat objek MIMEText untuk plain text dan HTML
        part1 = MIMEText(body_text, "plain")
        message.attach(part1)

        if body_html:
            part2 = MIMEText(body_html, "html")
            message.attach(part2)
        
        try:
            # Membuka koneksi ke server SMTP Brevo
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Upgrade koneksi ke TLS untuk keamanan
            server.login(self.smtp_username, self.smtp_password)
            
            # Mengirim email
            server.sendmail(sender_email, receiver_emails, message.as_string())
            logger.info(f"Email berhasil dikirim ke: {receiver_emails}")
            return True
        except Exception as e:
            logger.error(f"Terjadi kesalahan saat mengirim email: {e}")
            return False
        finally:
            server.quit()

    def test_smtp_connection(self):
        """
        Menguji koneksi ke server SMTP.
        """
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.quit()
            logger.info("Koneksi SMTP berhasil.")
            return True
        except Exception as e:
            logger.error(f"Koneksi SMTP gagal: {e}")
            return False
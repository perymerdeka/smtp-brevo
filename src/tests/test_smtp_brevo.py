import os
import smtplib
import unittest
from pathlib import Path

# Pastikan sys.path mencakup direktori tempat brevo_smtp_test.py berada
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent / "brevotest"))

from brevo_smtp_test import BrevoSMTPTest  # Sesuaikan dengan nama file yang benar jika berbeda

class TestBrevoSMTPTest(unittest.TestCase):
    def setUp(self):
        """
        Setup sebelum setiap test dijalankan.
        """
        # Setting environment variables secara manual atau pastikan sudah diatur sebelumnya
        os.environ.setdefault("SMTP_HOST", "smtp.brevo.com")
        os.environ.setdefault("SMTP_PORT", "587")
        os.environ.setdefault("SMTP_USERNAME", "user@brevo.com")
        os.environ.setdefault("SMTP_PASSWORD", "securepassword")
        os.environ.setdefault("SENDER_EMAIL", "sender@brevo.com")
        
        # Inisialisasi instance BrevoSMTPTest
        self.smtp_test = BrevoSMTPTest()

    def tearDown(self):
        """
        Cleanup setelah setiap test dijalankan.
        """
        pass  # Tidak ada yang perlu dibersihkan karena tidak ada mock

    def test_send_email_success(self):
        """
        Test mengirim email berhasil.
        """
        receiver_emails = ["recipient1@example.com", "recipient2@example.com"]
        subject = "Test Subject"
        body_text = "This is a test email."
        body_html = "<p>This is a <strong>test</strong> email.</p>"

        # Panggil metode send_email
        result = self.smtp_test.send_email(receiver_emails, subject, body_text, body_html)

        # Assertions
        self.assertTrue(result)

    def test_send_email_failure(self):
        """
        Test mengirim email gagal karena informasi yang salah.
        """
        receiver_emails = ["recipient@example.com"]
        subject = "Test Subject"
        body_text = "This is a test email."

        # Ubah environment variable password untuk menyebabkan kegagalan login
        os.environ["SMTP_PASSWORD"] = "wrongpassword"

        # Panggil metode send_email
        result = self.smtp_test.send_email(receiver_emails, subject, body_text)

        # Assertions
        self.assertFalse(result)

    def test_test_smtp_connection_success(self):
        """
        Test koneksi SMTP berhasil.
        """
        result = self.smtp_test.test_smtp_connection()
        self.assertTrue(result)

    def test_test_smtp_connection_failure(self):
        """
        Test koneksi SMTP gagal karena informasi yang salah.
        """
        # Ubah environment variable password untuk menyebabkan kegagalan login
        os.environ["SMTP_PASSWORD"] = "wrongpassword"

        result = self.smtp_test.test_smtp_connection()
        self.assertFalse(result)

    def test_send_bulk_emails(self):
        """
        Test mengirim email ke banyak penerima berhasil.
        """
        # Membuat list dengan 100 email penerima
        receiver_emails = [f"recipient{i}@example.com" for i in range(1, 101)]
        subject = "Bulk Test Subject"
        body_text = "This is a bulk test email."
        body_html = "<p>This is a <strong>bulk test</strong> email.</p>"

        # Panggil metode send_email
        result = self.smtp_test.send_email(receiver_emails, subject, body_text, body_html)

        # Assertions
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
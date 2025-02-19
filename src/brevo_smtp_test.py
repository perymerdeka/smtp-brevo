import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

# Konfigurasi SMTP Brevo
smtp_server   = os.getenv("SMTP_HOST")
smtp_port     = os.getenv("SMTP_PORT")
smtp_username = os.getenv("SMTP_USERNAME")
smtp_password = os.getenv("SMTP_PASSWORD") # Master Password

# Data email
sender_email   = os.getenv("SENDER_EMAIL") #smtp_username
receiver_email = os.getenv("RECEIVER_EMAIL")  # Ganti dengan alamat email penerima
subject        = "Judul Email"
body_text      = "Ini adalah isi email dalam format teks biasa."
body_html      = "<html><body><p>Ini adalah isi email dalam format HTML.</p></body></html>"

# Membuat pesan email dengan format multipart (plain text dan HTML)
message = MIMEMultipart("alternative")
message["From"]    = sender_email
message["To"]      = receiver_email
message["Subject"] = subject

# Membuat objek MIMEText untuk plain text dan HTML
part1 = MIMEText(body_text, "plain")
part2 = MIMEText(body_html, "html")

# Melampirkan kedua bagian ke pesan email
message.attach(part1)
message.attach(part2)

try:
    # Membuka koneksi ke server SMTP Brevo
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Upgrade koneksi ke TLS untuk keamanan
    server.login(smtp_username, smtp_password)
    
    # Mengirim email
    server.sendmail(sender_email, receiver_email, message.as_string())
    print("Email berhasil dikirim!")
except Exception as e:
    print("Terjadi kesalahan saat mengirim email:", e)
finally:
    server.quit()
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_test_email(smtp_host, smtp_port, username, password, from_email, to_email, use_tls=True):
    """
    Send a test HTML email using provided SMTP credentials
    
    Args:
        smtp_host: SMTP server hostname (e.g., 'smtp.gmail.com')
        smtp_port: SMTP server port (e.g., 587 for TLS, 465 for SSL)
        username: SMTP username
        password: SMTP password
        from_email: Sender email address
        to_email: Recipient email address
        use_tls: Whether to use TLS (default: True)
    """
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'SMTP Test Email - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        msg['From'] = from_email
        msg['To'] = to_email
        
        # HTML content
        html_content = """
        <html>
            <head></head>
            <body>
                <h2 style="color: #2e6c80;">SMTP Test Email</h2>
                <p>This is a test email sent from your SMTP configuration.</p>
                <div style="background-color: #f0f0f0; padding: 15px; border-left: 4px solid #2e6c80;">
                    <h3>Configuration Details:</h3>
                    <ul>
                        <li><strong>SMTP Host:</strong> {smtp_host}</li>
                        <li><strong>SMTP Port:</strong> {smtp_port}</li>
                        <li><strong>Username:</strong> {username}</li>
                        <li><strong>From:</strong> {from_email}</li>
                        <li><strong>To:</strong> {to_email}</li>
                        <li><strong>Time:</strong> {timestamp}</li>
                    </ul>
                </div>
                <p style="color: green; font-weight: bold;">✓ If you received this email, your SMTP configuration is working correctly!</p>
            </body>
        </html>
        """.format(
            smtp_host=smtp_host,
            smtp_port=smtp_port,
            username=username,
            from_email=from_email,
            to_email=to_email,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Connect to SMTP server and send email
        print(f"Connecting to {smtp_host}:{smtp_port}...")
        
        if use_tls:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=30)
            server.ehlo()
            server.starttls()
            server.ehlo()
        else:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30)
            server.ehlo()
        
        print("Logging in...")
        server.login(username, password)
        
        print("Sending email...")
        server.send_message(msg)
        server.quit()
        
        print(f"✓ Email sent successfully to {to_email}!")
        return True
        
    except smtplib.SMTPException as e:
        print(f"✗ SMTP Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"✗ Error sending email: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # SMTP Configuration - Replace with your details
    SMTP_HOST = "smtp.gmail.com"  # e.g., smtp.gmail.com, smtp.office365.com, smtp.sendgrid.net
    SMTP_PORT = 587  # 587 for TLS, 465 for SSL
    USERNAME = "your-email@gmail.com"
    PASSWORD = "your-app-password"
    FROM_EMAIL = "your-email@gmail.com"
    TO_EMAIL = "recipient@example.com"
    USE_TLS = True  # Set to False if using SSL on port 465
    
    print("=" * 50)
    print("SMTP Tester - InvoIQ")
    print("=" * 50)
    
    send_test_email(
        smtp_host=SMTP_HOST,
        smtp_port=SMTP_PORT,
        username=USERNAME,
        password=PASSWORD,
        from_email=FROM_EMAIL,
        to_email=TO_EMAIL,
        use_tls=USE_TLS
    )

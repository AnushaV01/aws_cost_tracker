import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
import json
import sys

def test_email_connection(smtp_server, smtp_port, username, password):
    try:
        print(f"Testing connection to {smtp_server}:{smtp_port}")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        print("TLS connection established")
        
        server.login(username, password)
        print("Login successful!")
        
        server.quit()
        return True
    except Exception as e:
        print(f"Connection error: {str(e)}")
        return False

def test_database():
    try:
        print("Testing database connection...")
        conn = sqlite3.connect('aws_costs.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cost_data")
        count = cursor.fetchone()[0]
        print(f"Found {count} records in database")
        conn.close()
        return count > 0
    except Exception as e:
        print(f"Database error: {str(e)}")
        return False

def main():
    # Email settings
    settings = {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "username": "your-email@example.com",  # Replace with your email
        "password": "your-app-password",     # Replace with your app password(no spaces)
    }
    
    recipients = ["anymail@example.com"]  # Replace with recipient email

    print("Starting email sender diagnostic...")
    
    # Test email connection
    if not test_email_connection(settings["smtp_server"], 
                               settings["smtp_port"], 
                               settings["username"], 
                               settings["password"]):
        print("Email connection test failed!")
        sys.exit(1)

    # Test database
    if not test_database():
        print("Database test failed!")
        sys.exit(1)

    # Try sending email
    try:
        # Get latest cost data
        conn = sqlite3.connect('aws_costs.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT start_date, end_date, total_cost, service_costs 
            FROM cost_data 
            ORDER BY timestamp DESC 
            LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()

        if not row:
            print("No data found in database!")
            sys.exit(1)

        # Create email
        msg = MIMEMultipart()
        msg['Subject'] = f'AWS Cost Report - {row[0]} to {row[1]}'
        msg['From'] = settings["username"]
        msg['To'] = ', '.join(recipients)

        # Create email body
        cost_data = {
            'start_date': row[0],
            'end_date': row[1],
            'total_cost': row[2],
            'service_costs': json.loads(row[3])
        }

        body = f"""
        <html>
        <body>
            <h2>AWS Cost Report</h2>
            <p>Period: {cost_data['start_date']} to {cost_data['end_date']}</p>
            <p>Total Cost: ${cost_data['total_cost']:.2f}</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))

        # Send email
        print("Attempting to send email...")
        with smtplib.SMTP(settings["smtp_server"], settings["smtp_port"]) as server:
            server.starttls()
            server.login(settings["username"], settings["password"])
            server.send_message(msg)
            print("Email sent successfully!")

    except Exception as e:
        print(f"Error sending email: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
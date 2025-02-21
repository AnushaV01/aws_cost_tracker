# AWS Cost Tracker Dashboard

## Overview
AWS Cost Tracker Dashboard is a comprehensive cost monitoring solution designed to help users track AWS usage costs, analyze historical data, and receive automated email notifications. It features a web-based dashboard for interactive cost visualization and supports scheduled cost tracking via cron jobs.

## Features
- **Daily AWS Cost Tracking**: Automatically fetches daily AWS cost usage.
- **AWS Cost Explorer Integration**: Uses AWS Cost Explorer API to retrieve cost and usage data.
- **Email Notifications**: Sends periodic cost summary emails with detailed breakdowns.
- **Interactive Web Dashboard**: Displays cost trends and analysis in a user-friendly interface.
- **Historical Data Storage**: Stores past AWS cost data using SQLite for future reference.
- **Automated Scheduling**: Uses cron jobs to run cost tracking scripts at scheduled intervals.

## Technologies Used
- **Python 3.9+**: Core programming language.
- **Flask**: Web framework for the dashboard.
- **AWS Cost Explorer API**: Fetches cost data.
- **SQLite**: Local database for cost data storage.
- **Tailwind CSS**: Styling for the web dashboard.
- **SMTP (Email)**: Sends notifications via Gmail or another email provider.

## How It Works
### AWS Cost Explorer API
The **AWS Cost Explorer API** is used to fetch cost and usage reports. It provides a way to retrieve granular cost insights based on service usage, time range, and grouping criteria. This project leverages the API to:
- Fetch total AWS spend.
- Break down costs by AWS services (e.g., EC2, S3, Lambda, etc.).
- Retrieve cost data for a specific time range (e.g., daily, monthly).
- Analyze cost trends over time.

## Setup & Installation
### Prerequisites
- An AWS account with Cost Explorer enabled.
- Python 3.9 or later installed.
- AWS credentials (Access Key ID and Secret Access Key).
- A configured email account for notifications.

### Steps to Install and Run
1. **Clone the Repository**
   ```sh
   git clone https://github.com/your-repo/aws-cost-tracker.git
   cd aws-cost-tracker
   ```
2. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```
3. **Configure AWS and Email Settings**
   
   AWS_CONFIG = {
       "aws_access_key_id": "your-access-key",
       "aws_secret_access_key": "your-secret-key",
       "region_name": "your-region"
   }

   EMAIL_CONFIG = {
       "smtp_server": "smtp.gmail.com",
       "smtp_port": 587,
       "username": "your-email@gmail.com",
       "password": "your-app-password"
   }
   ```

4. **Run the AWS Cost Tracker**
   ```sh
   python src/cost_tracker.py
   ```
   This script fetches AWS cost data and stores it in the SQLite database.

5. **Start the Web Dashboard**
   ```sh
   python src/dashboard.py
   ```
   The dashboard will be available at `http://localhost:5000/`.

6. **Schedule Cost Tracking with Cron (Optional)**
   To automate daily cost tracking, add the following cron job:
   ```sh
   crontab -e
   ```
   Add this line to run the script every day at 2:30 AM:
   ```sh
   30 2 * * * /usr/bin/python3 /path-to-project/src/cost_tracker.py
   ```

## Usage
### Fetching AWS Cost Data
The cost tracker script retrieves cost data using the AWS Cost Explorer API. It extracts:
- **Total AWS cost for a specified period**
- **Breakdown of costs by AWS services**
- **Historical cost data for trend analysis**

### Viewing Cost Reports
- Open `http://localhost:8080/` in your browser.
- The dashboard will display:
  - **Total cost overview**
  - **Breakdown by service**
  - **Historical trends**

### Email Notifications
- The script will send email notifications with a cost summary whenever it runs successfully.
- Email format includes:
  - **Total AWS cost**
  - **Breakdown of costs per service**
  - **Comparison with previous periods**

## Security Considerations
- Never hardcode AWS credentials in your code. Use environment variables or AWS IAM roles when possible.
- Use an **App Password** instead of your real email password for SMTP authentication.
- Regularly rotate AWS credentials to maintain security.

## Troubleshooting
### Common Issues
- **AWS API Access Denied**: Ensure your AWS IAM user has `ce:GetCostAndUsage` permission.
- **Emails Not Sending**: Verify SMTP credentials and check email provider restrictions.
- **Dashboard Not Loading**: Make sure Flask is running and no firewall is blocking the port.

## Future Improvements
- Support for additional cost visualization options.
- Multi-user authentication for shared dashboard access.
- Advanced cost prediction using machine learning.
- Support for multiple cloud providers (Azure, GCP).


## License
This project is licensed under the MIT License.

## Contributions
Contributions are welcome! Feel free to submit pull requests or raise issues.

---
#**Developed with ❤️ for AWS cost tracking enthusiasts.**(Took AI tools assistance to generate and refine certain code segments.)


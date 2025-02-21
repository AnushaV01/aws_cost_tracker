import boto3
import json
from datetime import datetime, timedelta
import sqlite3
from typing import Dict, Any

class AWSCostTracker:
    def __init__(self, db_path: str = 'aws_costs.db'):
        self.ce_client = boto3.client('ce',
            aws_access_key_id=AWS_CONFIG['aws_access_key_id'],
            aws_secret_access_key=AWS_CONFIG['aws_secret_access_key'],
            region_name=AWS_CONFIG['region_name']
        )
        self.db_path = db_path
        self.setup_database()

    def setup_database(self) -> None:
        """Initialize SQLite database and create necessary tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS cost_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_date TEXT,
            end_date TEXT,
            total_cost REAL,
            service_costs TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()

    def get_costs(self, days: int = 30) -> Dict[str, Any]:
        """Fetch AWS costs for the specified time period."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        response = self.ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'}
            ]
        )
        
        return self._process_cost_data(response)

    def _process_cost_data(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Process and structure the cost data."""
        total_cost = 0
        service_costs = {}
        
        for result in response['ResultsByTime']:
            for group in result['Groups']:
                service = group['Keys'][0]
                cost = float(group['Metrics']['UnblendedCost']['Amount'])
                service_costs[service] = cost
                total_cost += cost
        
        return {
            'total_cost': total_cost,
            'service_costs': service_costs,
            'start_date': response['ResultsByTime'][0]['TimePeriod']['Start'],
            'end_date': response['ResultsByTime'][-1]['TimePeriod']['End']
        }

    def save_to_database(self, cost_data: Dict[str, Any]) -> None:
        """Save the cost data to SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO cost_data (start_date, end_date, total_cost, service_costs)
        VALUES (?, ?, ?, ?)
        ''', (
            cost_data['start_date'],
            cost_data['end_date'],
            cost_data['total_cost'],
            json.dumps(cost_data['service_costs'])
        ))
        
        conn.commit()
        conn.close()

def main():
    try:
        print("Starting AWS Cost Tracker...")
        tracker = AWSCostTracker()
        print("Fetching cost data...")
        cost_data = tracker.get_costs()
        print("Saving to database...")
        tracker.save_to_database(cost_data)
        
        print("\nAWS Cost Summary:")
        print(f"Period: {cost_data['start_date']} to {cost_data['end_date']}")
        print(f"Total Cost: ${cost_data['total_cost']:.2f}")
        print("\nCost by Service:")
        for service, cost in cost_data['service_costs'].items():
            print(f"{service}: ${cost:.2f}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()

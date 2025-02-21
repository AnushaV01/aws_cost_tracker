from flask import Flask, render_template
import sqlite3
import json

app = Flask(__name__)

# Add custom filter to handle JSON strings
@app.template_filter('from_json')
def from_json(value):
    return json.loads(value)

@app.route('/')
def dashboard():
    conn = sqlite3.connect('aws_costs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cost_data ORDER BY timestamp DESC")
    data = cursor.fetchall()
    conn.close()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
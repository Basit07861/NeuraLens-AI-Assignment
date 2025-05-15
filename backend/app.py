from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Loading the demo products CSV with full product details
PRODUCTS_CSV = 'demo_data.csv'
df = pd.read_csv(PRODUCTS_CSV)

# Ensuring price column is treated as numeric
df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)

@app.route('/api/products', methods=['GET'])
def get_products():
    # Replace NaN with None to ensure valid JSON
    clean_df = df.where(pd.notnull(df), None)
    return jsonify(clean_df.to_dict(orient='records'))

@app.route('/api/products/filter', methods=['POST'])
def filter_products():
    data = request.get_json()
    min_price = float(data.get('min_price', 0))
    max_price = float(data.get('max_price', float('inf')))

    filtered = df[(df['price'] >= min_price) & (df['price'] <= max_price)]
    clean_filtered = filtered.where(pd.notnull(filtered), None)
    return jsonify(clean_filtered.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)


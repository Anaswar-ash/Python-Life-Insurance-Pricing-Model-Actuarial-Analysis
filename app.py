from flask import Flask, request, jsonify, render_template
from calculator_logic import PremiumCalculator # Import our class

# Initialize the Flask application
app = Flask(__name__)

# --- Pre-load the mortality data to be efficient ---
# This avoids reloading the Excel file on every single request.
EXCEL_FILE = 'research-2017-cso-unloaded.xlsx'
try:
    MALE_CALCULATOR = PremiumCalculator(EXCEL_FILE, '2017 Male Composite ANB')
    FEMALE_CALCULATOR = PremiumCalculator(EXCEL_FILE, '2017 Female Composite ANB')
    print("Mortality data pre-loaded successfully.")
except Exception as e:
    print(f"Could not start the server. Failed to load data: {e}")
    # In a real application, you might handle this more gracefully.
    exit()

# --- Define the routes (the URLs for our app) ---

@app.route('/')
def home():
    """This function serves the main HTML page."""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """This is the API endpoint that performs the calculation."""
    try:
        data = request.get_json()
        
        # Get data from the webpage's request
        age = int(data['age'])
        gender = data['gender']
        benefit = float(data['benefit'])
        rate = float(data['rate'])

        # Select the correct pre-loaded calculator
        if gender == 'Male':
            calculator = MALE_CALCULATOR
        else:
            calculator = FEMALE_CALCULATOR

        # --- Perform Calculations ---
        if age not in calculator.mortality_data['age'].values:
            return jsonify({'error': f"Age {age} not found in the mortality table."}), 400

        nsp = calculator.calculate_nsp(age, benefit, rate)
        annuity = calculator.calculate_annuity_due(age, rate)
        
        if annuity == 0:
            annual_premium = 0
        else:
            annual_premium = nsp / annuity

        # Send the results back to the webpage as JSON
        return jsonify({
            'nsp': f"${nsp:,.2f}",
            'annuity': f"{annuity:.4f}",
            'annual_premium': f"${annual_premium:,.2f}"
        })

    except Exception as e:
        # Handle potential errors gracefully
        return jsonify({'error': str(e)}), 400

# --- Run the application ---
if __name__ == '__main__':
    # Setting debug=True is useful for development
    app.run(debug=True)

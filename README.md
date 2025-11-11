# Life Insurance Premium Calculator

This project is a web-based application that calculates life insurance premiums using actuarial principles. It uses the 2017 Commissioners Standard Ordinary (CSO) mortality table to determine the probability of death at each age and calculates the net single premium and annual premium for a given whole life insurance policy.

## Features

-   **Actuarial Calculations:** Implements core actuarial formulas for Net Single Premium (NSP) and Life Annuity Due.
-   **Web Interface:** A simple and clean user interface built with Flask and HTML/JavaScript to input policy details and view results.
-   **CSO Mortality Data:** Uses the official 2017 CSO mortality table, which is the standard for life insurance in the United States.
-   **Gender-Specific Rates:** Loads and uses separate mortality tables for males and females.
-   **Efficient Data Loading:** Pre-loads the mortality data when the application starts to ensure fast calculation times.

## How It Works

The application is based on the following actuarial concepts:

1.  **Mortality Table (`qx`):** The probability that a person of a certain age will die within one year. This data is loaded from the `research-2017-cso-unloaded.xlsx` file.
2.  **Net Single Premium (NSP):** The present value of the future death benefit. It's the lump-sum amount someone would need to pay today to be fully insured.
3.  **Life Annuity Due:** The present value of a series of payments of $1 made at the beginning of each year for as long as the insured person is alive.
4.  **Annual Premium:** The level premium paid at the beginning of each year. It is calculated by dividing the NSP by the Life Annuity Due.

## Technologies & Libraries

-   **Backend:** Python, Flask
-   **Data Manipulation:** Pandas
-   **Excel Parsing:** openpyxl
-   **Frontend:** HTML, JavaScript (for API calls)

## Project Structure

```
Python-Life-Insurance-Pricing-Model-Actuarial-Analysis/
│
├── app.py                      # Main Flask application and API endpoint
├── calculator_logic.py         # Contains the PremiumCalculator class and actuarial formulas
├── research-2017-cso-unloaded.xlsx # The mortality data file
├── templates/
│   └── index.html              # The HTML for the user interface
├── requirements.txt            # (To be created) List of Python dependencies
└── README.md                   # This file
```

## Getting Started

### Prerequisites

-   Python 3.x

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Anaswar-ash/Python-Life-Insurance-Pricing-Model-Actuarial-Analysis.git
    cd Python-Life-Insurance-Pricing-Model-Actuarial-Analysis
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    A `requirements.txt` file is not provided, but you can install the dependencies directly:
    ```bash
    pip install Flask pandas openpyxl
    ```

### Usage

1.  **Run the Flask application:**
    ```bash
    flask run
    ```
    You should see output indicating that the server is running on `http://127.0.0.1:5000`.

2.  **Open the application in your browser:**
    Navigate to `http://127.0.0.1:5000` in your web browser.

3.  **Enter the policy details:**
    -   **Age:** The current age of the insured.
    -   **Gender:** Male or Female.
    -   **Death Benefit:** The amount to be paid out.
    -   **Interest Rate:** The assumed annual interest rate (e.g., 0.05 for 5%).

4.  **Calculate:**
    Click the "Calculate" button to see the Net Single Premium, Life Annuity Due, and the calculated Annual Premium.
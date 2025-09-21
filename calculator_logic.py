import pandas as pd
import sys

class PremiumCalculator:
    """
    A class to calculate life insurance premiums based on mortality data.
    It loads and prepares data from a specific sheet in an Excel file.
    """
    def __init__(self, excel_file, sheet_name):
        """
        Initializes the calculator by loading and processing the mortality data.
        """
        self.mortality_data = None
        self._load_data(excel_file, sheet_name)

    def _load_data(self, excel_file, sheet_name):
        """Loads and prepares mortality data from the specified Excel file and sheet."""
        try:
            raw_data = pd.read_excel(excel_file, sheet_name=sheet_name, skiprows=2)
            
            self.mortality_data = raw_data[['Att. Age', 'Ult.']].rename(
                columns={'Att. Age': 'age', 'Ult.': 'qx_per_1000'}
            )

            self.mortality_data['qx'] = self.mortality_data['qx_per_1000'] / 1000
            self.mortality_data['px'] = 1 - self.mortality_data['qx']
            self.mortality_data = self.mortality_data[['age', 'qx', 'px']].copy()
            print(f"Successfully loaded mortality data from sheet: {sheet_name}")

        except FileNotFoundError:
            raise Exception(f"FATAL ERROR: The file '{excel_file}' was not found.")
        except ValueError:
            raise Exception(f"FATAL ERROR: The sheet named '{sheet_name}' was not found in the Excel file.")
        except KeyError:
            raise Exception("FATAL ERROR: Could not find required columns 'Att. Age' or 'Ult.' in the sheet.")

    def calculate_t_px(self, age, t):
        """Calculates the cumulative survival probability (t_px)."""
        if age + t > self.mortality_data['age'].max():
            return 0
        px_series = self.mortality_data.loc[self.mortality_data['age'].between(age, age + t - 1), 'px']
        return px_series.prod()

    def calculate_nsp(self, age, death_benefit, interest_rate):
        """Calculates the Net Single Premium (NSP)."""
        v = 1 / (1 + interest_rate)
        total_pv = 0
        for t in range(0, 121 - age):
            t_px = self.calculate_t_px(age, t)
            qx_t_series = self.mortality_data.loc[self.mortality_data['age'] == age + t, 'qx']
            if qx_t_series.empty:
                continue
            qx_t = qx_t_series.iloc[0]
            
            pv_benefit = death_benefit * (v ** (t + 1))
            prob_dying = t_px * qx_t
            total_pv += pv_benefit * prob_dying
            
        return total_pv

    def calculate_annuity_due(self, age, interest_rate):
        """Calculates the value of a life annuity due."""
        v = 1 / (1 + interest_rate)
        total_pv_annuity = 0
        for t in range(0, 121 - age):
            t_px = self.calculate_t_px(age, t)
            total_pv_annuity += (v ** t) * t_px
        return total_pv_annuity

from flask import Flask, render_template, request

app = Flask(__name__)

# Constants
AVERAGE_SUNLIGHT_HOURS = {
    "north": 4,  # Northern regions
    "south": 6,  # Southern regions
    "equator": 7  # Equatorial regions
}
DAYS_IN_MONTH = 30
COST_PER_PANEL = 300  # USD per panel
COST_PER_BATTERY = 200  # USD per battery

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Panels calculation route
@app.route('/panels', methods=['GET', 'POST'])
def panels():
    if request.method == 'POST':
        try:
            # Get user inputs
            monthly_usage = float(request.form['monthly_usage'])  # in kWh
            panel_wattage = float(request.form['panel_wattage'])  # in watts
            location = request.form['location']  # north, south, equator

            # Calculate daily energy consumption
            daily_usage = monthly_usage / DAYS_IN_MONTH  # kWh per day

            # Get sunlight hours based on location
            sunlight_hours = AVERAGE_SUNLIGHT_HOURS.get(location, 5)

            # Calculate energy produced by one panel per day
            panel_daily_output = (panel_wattage * sunlight_hours) / 1000  # kWh per day

            # Calculate number of panels required
            panels_required = daily_usage / panel_daily_output

            # Round up to the nearest whole number
            panels_required = int(panels_required) + 1 if panels_required % 1 != 0 else int(panels_required)

            # Return result to the user
            return render_template('result.html', result_type="panels", result_value=panels_required)
        except Exception as e:
            return f"An error occurred: {str(e)}"
    return render_template('panels.html')

# Batteries calculation route
@app.route('/batteries', methods=['GET', 'POST'])
def batteries():
    if request.method == 'POST':
        try:
            # Get user inputs
            daily_usage = float(request.form['daily_usage'])  # in kWh
            battery_capacity = float(request.form['battery_capacity'])  # in kWh
            depth_of_discharge = float(request.form['depth_of_discharge'])  # in percentage

            # Calculate usable battery capacity
            usable_capacity = battery_capacity * (depth_of_discharge / 100)

            # Calculate number of batteries required
            batteries_required = daily_usage / usable_capacity

            # Round up to the nearest whole number
            batteries_required = int(batteries_required) + 1 if batteries_required % 1 != 0 else int(batteries_required)

            # Return result to the user
            return render_template('result.html', result_type="batteries", result_value=batteries_required)
        except Exception as e:
            return f"An error occurred: {str(e)}"
    return render_template('batteries.html')

# Cost calculation route
@app.route('/cost', methods=['GET', 'POST'])
def cost():
    if request.method == 'POST':
        try:
            # Get user inputs
            panels_required = int(request.form['panels_required'])
            batteries_required = int(request.form['batteries_required'])

            # Calculate total cost
            total_cost = (panels_required * COST_PER_PANEL) + (batteries_required * COST_PER_BATTERY)

            # Return result to the user
            return render_template('result.html', result_type="total cost", result_value=f"${total_cost:,.2f}")
        except Exception as e:
            return f"An error occurred: {str(e)}"
    return render_template('cost.html')

if __name__ == '__main__':
    app.run(debug=True)

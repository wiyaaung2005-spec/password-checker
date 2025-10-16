from flask import Flask, render_template, request

# Initialize the Flask application
app = Flask(__name__)

# --- Password Scoring Logic ---
# This function calculates the strength based on various criteria
def check_password_strength(password):
    score = 0
    feedback = []

    # 1. Length Check: The most important factor
    if len(password) >= 12:
        score += 3
        feedback.append("Excellent length (12+ characters)")
    elif len(password) >= 8:
        score += 2
        feedback.append("Good length (8+ characters)")
    else:
        feedback.append("Password is too short (less than 8 characters)")

    # 2. Character Variety Checks:
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)

    if has_upper:
        score += 1
        feedback.append("Includes uppercase letters")
    if has_lower:
        score += 1
    if has_digit:
        score += 1
        feedback.append("Includes numbers")
    if has_symbol:
        score += 2
        feedback.append("Includes special symbols")

    # Final Score Mapping
    if score >= 8:
        return "Strong", "green", feedback
    elif score >= 5:
        return "Medium", "orange", feedback
    else:
        return "Weak", "red", feedback

# --- Flask Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the password from the HTML form
        user_password = request.form['password']

        # Get the results from our strength checker function
        strength, color, feedback = check_password_strength(user_password)

        # Render the template and send the results back to be displayed
        return render_template('index.html', 
                               strength=strength, 
                               color=color, 
                               feedback=feedback)
    
    # Render the initial page with no results
    return render_template('index.html', strength=None, color=None, feedback=None)


if __name__ == '__main__':
    # Flask runs locally on port 5000 (standard for development)
    app.run(debug=True)
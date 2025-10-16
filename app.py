from flask import Flask, render_template, request

# Initialize the Flask application
app = Flask(__name__)

# --- Password Scoring Logic ---
# This function calculates the strength based on various criteria
# --- Password Scoring Logic (Updated) ---
def check_password_strength(password):
    score = 0
    feedback = []
    suggestions = [] # New list to hold suggestions

    # 1. Length Check
    if len(password) >= 12:
        score += 3
        feedback.append("Excellent length (12+ characters)")
    elif len(password) >= 8:
        score += 2
        feedback.append("Good length (8+ characters)")
    else:
        feedback.append("Password is too short (less than 8 characters)")
        suggestions.append("⚠️ Increase length to 12 or more characters.")


    # 2. Character Variety Checks
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)

    if has_upper:
        score += 1
        feedback.append("Includes uppercase letters")
    else:
        suggestions.append("✅ Add uppercase letters (A, B, C).")
        
    if has_lower:
        score += 1
        feedback.append("Includes lowercase letters")
        
    if has_digit:
        score += 1
        feedback.append("Includes numbers")
    else:
        suggestions.append("🔢 Include numbers (1, 2, 3).")
        
    if has_symbol:
        score += 2
        feedback.append("Includes special symbols")
    else:
        suggestions.append("⚡ Integrate special symbols (@, #, !, $).")

    # Final Score Mapping
    if score >= 8:
        # If strong, clear suggestions as none are needed
        return "Strong", "green", feedback, []
    elif score >= 5:
        # Medium: return the calculated suggestions
        return "Medium", "orange", feedback, suggestions
    else:
        # Weak: return the calculated suggestions
        return "Weak", "red", feedback, suggestions

# --- Flask Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_password = request.form['password']
        
        # NOTE: We now unpack a fourth variable: suggestions
        strength, color, feedback, suggestions = check_password_strength(user_password)

        # Render the template and send the new variables
        return render_template('index.html', 
                               strength=strength, 
                               color=color, 
                               feedback=feedback,
                               suggestions=suggestions) # Passed to HTML!
    
    # Render the initial page with empty variables
    return render_template('index.html', strength=None, color=None, feedback=None, suggestions=None)


if __name__ == '__main__':
    # Flask runs locally on port 5000 (standard for development)
    app.run(debug=True)
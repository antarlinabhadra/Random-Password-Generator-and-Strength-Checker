from flask import Flask, render_template, request, jsonify
import pyperclip
import random
import string

app = Flask(__name__)

# Function to check password strength
def check_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)

    score = sum([has_upper, has_lower, has_digit, has_special])

    if length < 8:
        return "Very Weak", "red", 20
    elif length < 10:
        return "Weak", "orange", 40
    elif length >= 20 and score == 4:
        return "Strong", "green", 100
    else:
        return "Moderate", "blue", 60

# Route for home page
@app.route('/')
def home():
    return render_template("frontend.html")

#Route for About Us page
@app.route('/about')
def about():
    return render_template("about.html")

#Route for Contact Us page
@app.route('/contact')
def contact():
    return render_template("contact.html")

# Route for checking password strength
@app.route('/check_strength', methods=["POST"])
def check_password_strength():
    data = request.get_json()
    password = data.get('password', '')
    strength, color, width = check_strength(password)
    return jsonify({'strength': strength, 'color': color, 'width': width})

# Route for generating strong password
@app.route('/generate_password', methods=["POST"])
def generate_password():
    data = request.get_json()
    length = int(data.get('length', 12))
    use_upper = data.get('uppercase', True)
    use_lower = data.get('lowercase', True)
    use_digits = data.get('numbers', True)
    use_symbols = data.get('symbols', True)
    
    chars = ''
    if use_upper:
        chars += string.ascii_uppercase
    if use_lower:
        chars += string.ascii_lowercase
    if use_digits:
        chars += string.digits
    if use_symbols:
        chars += string.punctuation
    if not chars:
        return jsonify({'error': 'At least one character type must be selected.'}), 400
    
    password = ''.join(random.choice(chars) for _ in range(length))
    strength, color, width = check_strength(password)
    return jsonify({'password': password, 'strength': strength, 'color': color, 'width': width})

#Route for analyzing the composition of the passwor
@app.route('/analyze_password', methods=['POST'])
def analyze_password():
    data = request.get_json()
    password = data.get('password', '')

    uppercase = sum(1 for c in password if c.isupper())
    lowercase = sum(1 for c in password if c.islower())
    digits = sum(1 for c in password if c.isdigit())
    special = sum(1 for c in password if c in string.punctuation)

    return jsonify({
        'uppercase': uppercase,
        'lowercase': lowercase,
        'digits': digits,
        'special': special
    })
    

@app.route('/copy_password', methods=['POST'])
def copy_password():
    data = request.get_json()
    password = data.get('password', '')
    
    if password:
        pyperclip.copy(password)
        return jsonify({'status': 'success', 'message': 'Password copied to clipboard!'})
    else:
        return jsonify({'status': 'error', 'message': 'No password to copy!'})
    

if __name__ == '_main_':
    app.run(debug=True)
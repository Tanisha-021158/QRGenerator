from flask import Flask, render_template, request
import qrcode
from io import BytesIO
from base64 import b64encode

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Render the home page

@app.route('/', methods=['POST'])
def generateQR():
    memory = BytesIO()  # Create a BytesIO stream
    data = request.form.get('link')  # Get the user input from the form
    if not data:  # Check if input is empty
        return render_template('index.html', error="Please enter a valid link or text.")

    try:
        img = qrcode.make(data)  # Generate the QR code
        img.save(memory)  # Save the QR code image to the BytesIO stream
        memory.seek(0)  # Reset stream position to the beginning

        # Convert the image to a Base64 string
        base64_img = "data:image/png;base64," + b64encode(memory.getvalue()).decode('ascii')
        return render_template('index.html', data=base64_img)
    except Exception as e:
        return render_template('index.html', error="An error occurred: " + str(e))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, render_template_string
import openai
from googletrans import Translator

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key
openai.api_key = "YOUR API KEY"
# Initialize translator
translator = Translator()

# Function to generate product descriptions using GPT-4
def generate_product_description(product_name, keywords, language="en"):
    prompt = f"Write a detailed and engaging product description for {product_name}. Keywords: {keywords}."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates product descriptions."},
            {"role": "user", "content": prompt}
        ]
    )
    
    description = response['choices'][0]['message']['content']
    
    # Translate if needed
    if language != "en":
        description = translator.translate(description, dest=language).text
    
    return description

# HTML template for the user interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Product Description Generator</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 600px; margin: auto; }
        input, textarea, button { width: 100%; padding: 10px; margin: 10px 0; }
        .output { background: #f4f4f4; padding: 10px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Product Description Generator</h1>
        <form id="descriptionForm">
            <input type="text" id="productName" placeholder="Product Name" required>
            <textarea id="keywords" placeholder="Keywords (comma-separated)" required></textarea>
            <select id="language">
                <option value="en">English</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
                <option value="de">German</option>
                <option value="zh-cn">Chinese</option>
            </select>
            <button type="submit">Generate Description</button>
        </form>
        <div class="output" id="output"></div>
    </div>

    <script>
        document.getElementById("descriptionForm").addEventListener("submit", async (e) => {
            e.preventDefault();
            
            const productName = document.getElementById("productName").value;
            const keywords = document.getElementById("keywords").value;
            const language = document.getElementById("language").value;
            
            const response = await fetch("/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ product_name: productName, keywords: keywords, language: language })
            });
            
            const data = await response.json();
            document.getElementById("output").innerText = data.description;
        });
    </script>
</body>
</html>
"""

# Home page with form
@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

# API endpoint to generate descriptions
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    product_name = data.get("product_name")
    keywords = data.get("keywords")
    language = data.get("language", "en")
    
    description = generate_product_description(product_name, keywords, language)
    
    return {"description": description}

# Run the app
if __name__ == "__main__":
    app.run(debug=True)

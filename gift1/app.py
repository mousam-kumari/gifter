from flask import Flask, request, jsonify,render_template
import google.generativeai as genai
import re
app = Flask(__name__)
# Your Gemini API key
GEMINI_API_KEY = 'AIzaSyCclRMJ0cdftV0xAhHS7yPEyMWbc3TZtPs'

products_schema = [
    {
        "Product_name": "Eco-friendly Water Bottle",
        "Reason": "Chosen for its environmental benefits and the growing consumer preference for sustainable products."
    },
]

# Initialize the Gemini API client
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.0-pro')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_gift_idea', methods=['POST'])
def generate_gift_idea():
    data = request.json
    age = data.get('age')
    gender = data.get('gender')
    occasion = data.get('occasion')
    recipient_type = data.get('recipient_type')
    categories = data.get('categories')
    price_range = data.get('price_range')
    
    # Convert categories list to a string for the prompt
    categories_str = ', '.join(categories)
    
    prompt = (f"You have a very good choice, so just provide me a list of 9 highly-rated and trending different gift ideas with a specific product, for indian people "
              f"for a {age}-year-old {recipient_type} who is {gender} and loves {categories_str} items. These gifts should be suitable for {occasion}, "
              f"available on Amazon India, and within the price range {price_range}. Ensure that each product followed by only its product_names,"
              f"of each product, each product followed by a convincing reason for its selection for Indian people in brief and ensure that product are listed without any "
              f"special characters such as *, -, here {products_schema} is an example with three products with its Product_name:,Reason_for_selection :, "
              f"similarly do that for all 9 product.GEnerate 9 products with product and reason for selection as gift idea and reason should be just below the product name follow {products_schema}")

    try:
        response = model.generate_content(prompt)
        generated_text = response.text
        cleaned_text = clean_text(generated_text)
        gift_ideas = process_text_for_gift_ideas(cleaned_text)[:12]
        return jsonify({"gift_ideas": gift_ideas})
    except Exception as e:
        print(f"Error generating gift ideas: {e}")
        return jsonify({"error": "Error generating gift ideas"}), 500

@app.route('/search_gift_idea', methods=['POST'])
def search_gift_idea():
    data = request.json
    textdata = data.get('prompt')
    prompt = (f"Task: Gift idea generation\nDescription: Based on {textdata} generate gift idea suggestions that are available on Amazon India ecommerce website. "
              f"Ensure that only the product namee and reason is provided as example in schema {products_schema}. Additionally, include each product "
              f"followed by its description and a convincing reason for its selection for Indian people. Provide me the output in the format: Product:\n Reason:")

    try:
        response = model.generate_content(prompt)
        generated_text = response.text
        cleaned_text = clean_text(generated_text)
        gift_ideas = process_text_for_gift_ideas(cleaned_text)[:12]
        return jsonify({"gift_ideas": gift_ideas})
    except Exception as e:
        print(f"Error generating gift ideas: {e}")
        return jsonify({"error": "Error generating gift ideas"}), 500
def clean_text(text):
    return re.sub(r'[*-]', '', text)
def process_text_for_gift_ideas(text):
    return text.split('\n')[:12]

if __name__ == '__main__':
    app.run(debug=True)

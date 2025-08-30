import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Configure the Gemini API
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    print(f"Error configuring Generative AI: {e}")
    model = None

def generate_recommendation_prompt(data: dict) -> str:
    """Creates a detailed prompt for the AI model."""
    prompt = f"""
    Act as an expert agronomist specializing in soil regeneration for Indian soil conditions. Based on the following soil data, provide a set of actionable, personalized recommendations to improve soil health.

    **Soil Data:**
    - **Location/Climate:** {data.get('location', 'Not specified')} (Provide context relevant to this Indian location)
    - **pH Level:** {data['ph_level']}
    - **Organic Matter Percentage:** {data['organic_matter']}%
    - **Moisture Content:** {data['moisture_content']}%
    - **Previous Crop History:** {data.get('previous_crop', 'Not specified')}

    **Instructions:**
    1.  **Analysis:** Briefly analyze the provided soil data.
    2.  **Core Recommendations:** Suggest 3-5 key practices. For each, explain why it is suitable for these specific conditions. Examples include:
        - Specific cover crops to plant (e.g., 'Dhaincha or Sunn Hemp to fix nitrogen').
        - Composting strategies (e.g., 'apply 5 tons/hectare of vermicompost').
        - No-till or minimum tillage advice.
        - Suitable microbial inoculants like Azotobacter or PSB.
    3.  **Formatting:** Use Markdown for clarity (e.g., headings, bullet points).

    Begin your response now.
    """
    return prompt

def get_ai_recommendation(soil_data: dict) -> str:
    """Gets a recommendation from the configured generative AI model."""
    if model is None:
        return "AI Model not configured. Please check your API key in the .env file."

    try:
        prompt = generate_recommendation_prompt(soil_data)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Generative AI API: {e}")
        return f"Sorry, an error occurred while generating the recommendation: {e}"
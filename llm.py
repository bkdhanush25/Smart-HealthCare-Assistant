from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize the LLM with Groq model
groq_llm = ChatGroq(
    model_name="llama3-70b-8192",
    api_key=groq_api_key
)

# Prompt template for extracting ingredient quantities
ingredient_quantity_prompt = PromptTemplate(
    input_variables=["dish_name"],
    template="""
You are a nutrition assistant. Given a dish name, return:

1. A comma-separated list of common ingredients with typical cooking measurements for 3–4 servings(if quantity is not specified).
2. A dictionary mapping each ingredient to an estimated weight in grams (g).

Example Input: "Paneer Butter Masala"

Example Output:
Ingredients: 200g paneer, 2 tomatoes, 1 onion, 1 tbsp butter, 1 tsp garam masala
Quantities (in grams): {{
  "paneer": 200,
  "tomatoes": 150,
  "onion": 100,
  "butter": 14,
  "garam masala": 5
}}

DO NOT include any explanations or preamble. ONLY return the JSON output.
(Calculate the quantity precisely that the ingredients quantity should not exceed the final dish quantity)

Now answer for this dish:
{dish_name}
"""
)

# Prompt template for classifying dish type
dish_type_prompt = PromptTemplate(
    input_variables=["dish_name"],
    template="""
Classify the following Indian dish into one of these categories:
Wet Sabzi, Dry Sabzi, Dal, Non-Veg Curry, Egg Dish, Chicken Dish, Mutton Dish,
Fish Dish, Rice Dish, Pulao/Biryani, Roti/Paratha, Chutney, Pickle, Snack, Sweet,
Dessert, Beverage, Salad, Soup, Breakfast Item, Street Food, South Indian Dish,
North Indian Dish, Other.

Dish: {dish_name}
Category:
"""
)

# Chain for classifying dish type
dish_type_chain = LLMChain(llm=groq_llm, prompt=dish_type_prompt)

# Function to extract dish type
def extract_dish_type(dish_name):
    try:
        result = dish_type_chain.invoke({"dish_name": dish_name})
        if isinstance(result, dict) and 'text' in result:
            return result['text'].replace('Category: ', '').strip()
        return "Unknown"
    except Exception as e:
        return "Unknown"  # Return "Unknown" if an error occurs

# Chain for extracting ingredient quantities
ingredient_extraction_chain = LLMChain(llm=groq_llm, prompt=ingredient_quantity_prompt)

# Function to extract ingredients and their quantities from the dish
def extract_ingredients_from_dish(dish_name):
    try:
        response = ingredient_extraction_chain.run(dish_name=dish_name)

        # Initialize the ingredient list and quantities dictionary
        ingredients = []
        quantities_in_grams = {}

        # Process the LLM response
        if "Ingredients:" in response and "Quantities (in grams):" in response:
            parts = response.split("Quantities (in grams):")
            ingredients_text = parts[0].replace("Ingredients:", "").strip()
            ingredients = [item.strip() for item in ingredients_text.split(",")]

            import ast
            grams_dict_str = parts[1].strip()
            try:
                quantities_in_grams = ast.literal_eval(grams_dict_str)
            except Exception:
                pass

        return ingredients, quantities_in_grams
    except Exception:
        return [], {}  # Return empty lists/dictionaries in case of failure

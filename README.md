# 🍎 Smart Healthcare Assistant - Nutrient Lookup

This Streamlit-based web application helps users estimate nutritional information of Indian dishes by extracting ingredients and their quantities using a large language model (LLM), then querying a vector database for nutrient details.

## 🚀 Features

- **Dish Type Classification**: Automatically classify Indian dishes (e.g., Dal, Sabzi, Snack, Sweet, etc.)
- **LLM-based Ingredient Extraction**: Uses Groq's LLaMA-3 model to extract common ingredients and estimate their quantities in grams.
- **Vector Search with ChromaDB**: Finds nutritional values of ingredients using vector similarity search.
- **Interactive UI**: Built using Streamlit for ease of use.
- **Nutrient Summary**: View total calories, protein, fat, and carbs for your dish.

## 🧠 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **LLM**: Groq's `llama3-70b-8192` via LangChain
- **Vector Database**: ChromaDB (with `sentence-transformers`)
- **Environment Variables**: `.env` for Groq API key

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/health-nutrition-assistant.git
cd health-nutrition-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your `.env` file

Create a `.env` file in the root directory with your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Add `ingredients.csv`

Place the `ingredients.csv` file in the project root. The CSV must include columns like `food_name`, `energy_kcal`, `carb_g`, `protein_g`, `fat_g`, `fibre_g`.

### 5. Run the app

```bash
streamlit run main.py
```

## 🧪 Folder Structure

```
.
├── main.py                # Streamlit app
├── vectordb.py           # Vector search and DB initialization logic
├── llm.py                # LLM prompt and ingredient extraction logic
├── ingredients.csv       # Ingredient nutrient data
├── .env                  # API keys
└── requirements.txt      # Python dependencies
```

## 5 Input/Output Examples

### Example:1
```
Dish: Paneer Butter Masala
```

- Dish Type: Veg Curry
- Ingredients: 200g paneer, 2 tomatoes, 1 onion, 1 tbsp butter, 1 tsp garam masala
- Total Nutrients: Calories: 739.67 kcal, Protein: 42.28 g, Fat: 41.91 g, Carbs: 47.76 g


### Example: 2
```
Dish: 3kg of Chicken Biryani
```

- Dish Type: Pulao/Biryani  
- Ingredients: 1.5kg basmati rice, 1.2kg chicken, 2 cups water, 2 tbsp ghee, 1 tsp cumin seeds, 1 tsp coriander seeds, 1 tsp fennel seeds, 1 tsp cardamom powder, 1 tsp cinnamon powder, 1 tsp turmeric powder, 1 tsp red chili powder, Salt to taste  
- Total Nutrients: Calories: 7232.25 kcal, Protein: 304.91 g, Fat: 165.24 g, Carbs: 1218.39 g

### Example: 3
```
Dish: Masala Dosa
```

- Dish Type: South Indian Dish  
- Ingredients: 1 cup dosa batter, 1/4 cup potato, 1/4 cup onion, 1/4 cup peas, 1 tsp cumin seeds, 1 tsp mustard seeds, 1/4 tsp turmeric, 1/4 tsp red chili powder, 1 tbsp butter, salt to taste  
- Total Nutrients: Calories: 1033.99 kcal, Protein: 31.6 g, Fat: 30.52 g, Carbs: 154.8 g

### Example: 4
```
Dish: 3 bowls of Gulab Jamun
```

- Dish Type: Sweet, Dessert  
- Ingredients: 300g milk powder, 150g all-purpose flour, 1/4 tsp baking soda, 1/4 tsp salt, 1/4 cup ghee, 1 cup lukewarm milk, 1 tsp rose water, 1 tsp cardamom powder, sugar syrup (for serving)  
- Total Nutrients: Calories: 2731.47 kcal, Protein: 83.13 g, Fat: 141.03 g, Carbs: 283.15 g

### Example: 4  
```
Dish: 1kg of Vegetable Pulao
```

- Dish Type: Pulao/Biryani  
- Ingredients: 250g basmati rice, 500g mixed vegetables, 1 tbsp ghee, 1 tsp cumin seeds, 1 tsp fennel seeds, salt to taste  
- Total Nutrients: Calories: 1939.19 kcal, Protein: 54.0 g, Fat: 28.67 g, Carbs: 378.98 g

## 📘 Notes

- LLM estimates quantities based on common cooking proportions.
- ChromaDB initializes on first run and persists data.

## 👨‍💻 Author

Made with ❤️ by Dhanush BK.



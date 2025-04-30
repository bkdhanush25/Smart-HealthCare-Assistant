import chromadb
import pandas as pd
from sentence_transformers import SentenceTransformer
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Initialize persistent ChromaDB client
client = chromadb.PersistentClient("vectorstore")
collection = client.get_or_create_collection("ingredients")

# Lazy-loaded sentence transformer model
model = None

def get_model():
    global model
    if model is None:
        logging.info("Loading sentence transformer model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

# Load ingredients from CSV with validation
def load_ingredients_from_csv(file_path="ingredients.csv"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found at {file_path}")

    df = pd.read_csv(file_path)
    ingredients = []
    for _, row in df.iterrows():
        if not pd.notna(row.get('food_name')):
            continue

        nutrient_details = {
            "energy_kcal": row.get('energy_kcal', 0),
            "carb_g": row.get('carb_g', 0),
            "protein_g": row.get('protein_g', 0),
            "fat_g": row.get('fat_g', 0),
            "fibre_g": row.get('fibre_g', 0),
        }
        ingredients.append({
            'ingredient_name': row['food_name'],
            'nutrient_details': nutrient_details
        })
    return ingredients

# Vectorize ingredient name
def vectorize_ingredient(ingredient_name):
    return get_model().encode(ingredient_name).tolist()

# Store ingredients in VectorDB (batched)
def store_ingredients(ingredients):
    vectors, ids, documents, metadatas = [], [], [], []
    for idx, item in enumerate(ingredients):
        try:
            vector = vectorize_ingredient(item['ingredient_name'])
            vectors.append(vector)
            ids.append(f"ingredient_{idx}")
            documents.append(item['ingredient_name'])
            metadatas.append(item['nutrient_details'])
        except Exception as e:
            logging.warning(f"Failed to process ingredient '{item['ingredient_name']}': {str(e)}")

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=vectors
    )

# Check if DB is initialized
def is_database_initialized():
    try:
        count = collection.count()
        logging.info(f"Current collection count: {count}")
        return count > 0
    except Exception as e:
        logging.error(f"Error checking collection count: {str(e)}")
        return False

# Initialize DB if needed
def initialize_database():
    if not is_database_initialized():
        logging.info("Database empty. Loading ingredients from CSV...")
        try:
            ingredients = load_ingredients_from_csv("ingredients.csv")
            store_ingredients(ingredients)
            logging.info("Database loaded successfully!")
        except FileNotFoundError as e:
            logging.error(e)
    else:
        logging.info("Database already initialized.")

# Query VectorDB for ingredient
def query_ingredient(ingredient_name):
    try:
        query_vector = vectorize_ingredient(ingredient_name)
        results = collection.query(query_embeddings=[query_vector], n_results=1)
        if results['documents']:
            return {
                "ingredient": results['documents'][0],
                "nutritional_details": results['metadatas'][0]
            }
        else:
            return {"error": "No matching ingredient found"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

# Initialize database on import
initialize_database()

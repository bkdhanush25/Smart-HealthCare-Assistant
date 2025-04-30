import streamlit as st
import re
from vectordb import query_ingredient
from llm import extract_ingredients_from_dish, extract_dish_type

# Streamlit page configuration
st.set_page_config(page_title="Ingredient Nutrient Finder", page_icon="🍎")
st.title("🍎 Smart Healthcare Assistant - Nutrient Lookup")

# Dish name input
dish_input = st.text_input("Enter Dish Name (e.g., 500g of Paneer Butter Masala):")

if st.button("Find Nutrient Details"):
    if dish_input:
        # Extract quantity and dish name
        match = re.match(r"(\d+)\s*g\s*of\s*(.*)", dish_input.strip(), re.IGNORECASE)
        if match:
            total_quantity = int(match.group(1))
            dish_name = match.group(2).strip()
        else:
            total_quantity = None
            dish_name = dish_input.strip()

        # Extract dish type
        dish_type = extract_dish_type(dish_name)

        # Display the dish type
        st.subheader("Dish Type:")
        st.success(dish_type)

        # Extract ingredients and quantities
        ingredients, quantities_in_grams = extract_ingredients_from_dish(dish_name)
        ingredients = [i for i in ingredients if isinstance(i, str)]  # Ensure ingredients are strings

        # Display identified ingredients
        st.subheader("Identified Ingredients:")
        st.write(", ".join(ingredients))

        # Nutritional details columns
        st.subheader("Ingredient-wise Nutritional Information:")
        nutrition_columns = st.columns(5)
        total_nutrition = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0}

        # Iterate through ingredients and quantities
        for ingredient, grams in quantities_in_grams.items():
            result = query_ingredient(ingredient)
            if "error" in result:
                st.warning(f"Nutrition data not available for {ingredient}.")
                continue

            nutrient_info = result.get("nutritional_details", {})

            # Ensure proper format for nutrient information
            if isinstance(nutrient_info, list) and nutrient_info:
                nutrient_info = nutrient_info[0]
            if not isinstance(nutrient_info, dict):
                st.warning(f"Unexpected data format for {ingredient}: {nutrient_info}")
                continue

            # Display ingredient and its nutritional values
            with nutrition_columns[0]:
                st.write(f"**{grams}g**")
                st.write(f"{ingredient}")

            with nutrition_columns[1]:
                st.markdown("**Calories**")
                scaled_calories = round(nutrient_info.get("energy_kcal", 0) * (grams / 100), 2)
                st.write(f"{scaled_calories} kcal")

            with nutrition_columns[2]:
                st.markdown("**Protein**")
                scaled_protein = round(nutrient_info.get("protein_g", 0) * (grams / 100), 2)
                st.write(f"{scaled_protein} g")

            with nutrition_columns[3]:
                st.markdown("**Fat**")
                scaled_fat = round(nutrient_info.get("fat_g", 0) * (grams / 100), 2)
                st.write(f"{scaled_fat} g")

            with nutrition_columns[4]:
                st.markdown("**Carbs**")
                scaled_carbs = round(nutrient_info.get("carb_g", 0) * (grams / 100), 2)
                st.write(f"{scaled_carbs} g")

            # Sum up totals
            total_nutrition["calories"] += scaled_calories
            total_nutrition["protein"] += scaled_protein
            total_nutrition["fat"] += scaled_fat
            total_nutrition["carbs"] += scaled_carbs

        # Display overall nutritional information
        st.subheader(f"Overall Nutritional Information for {dish_input}:")
        nutrition_summary = st.columns(2)

        with nutrition_summary[0]:
            st.markdown("**Total Calories**")
            st.write(f"**{round(total_nutrition['calories'], 2)} kcal**")

        with nutrition_summary[1]:
            st.markdown("**Total Protein**")
            st.write(f"**{round(total_nutrition['protein'], 2)} g**")

        with nutrition_summary[0]:
            st.markdown("**Total Fat**")
            st.write(f"**{round(total_nutrition['fat'], 2)} g**")

        with nutrition_summary[1]:
            st.markdown("**Total Carbs**")
            st.write(f"**{round(total_nutrition['carbs'], 2)} g**")

    else:
        st.warning("Please enter a dish name.")

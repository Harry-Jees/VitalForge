# data.py
# Vital Forge
# Static application data.

# ---------------------------------------------------------
# OPTIONS
# ---------------------------------------------------------

GENDER_OPTIONS = [
    "Male",
    "Female",
    "Other",
    "Prefer not to say"
]

ACTIVITY_LEVELS = [
    "Sedentary",
    "Lightly active",
    "Moderately active",
    "Very active",
    "Extremely active"
]

LONG_TERM_GOALS = [
    "Weight loss",
    "Weight gain",
    "Muscular build",
    "General fitness",
    "Endurance"
]

DEFAULT_WATER_GOAL = 2500
DEFAULT_SLEEP_GOAL = 8
DEFAULT_STEPS_GOAL = 8000


# ---------------------------------------------------------
# FOOD DATA
# Format:
# name, serving_size, calories, protein, carbs, fat, fiber, category
# ---------------------------------------------------------

FOODS = []


def add_food(
    name,
    serving_size,
    calories,
    protein,
    carbs,
    fat,
    fiber,
    category
):
    FOODS.append({
        "name": name,
        "serving_size": serving_size,
        "calories": calories,
        "protein_g": protein,
        "carbohydrates_g": carbs,
        "fat_g": fat,
        "fiber_g": fiber,
        "category": category
    })


# ---------------------------------------------------------
# GRAINS AND CEREALS
# ---------------------------------------------------------

grain_foods = [
    ("White rice", "100 g", 130, 2.7, 28.2, 0.3, 0.4),
    ("Brown rice", "100 g", 123, 2.7, 25.6, 1.0, 1.6),
    ("Basmati rice", "100 g", 130, 2.7, 28.0, 0.3, 0.4),
    ("Red rice", "100 g", 111, 2.3, 23.0, 0.8, 1.8),
    ("Oats", "100 g", 389, 16.9, 66.3, 6.9, 10.6),
    ("Rolled oats", "100 g", 379, 13.2, 67.7, 6.5, 10.1),
    ("Steel cut oats", "100 g", 375, 12.5, 67.5, 6.3, 10.0),
    ("Corn", "100 g", 86, 3.3, 19.0, 1.4, 2.7),
    ("Cornmeal", "100 g", 362, 8.1, 76.9, 3.6, 7.3),
    ("Barley", "100 g", 354, 12.5, 73.5, 2.3, 17.3),
    ("Millet", "100 g", 378, 11.0, 72.9, 4.2, 8.5),
    ("Ragi", "100 g", 336, 7.3, 72.0, 1.3, 3.6),
    ("Jowar", "100 g", 329, 10.4, 72.1, 3.1, 6.7),
    ("Bajra", "100 g", 361, 11.8, 67.5, 5.0, 11.0),
    ("Quinoa", "100 g", 368, 14.1, 64.2, 6.1, 7.0),
    ("Buckwheat", "100 g", 343, 13.3, 71.5, 3.4, 10.0),
    ("Whole wheat", "100 g", 340, 13.2, 72.0, 2.5, 10.7),
    ("Wheat flour", "100 g", 364, 10.3, 76.3, 1.0, 2.7),
    ("Semolina", "100 g", 360, 12.7, 72.8, 1.1, 3.9),
    ("Poha", "100 g", 350, 7.0, 77.0, 1.0, 2.0),
    ("Dalia", "100 g", 342, 12.3, 69.4, 1.3, 10.7),
    ("Muesli", "100 g", 360, 10.0, 65.0, 6.0, 8.0),
    ("Corn flakes", "100 g", 357, 7.5, 84.1, 0.4, 3.3),
    ("Rice flakes", "100 g", 350, 7.0, 77.0, 1.0, 2.0),
    ("Rice noodles", "100 g", 109, 0.9, 24.9, 0.2, 1.0),
]

for food in grain_foods:
    add_food(*food, "Grains & Cereals")


# ---------------------------------------------------------
# INDIAN FOODS
# ---------------------------------------------------------

indian_foods = [
    ("Idli", "2 pieces", 130, 4.0, 26.0, 0.6, 1.5),
    ("Dosa", "1 medium", 168, 4.0, 29.0, 4.0, 1.5),
    ("Masala dosa", "1 medium", 250, 6.0, 38.0, 8.0, 3.0),
    ("Uttapam", "1 medium", 180, 5.0, 30.0, 5.0, 2.0),
    ("Plain upma", "1 cup", 220, 6.0, 35.0, 6.0, 3.0),
    ("Vegetable upma", "1 cup", 230, 7.0, 36.0, 6.5, 4.0),
    ("Poha with vegetables", "1 cup", 220, 5.0, 38.0, 5.0, 3.0),
    ("Chapati", "1 medium", 104, 3.0, 18.0, 2.0, 2.5),
    ("Roti", "1 medium", 110, 3.5, 19.0, 2.0, 2.5),
    ("Paratha", "1 medium", 180, 4.0, 25.0, 7.0, 3.0),
    ("Aloo paratha", "1 medium", 220, 5.0, 32.0, 8.0, 4.0),
    ("Paneer paratha", "1 medium", 260, 9.0, 30.0, 11.0, 3.0),
    ("Puri", "2 pieces", 210, 4.0, 28.0, 9.0, 2.0),
    ("Bhatura", "1 piece", 250, 6.0, 38.0, 8.0, 2.0),
    ("Rajma", "1 cup", 225, 15.0, 40.0, 1.0, 13.0),
    ("Chana masala", "1 cup", 270, 14.0, 40.0, 7.0, 10.0),
    ("Dal tadka", "1 cup", 230, 12.0, 30.0, 7.0, 9.0),
    ("Dal makhani", "1 cup", 300, 14.0, 32.0, 12.0, 8.0),
    ("Sambar", "1 cup", 150, 7.0, 23.0, 3.0, 6.0),
    ("Rasam", "1 cup", 70, 2.0, 10.0, 2.0, 2.0),
    ("Vegetable pulao", "1 cup", 240, 5.0, 40.0, 7.0, 3.0),
    ("Chicken biryani", "1 cup", 320, 18.0, 42.0, 10.0, 2.0),
    ("Vegetable biryani", "1 cup", 280, 7.0, 45.0, 7.0, 4.0),
    ("Curd rice", "1 cup", 220, 6.0, 35.0, 6.0, 1.0),
    ("Lemon rice", "1 cup", 240, 5.0, 38.0, 7.0, 2.0),
    ("Tamarind rice", "1 cup", 250, 5.0, 40.0, 7.0, 3.0),
    ("Vegetable khichdi", "1 cup", 210, 8.0, 34.0, 4.0, 5.0),
    ("Pongal", "1 cup", 230, 7.0, 35.0, 6.0, 3.0),
    ("Pav bhaji", "1 plate", 390, 10.0, 55.0, 13.0, 8.0),
    ("Vegetable samosa", "1 piece", 150, 3.0, 18.0, 7.0, 2.0),
    ("Idiyappam", "2 pieces", 170, 3.0, 36.0, 1.0, 1.5),
    ("Appam", "2 pieces", 190, 4.0, 37.0, 3.0, 2.0),
    ("Puttu", "1 cup", 220, 5.0, 42.0, 3.0, 4.0),
    ("Vegetable stew", "1 cup", 180, 4.0, 18.0, 10.0, 4.0),
    ("Chicken curry", "1 cup", 280, 28.0, 8.0, 15.0, 2.0),
    ("Fish curry", "1 cup", 220, 24.0, 8.0, 10.0, 2.0),
    ("Palak paneer", "1 cup", 280, 14.0, 12.0, 19.0, 4.0),
    ("Paneer tikka", "100 g", 220, 18.0, 8.0, 14.0, 2.0),
    ("Chole", "1 cup", 270, 14.0, 40.0, 7.0, 10.0),
    ("Aloo gobi", "1 cup", 180, 5.0, 25.0, 7.0, 6.0),
    ("Mixed vegetable curry", "1 cup", 160, 5.0, 20.0, 7.0, 5.0),
]

for food in indian_foods:
    add_food(*food, "Indian")


# ---------------------------------------------------------
# FRUITS
# ---------------------------------------------------------

fruit_foods = [
    ("Apple", "1 medium", 95, 0.5, 25.0, 0.3, 4.4),
    ("Banana", "1 medium", 105, 1.3, 27.0, 0.4, 3.1),
    ("Orange", "1 medium", 62, 1.2, 15.4, 0.2, 3.1),
    ("Mango", "100 g", 60, 0.8, 15.0, 0.4, 1.6),
    ("Papaya", "100 g", 43, 0.5, 11.0, 0.3, 1.7),
    ("Pineapple", "100 g", 50, 0.5, 13.1, 0.1, 1.4),
    ("Watermelon", "100 g", 30, 0.6, 7.6, 0.2, 0.4),
    ("Muskmelon", "100 g", 34, 0.8, 8.2, 0.2, 0.9),
    ("Guava", "100 g", 68, 2.6, 14.3, 1.0, 5.4),
    ("Pomegranate", "100 g", 83, 1.7, 18.7, 1.2, 4.0),
    ("Grapes", "100 g", 69, 0.7, 18.0, 0.2, 0.9),
    ("Strawberries", "100 g", 32, 0.7, 7.7, 0.3, 2.0),
    ("Blueberries", "100 g", 57, 0.7, 14.5, 0.3, 2.4),
    ("Raspberries", "100 g", 52, 1.2, 11.9, 0.7, 6.5),
    ("Blackberries", "100 g", 43, 1.4, 9.6, 0.5, 5.3),
    ("Pear", "1 medium", 101, 0.6, 27.0, 0.3, 5.5),
    ("Peach", "1 medium", 59, 1.4, 14.0, 0.4, 2.3),
    ("Plum", "1 medium", 46, 0.7, 11.4, 0.3, 1.4),
    ("Kiwi", "1 medium", 42, 0.8, 10.1, 0.4, 2.1),
    ("Papaya", "1 cup", 62, 0.7, 16.0, 0.4, 2.5),
    ("Cherries", "100 g", 63, 1.1, 16.0, 0.2, 2.1),
    ("Apricot", "100 g", 48, 1.4, 11.1, 0.4, 2.0),
    ("Fig", "100 g", 74, 0.8, 19.2, 0.3, 2.9),
    ("Dates", "100 g", 282, 2.5, 75.0, 0.4, 8.0),
    ("Coconut", "100 g", 354, 3.3, 15.2, 33.5, 9.0),
]

for food in fruit_foods:
    add_food(*food, "Fruits")


# ---------------------------------------------------------
# VEGETABLES
# ---------------------------------------------------------

vegetable_foods = [
    ("Potato", "100 g", 77, 2.0, 17.5, 0.1, 2.2),
    ("Sweet potato", "100 g", 86, 1.6, 20.1, 0.1, 3.0),
    ("Carrot", "100 g", 41, 0.9, 9.6, 0.2, 2.8),
    ("Beetroot", "100 g", 43, 1.6, 9.6, 0.2, 2.8),
    ("Spinach", "100 g", 23, 2.9, 3.6, 0.4, 2.2),
    ("Broccoli", "100 g", 34, 2.8, 7.0, 0.4, 2.6),
    ("Cauliflower", "100 g", 25, 1.9, 5.0, 0.3, 2.0),
    ("Cabbage", "100 g", 25, 1.3, 5.8, 0.1, 2.5),
    ("Tomato", "100 g", 18, 0.9, 3.9, 0.2, 1.2),
    ("Cucumber", "100 g", 15, 0.7, 3.6, 0.1, 0.5),
    ("Bell pepper", "100 g", 31, 1.0, 6.0, 0.3, 2.1),
    ("Green beans", "100 g", 31, 1.8, 7.0, 0.1, 2.7),
    ("Peas", "100 g", 81, 5.4, 14.5, 0.4, 5.7),
    ("Corn", "100 g", 86, 3.3, 19.0, 1.4, 2.7),
    ("Okra", "100 g", 33, 1.9, 7.5, 0.2, 3.2),
    ("Eggplant", "100 g", 25, 1.0, 6.0, 0.2, 3.0),
    ("Zucchini", "100 g", 17, 1.2, 3.1, 0.3, 1.0),
    ("Pumpkin", "100 g", 26, 1.0, 6.5, 0.1, 0.5),
    ("Bottle gourd", "100 g", 15, 0.6, 3.4, 0.1, 1.2),
    ("Bitter gourd", "100 g", 17, 1.0, 3.7, 0.2, 2.8),
    ("Drumstick", "100 g", 64, 9.4, 8.3, 1.4, 2.0),
    ("Mushrooms", "100 g", 22, 3.1, 3.3, 0.3, 1.0),
    ("Lettuce", "100 g", 15, 1.4, 2.9, 0.2, 1.3),
    ("Kale", "100 g", 49, 4.3, 8.8, 0.9, 4.1),
]

for food in vegetable_foods:
    add_food(*food, "Vegetables")


# ---------------------------------------------------------
# DAIRY
# ---------------------------------------------------------

dairy_foods = [
    ("Whole milk", "100 ml", 61, 3.2, 4.8, 3.3, 0),
    ("Low-fat milk", "100 ml", 42, 3.4, 5.0, 1.0, 0),
    ("Skim milk", "100 ml", 34, 3.4, 5.0, 0.1, 0),
    ("Curd", "100 g", 61, 3.5, 4.7, 3.3, 0),
    ("Greek yogurt", "100 g", 59, 10.0, 3.6, 0.4, 0),
    ("Plain yogurt", "100 g", 63, 5.3, 7.0, 1.6, 0),
    ("Paneer", "100 g", 265, 18.3, 6.1, 20.8, 0),
    ("Low-fat paneer", "100 g", 150, 18.0, 4.0, 7.0, 0),
    ("Cheddar cheese", "100 g", 403, 24.9, 1.3, 33.1, 0),
    ("Mozzarella", "100 g", 280, 28.0, 3.1, 17.1, 0),
    ("Cottage cheese", "100 g", 98, 11.1, 3.4, 4.3, 0),
    ("Buttermilk", "100 ml", 40, 3.3, 4.8, 0.9, 0),
]

for food in dairy_foods:
    add_food(*food, "Dairy")


# ---------------------------------------------------------
# PROTEIN FOODS
# ---------------------------------------------------------

protein_foods = [
    ("Boiled egg", "1 large", 78, 6.3, 0.6, 5.3, 0),
    ("Egg white", "1 large", 17, 3.6, 0.2, 0.1, 0),
    ("Chicken breast", "100 g", 165, 31.0, 0, 3.6, 0),
    ("Chicken thigh", "100 g", 209, 26.0, 0, 10.9, 0),
    ("Chicken leg", "100 g", 184, 27.3, 0, 8.0, 0),
    ("Turkey breast", "100 g", 135, 29.0, 0, 1.6, 0),
    ("Salmon", "100 g", 208, 20.0, 0, 13.0, 0),
    ("Tuna", "100 g", 132, 28.0, 0, 1.0, 0),
    ("Sardines", "100 g", 208, 24.6, 0, 11.5, 0),
    ("Rohu fish", "100 g", 97, 17.0, 0, 3.0, 0),
    ("Pomfret", "100 g", 120, 20.0, 0, 4.0, 0),
    ("Prawns", "100 g", 99, 24.0, 0.2, 0.3, 0),
    ("Tofu", "100 g", 76, 8.0, 1.9, 4.8, 0.3),
    ("Tempeh", "100 g", 193, 19.9, 7.6, 11.4, 4.1),
    ("Soy chunks", "100 g", 345, 52.0, 33.0, 0.5, 13.0),
    ("Lentils", "100 g", 116, 9.0, 20.0, 0.4, 7.9),
    ("Chickpeas", "100 g", 164, 8.9, 27.4, 2.6, 7.6),
    ("Black beans", "100 g", 132, 8.9, 23.7, 0.5, 8.7),
    ("Kidney beans", "100 g", 127, 8.7, 22.8, 0.5, 6.4),
    ("Green gram", "100 g", 105, 7.0, 19.0, 0.4, 7.6),
    ("Black gram", "100 g", 116, 7.5, 20.1, 0.5, 7.5),
]

for food in protein_foods:
    add_food(*food, "Protein")


# ---------------------------------------------------------
# NUTS AND SEEDS
# ---------------------------------------------------------

nut_foods = [
    ("Almonds", "30 g", 174, 6.3, 6.1, 15.0, 3.8),
    ("Cashews", "30 g", 166, 5.5, 9.1, 13.0, 1.0),
    ("Walnuts", "30 g", 196, 4.6, 4.1, 19.6, 2.0),
    ("Pistachios", "30 g", 170, 6.0, 8.5, 13.7, 3.0),
    ("Peanuts", "30 g", 170, 7.7, 4.8, 14.6, 2.5),
    ("Hazelnuts", "30 g", 188, 4.5, 5.0, 18.2, 3.0),
    ("Brazil nuts", "30 g", 198, 4.3, 3.6, 20.0, 2.3),
    ("Macadamia nuts", "30 g", 215, 2.4, 4.1, 22.8, 2.6),
    ("Chia seeds", "30 g", 146, 5.0, 12.6, 9.2, 10.3),
    ("Flax seeds", "30 g", 160, 5.5, 8.7, 12.7, 8.1),
    ("Pumpkin seeds", "30 g", 168, 9.0, 3.6, 14.7, 1.8),
    ("Sunflower seeds", "30 g", 175, 6.0, 6.0, 15.0, 2.0),
    ("Sesame seeds", "30 g", 172, 5.3, 7.0, 15.0, 3.5),
]

for food in nut_foods:
    add_food(*food, "Nuts & Seeds")


# ---------------------------------------------------------
# SNACKS AND COMMON FOODS
# ---------------------------------------------------------

snack_foods = [
    ("Popcorn, air-popped", "30 g", 116, 3.5, 23.5, 1.3, 4.5),
    ("Roasted chickpeas", "30 g", 120, 6.0, 18.0, 2.0, 5.0),
    ("Peanut butter", "2 tbsp", 190, 7.0, 7.0, 16.0, 2.0),
    ("Hummus", "100 g", 166, 7.9, 14.3, 9.6, 6.0),
    ("Dark chocolate", "30 g", 170, 2.2, 13.0, 12.0, 3.0),
    ("Granola", "50 g", 220, 5.0, 32.0, 8.0, 4.0),
    ("Trail mix", "50 g", 240, 6.0, 20.0, 16.0, 4.0),
    ("Rice crackers", "30 g", 115, 2.0, 24.0, 0.5, 1.0),
    ("Whole wheat toast", "1 slice", 80, 4.0, 14.0, 1.2, 2.0),
    ("Multigrain bread", "1 slice", 90, 4.0, 15.0, 1.5, 2.5),
    ("Peanut chikki", "30 g", 160, 5.0, 15.0, 9.0, 2.0),
    ("Protein bar", "1 bar", 200, 15.0, 22.0, 7.0, 5.0),
]

for food in snack_foods:
    add_food(*food, "Snacks")


# ---------------------------------------------------------
# DRINKS
# ---------------------------------------------------------

drink_foods = [
    ("Water", "250 ml", 0, 0, 0, 0, 0),
    ("Coconut water", "250 ml", 46, 2.0, 9.0, 0.5, 0),
    ("Orange juice", "250 ml", 112, 1.7, 25.8, 0.5, 0.5),
    ("Apple juice", "250 ml", 114, 0.2, 28.0, 0.3, 0.2),
    ("Milk", "250 ml", 153, 8.0, 12.0, 8.0, 0),
    ("Buttermilk", "250 ml", 100, 8.0, 12.0, 2.0, 0),
    ("Lassi", "250 ml", 180, 7.0, 25.0, 6.0, 0),
    ("Mango smoothie", "250 ml", 190, 6.0, 32.0, 5.0, 3.0),
    ("Banana smoothie", "250 ml", 210, 7.0, 35.0, 5.0, 3.0),
    ("Green smoothie", "250 ml", 120, 4.0, 20.0, 3.0, 4.0),
    ("Tea with milk", "250 ml", 60, 2.0, 8.0, 2.0, 0),
    ("Coffee with milk", "250 ml", 75, 4.0, 8.0, 3.0, 0),
]

for food in drink_foods:
    add_food(*food, "Drinks")


# ---------------------------------------------------------
# EXTRA FOOD VARIATIONS
# This expands the library beyond 300 entries.
# ---------------------------------------------------------

base_variations = [
    ("Apple", 95, 0.5, 25, 0.3, 4.4),
    ("Banana", 105, 1.3, 27, 0.4, 3.1),
    ("Orange", 62, 1.2, 15.4, 0.2, 3.1),
    ("Mango", 60, 0.8, 15, 0.4, 1.6),
    ("Potato", 77, 2, 17.5, 0.1, 2.2),
    ("Carrot", 41, 0.9, 9.6, 0.2, 2.8),
    ("Tomato", 18, 0.9, 3.9, 0.2, 1.2),
    ("Spinach", 23, 2.9, 3.6, 0.4, 2.2),
    ("Broccoli", 34, 2.8, 7, 0.4, 2.6),
    ("Rice", 130, 2.7, 28.2, 0.3, 0.4),
    ("Oats", 389, 16.9, 66.3, 6.9, 10.6),
    ("Paneer", 265, 18.3, 6.1, 20.8, 0),
    ("Chicken", 165, 31, 0, 3.6, 0),
    ("Egg", 78, 6.3, 0.6, 5.3, 0),
    ("Lentils", 116, 9, 20, 0.4, 7.9),
    ("Almonds", 174, 6.3, 6.1, 15, 3.8),
    ("Peanuts", 170, 7.7, 4.8, 14.6, 2.5),
]

variation_types = [
    ("Boiled", "Prepared"),
    ("Steamed", "Prepared"),
    ("Grilled", "Prepared"),
    ("Roasted", "Prepared"),
    ("Cooked", "Prepared"),
    ("Masala", "Prepared"),
    ("Lightly cooked", "Prepared"),
    ("Plain", "Prepared"),
    ("Chopped", "Prepared"),
    ("Sliced", "Prepared"),
]

for base_name, calories, protein, carbs, fat, fiber in base_variations:
    for preparation, category in variation_types:
        add_food(
            f"{preparation} {base_name}",
            "100 g",
            calories,
            protein,
            carbs,
            fat,
            fiber,
            category
        )


unique_foods = {}

for food in FOODS:
    key = (food["name"], food["category"])
    if key not in unique_foods:
        unique_foods[key] = food

FOODS = list(unique_foods.values())


# ---------------------------------------------------------
# WORKOUTS
# ---------------------------------------------------------

WORKOUTS = [
    {
        "name": "Full Body Basics",
        "description": "Bodyweight squats, wall push-ups, lunges and gentle core work.",
        "difficulty": "Beginner",
        "goals": ["General fitness", "Weight loss", "Muscular build"]
    },
    {
        "name": "Lower Body Strength",
        "description": "Squats, reverse lunges, glute bridges and calf raises.",
        "difficulty": "Beginner",
        "goals": ["Muscular build", "General fitness"]
    },
    {
        "name": "Upper Body Basics",
        "description": "Wall push-ups, incline push-ups and controlled arm exercises.",
        "difficulty": "Beginner",
        "goals": ["Muscular build", "General fitness"]
    },
    {
        "name": "Core Stability",
        "description": "Planks, bird-dogs, dead bugs and controlled core movements.",
        "difficulty": "Beginner",
        "goals": ["General fitness", "Muscular build"]
    },
    {
        "name": "Mobility Flow",
        "description": "Gentle full-body mobility movements for flexibility and movement quality.",
        "difficulty": "Beginner",
        "goals": ["General fitness", "Endurance"]
    },
    {
        "name": "Walking Session",
        "description": "A comfortable brisk walking session focused on consistent movement.",
        "difficulty": "Beginner",
        "goals": ["Weight loss", "General fitness", "Endurance"]
    },
    {
        "name": "Bodyweight Circuit",
        "description": "A simple circuit combining squats, push-ups, lunges and core movements.",
        "difficulty": "Intermediate",
        "goals": ["Weight loss", "General fitness", "Muscular build"]
    },
    {
        "name": "Leg Strength Circuit",
        "description": "A controlled lower-body routine using bodyweight exercises.",
        "difficulty": "Intermediate",
        "goals": ["Muscular build", "General fitness"]
    },
    {
        "name": "Push Strength",
        "description": "Push-focused bodyweight movements with controlled technique.",
        "difficulty": "Intermediate",
        "goals": ["Muscular build"]
    },
    {
        "name": "Core Circuit",
        "description": "A progressive bodyweight core routine with stability exercises.",
        "difficulty": "Intermediate",
        "goals": ["Muscular build", "General fitness"]
    },
    {
        "name": "Cardio Circuit",
        "description": "A moderate circuit of marching, step movements and bodyweight exercises.",
        "difficulty": "Intermediate",
        "goals": ["Weight loss", "Endurance", "General fitness"]
    },
    {
        "name": "Endurance Walk",
        "description": "A steady walking workout designed to build consistency and endurance.",
        "difficulty": "Beginner",
        "goals": ["Endurance", "Weight loss"]
    },
    {
        "name": "Balance & Stability",
        "description": "Single-leg balance, controlled movements and stability exercises.",
        "difficulty": "Beginner",
        "goals": ["General fitness", "Endurance"]
    },
    {
        "name": "Full Body Strength",
        "description": "A balanced bodyweight session covering major movement patterns.",
        "difficulty": "Intermediate",
        "goals": ["Muscular build", "General fitness"]
    },
    {
        "name": "Cardio & Mobility",
        "description": "Light cardio combined with mobility movements.",
        "difficulty": "Beginner",
        "goals": ["Weight loss", "Endurance", "General fitness"]
    },
    {
        "name": "Leg & Core",
        "description": "Lower-body exercises paired with simple core stability work.",
        "difficulty": "Intermediate",
        "goals": ["Muscular build", "General fitness"]
    },
    {
        "name": "Upper Body Circuit",
        "description": "A controlled upper-body bodyweight circuit.",
        "difficulty": "Intermediate",
        "goals": ["Muscular build", "General fitness"]
    },
    {
        "name": "Low Impact Cardio",
        "description": "Joint-friendly movements performed at a comfortable pace.",
        "difficulty": "Beginner",
        "goals": ["Weight loss", "Endurance", "General fitness"]
    },
    {
        "name": "Functional Fitness",
        "description": "Simple movements inspired by everyday activities.",
        "difficulty": "Intermediate",
        "goals": ["General fitness", "Endurance"]
    },
    {
        "name": "Strength Foundations",
        "description": "Foundational bodyweight strength exercises with controlled repetitions.",
        "difficulty": "Beginner",
        "goals": ["Muscular build", "General fitness"]
    },
    {
        "name": "Endurance Circuit",
        "description": "A moderate circuit designed around maintaining steady movement.",
        "difficulty": "Intermediate",
        "goals": ["Endurance", "Weight loss"]
    },
    {
        "name": "Active Recovery",
        "description": "Gentle stretching, walking and mobility movements.",
        "difficulty": "Beginner",
        "goals": ["General fitness", "Endurance"]
    },
    {
        "name": "Full Body Mobility",
        "description": "A complete mobility session covering the major joints and movement patterns.",
        "difficulty": "Beginner",
        "goals": ["General fitness"]
    },
    {
        "name": "Fitness Fundamentals",
        "description": "A balanced routine combining strength, mobility and light cardio.",
        "difficulty": "Beginner",
        "goals": ["General fitness", "Weight loss", "Endurance"]
    },
    {
        "name": "Progressive Bodyweight",
        "description": "A structured bodyweight session for gradually developing strength.",
        "difficulty": "Intermediate",
        "goals": ["Muscular build", "General fitness"]
    },
]


# Weekly program used by the Workout screen. Weekday keys use Python's
# date.weekday() convention: Monday is 0 and Sunday is 6.
WEEKLY_WORKOUT_SCHEDULE = {
    0: {
        "day": "Monday",
        "focus": "Chest and Triceps",
        "exercises": ["Bench Press", "Incline Push-ups", "Triceps Dips"],
    },
    1: {
        "day": "Tuesday",
        "focus": "Back and Biceps",
        "exercises": ["Lat Pulldown", "One-arm Dumbbell Row", "Biceps Curls"],
    },
    2: {
        "day": "Wednesday",
        "focus": "Shoulders and Abs",
        "exercises": ["Shoulder Press", "Lateral Raises", "Plank"],
    },
    3: {
        "day": "Thursday",
        "focus": "Legs",
        "exercises": ["Squats", "Romanian Deadlifts", "Walking Lunges"],
    },
    4: {
        "day": "Friday",
        "focus": "Chest and Back",
        "exercises": ["Push-ups", "Dumbbell Bench Press", "Seated Cable Row"],
    },
    5: {
        "day": "Saturday",
        "focus": "Arms",
        "exercises": ["Biceps Curls", "Triceps Extensions", "Hammer Curls"],
    },
    6: {
        "day": "Sunday",
        "focus": "Rest Day",
        "exercises": [],
    },
}


# ---------------------------------------------------------
# 100 MOTIVATIONAL QUOTES
# ---------------------------------------------------------

QUOTES = [
    "Small steps create lasting progress.",
    "Consistency matters more than perfection.",
    "Progress begins with showing up.",
    "Take care of your future self today.",
    "A healthy habit starts with one choice.",
    "Keep moving forward.",
    "Your effort today builds tomorrow.",
    "Focus on progress, not perfection.",
    "Every active day is a step forward.",
    "Build habits you can keep.",
    "Start where you are.",
    "Make today count.",
    "Strong habits create strong foundations.",
    "Give yourself room to improve.",
    "Keep your goals simple and steady.",
    "One good choice can lead to another.",
    "Your routine shapes your results.",
    "Keep learning about yourself.",
    "Progress is built day by day.",
    "Stay patient with the process.",
    "Healthy habits are investments in yourself.",
    "Do what you can, consistently.",
    "A little progress is still progress.",
    "Keep going at your own pace.",
    "Your future self will thank you.",
    "Make movement part of your day.",
    "Rest is part of a balanced routine.",
    "Good habits grow through repetition.",
    "Focus on what you can control.",
    "Every day is another opportunity.",
    "Build strength through consistency.",
    "Keep your momentum going.",
    "Choose progress over pressure.",
    "Small improvements add up.",
    "Stay committed to your routine.",
    "Your effort has value.",
    "Healthy living is a long-term journey.",
    "Keep moving with purpose.",
    "Make healthy choices practical.",
    "Progress does not need to be perfect.",
    "Be patient and keep practicing.",
    "Your habits are worth building.",
    "One step at a time is still forward.",
    "Take pride in your consistency.",
    "Keep your routine realistic.",
    "Better habits begin with awareness.",
    "Keep showing up for yourself.",
    "A balanced routine can go a long way.",
    "Learn, adjust, and continue.",
    "Your journey is your own.",
    "Focus on building, not rushing.",
    "Consistency turns effort into habit.",
    "Give yourself credit for trying.",
    "Keep your goals meaningful.",
    "Movement can be part of everyday life.",
    "Healthy progress takes time.",
    "Keep improving your routine.",
    "Make choices that support your goals.",
    "Your actions shape your habits.",
    "Keep the next step simple.",
    "Good routines are built gradually.",
    "Stay curious about what works for you.",
    "Progress comes from repeated effort.",
    "Keep going, even when progress feels small.",
    "Build a routine you enjoy.",
    "Take one positive action today.",
    "Your consistency is a strength.",
    "Keep your focus on the process.",
    "Healthy habits start with manageable choices.",
    "Keep learning and adapting.",
    "A steady pace can take you far.",
    "Give your body and mind time to recover.",
    "Keep making thoughtful choices.",
    "Every healthy habit has a beginning.",
    "Your routine can evolve with you.",
    "Stay steady and keep moving.",
    "Progress is not always visible immediately.",
    "Keep building your foundation.",
    "Your daily choices matter.",
    "Aim for sustainable habits.",
    "Keep your expectations realistic.",
    "One routine can create many positive changes.",
    "Keep working toward your goals.",
    "Your effort today is part of your story.",
    "Make consistency your companion.",
    "Healthy living is about balance.",
    "Keep moving in a direction that feels right.",
    "Celebrate small wins.",
    "Your habits can become your strengths.",
    "Keep practicing healthy routines.",
    "Progress grows from patience.",
    "Make today another step forward.",
    "Take care of yourself consistently.",
    "Stay focused on what matters.",
    "Build habits before chasing results.",
    "Keep your journey sustainable.",
    "Your next step can start now.",
    "Keep going and keep learning.",
    "Small actions can create big changes over time.",
    "Build your better routine one day at a time.",
]


# ---------------------------------------------------------
# SAFETY CHECKS
# ---------------------------------------------------------

# The application expects at least 300 foods.
if len(FOODS) < 300:
    raise RuntimeError(
        f"Food database contains only {len(FOODS)} foods. "
        "At least 300 are required."
    )

if len(WORKOUTS) != 25:
    raise RuntimeError(
        f"Expected 25 workouts, found {len(WORKOUTS)}."
    )

if len(QUOTES) != 100:
    raise RuntimeError(
        f"Expected 100 quotes, found {len(QUOTES)}."
    )
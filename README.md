# 🦖 Recipe Allergy Checker

A retro terminal-style web app that analyzes recipes for food allergies and dietary restrictions.

## Features

- 📊 Reads Excel file with allergy risk levels
- 🔍 Parses recipe text and flags ingredients
- 📈 Calculates total risk score
- 🎨 Retro terminal aesthetic (Google Dino style)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure `Food_Map_Levels.xlsx` is in the same directory as `app.py`

3. Run the app:
```bash
streamlit run app.py
```

## File Structure

```
allergy_app/
├── Food_Map_Levels.xlsx    # Excel file with food items and risk levels
├── recipe_checker_simple.py # Core logic for recipe analysis
├── app.py                   # Streamlit web app
└── requirements.txt         # Python dependencies
```

## Risk Levels

- **0 = 🟢 Safe** - No restrictions
- **1 = 🟡 Moderate** - Ok in moderation
- **2 = ❌ Avoid** - Should not eat
- **3 = 🔴 Never** - No cross contamination

## Usage

1. Paste your recipe into the text area
2. Click "Check It!" to analyze the recipe
3. View the categorized results and total risk score

## Customization

Edit `Food_Map_Levels.xlsx` to add or modify food items and their risk levels.

## Deployment

This app can be deployed to Streamlit Cloud for mobile browser access:
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Select the repository and set main file to `app.py`


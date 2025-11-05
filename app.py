"""Streamlit front-end for the recipe allergy checker.
Simplified Google Dino-inspired interface that keeps the UI lightweight.
"""

from __future__ import annotations

import base64
from pathlib import Path
from typing import Dict, List, Tuple

import streamlit as st

from recipe_checker_simple import analyze_recipe, add_food_item, clean_food_item_name


# Page configuration
st.set_page_config(
    page_title="Lily's Recipe Scanner",
    page_icon="🦖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for Google Dino aesthetic
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

    :root {
        --retro-bg-top: #f9e4ca;
        --retro-bg-bottom: #b0766a;
        --retro-text: #3c2e1d;
        --retro-muted: #9d7766;
        --retro-line: #775939;
        --retro-card: rgba(255, 255, 255, 0.92);
        --retro-shadow: rgba(39, 20, 29, 0.18);
        --retro-highlight: #77aba7;
        --retro-highlight-dark: #54858c;
    }

    .stApp {
        background: linear-gradient(180deg, var(--retro-bg-top) 0%, var(--retro-bg-bottom) 100%);
        background-attachment: fixed;
        font-family: 'Press Start 2P', 'Courier New', monospace;
        letter-spacing: 0.35px;
        color: var(--retro-text);
    }

    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image:
            linear-gradient(135deg, rgba(212, 178, 91, 0.08) 0%, rgba(196, 151, 77, 0.08) 100%),
            radial-gradient(circle at 20% 20%, rgba(133, 74, 55, 0.16), transparent 60%),
            radial-gradient(circle at 80% 0%, rgba(71, 95, 92, 0.22), transparent 55%);
        pointer-events: none;
        z-index: -1;
    }

    h1, h2, h3, h4 {
        font-family: 'Press Start 2P', 'Courier New', monospace;
        color: var(--retro-text);
    }

    .hero-banner {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1.5rem;
        margin: 1.5rem auto 2.25rem;
        max-width: 520px;
    }

    .hero-line {
        height: 2px;
        background-color: var(--retro-line);
        flex: 1 1 auto;
        opacity: 0.4;
    }

    .hero-circle {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background-color: var(--retro-card);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 12px 0 var(--retro-shadow);
        border: 3px solid #ddac81;
    }

    .hero-dino {
        width: 80px;
        height: 80px;
        object-fit: contain;
        image-rendering: pixelated;
        image-rendering: -moz-crisp-edges;
        image-rendering: crisp-edges;
        filter: drop-shadow(0 4px 0 rgba(39, 20, 29, 0.18));
    }

    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.8);
        border: 3px solid var(--retro-line);
        border-radius: 18px;
        padding: 1.75rem 1.6rem 1.6rem;
        box-shadow: 12px 12px 0 rgba(39, 20, 29, 0.12);
        backdrop-filter: blur(2px);
    }

    textarea {
        font-family: 'Press Start 2P', 'Courier New', monospace !important;
        font-size: 11px !important;
        background-color: var(--retro-card) !important;
        color: var(--retro-text) !important;
        border: 3px solid var(--retro-line) !important;
        border-radius: 16px !important;
        box-shadow: 8px 8px 0 var(--retro-shadow) !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    textarea:focus {
        border-color: var(--retro-highlight-dark) !important;
        box-shadow: 10px 10px 0 rgba(84, 133, 140, 0.25) !important;
        outline: 3px solid rgba(84, 133, 140, 0.25) !important;
    }

    textarea::placeholder {
        color: var(--retro-muted) !important;
    }

    button[kind="primary"], button[kind="secondary"],
    button.stButton, button[data-testid="baseButton-secondary"],
    button[data-testid="baseButton-primary"] {
        font-family: 'Press Start 2P', 'Courier New', monospace !important;
        font-size: 11px !important;
        border-radius: 12px;
        border: 3px solid var(--retro-line);
        box-shadow: 6px 6px 0 var(--retro-shadow);
        padding: 0.75rem 1.2rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease, background-color 0.2s ease;
        width: 100%;
        min-width: 0;
    }

    /* Ensure buttons stay side-by-side on mobile */
    div[data-testid="stForm"] [data-testid="column"],
    div[data-testid="stForm"] [data-baseweb="column"] {
        display: flex !important;
        flex-direction: row !important;
        gap: 0.5rem !important;
    }

    div[data-testid="stForm"] [data-testid="column"] > div,
    div[data-testid="stForm"] [data-baseweb="column"] > div {
        flex: 1 1 0 !important;
        min-width: 0 !important;
        width: auto !important;
    }

    @media (max-width: 768px) {
        div[data-testid="stForm"] [data-testid="column"],
        div[data-testid="stForm"] [data-baseweb="column"] {
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 0.5rem !important;
        }
        
        div[data-testid="stForm"] [data-testid="column"] > div,
        div[data-testid="stForm"] [data-baseweb="column"] > div {
            flex: 1 1 0 !important;
            min-width: 0 !important;
            max-width: none !important;
        }

        button[kind="primary"], button[kind="secondary"],
        button[data-baseweb="button"] {
            font-size: 10px;
            padding: 0.6rem 0.8rem;
        }
    }

    button[kind="primary"], button[data-testid="baseButton-primary"] {
        background-color: #54858c !important;
        border-color: #54858c !important;
        color: #ffffff !important;
    }

    button[kind="primary"] *, button[data-testid="baseButton-primary"] *,
    button[kind="primary"] p, button[data-testid="baseButton-primary"] p {
        color: #ffffff !important;
    }

    button[kind="secondary"], button[data-testid="baseButton-secondary"] {
        background-color: #54858c !important;
        color: #ffffff !important;
        border-color: #54858c !important;
    }

    button[kind="secondary"] *, button[data-testid="baseButton-secondary"] *,
    button[kind="secondary"] p, button[data-testid="baseButton-secondary"] p {
        color: #ffffff !important;
    }

    div[data-testid="stForm"] button {
        background-color: #54858c !important;
        color: #ffffff !important;
        border-color: #54858c !important;
    }

    div[data-testid="stForm"] button[data-baseweb="button"] {
        background-color: #54858c !important;
        color: #ffffff !important;
    }

    div[data-testid="stForm"] button[data-baseweb="button"][kind="secondary"],
    div[data-testid="stForm"] button[kind="secondary"] {
        background-color: #54858c !important;
        color: #ffffff !important;
        border-color: #54858c !important;
    }

    div[data-testid="stForm"] button *,
    div[data-testid="stForm"] button p,
    div[data-testid="stForm"] button span,
    div[data-testid="stForm"] button div {
        color: inherit !important;
    }

    div[data-testid="stForm"] button[data-baseweb="button"][kind="secondary"] *,
    div[data-testid="stForm"] button[data-baseweb="button"][kind="secondary"] p,
    div[data-testid="stForm"] button[data-baseweb="button"][kind="secondary"] span,
    div[data-testid="stForm"] button[kind="secondary"] *,
    div[data-testid="stForm"] button[kind="secondary"] p,
    div[data-testid="stForm"] button[kind="secondary"] span {
        color: #ffffff !important;
    }

    /* Force all button text to be visible */
    button[data-baseweb="button"] {
        background-color: #54858c !important;
    }
    
    button[data-baseweb="button"][kind="secondary"] {
        background-color: #54858c !important;
        color: #ffffff !important;
    }
    
    button[data-baseweb="button"] p,
    button[data-baseweb="button"] span,
    button[data-baseweb="button"] div {
        color: #ffffff !important;
    }
    
    button[data-baseweb="button"][kind="secondary"] p,
    button[data-baseweb="button"][kind="secondary"] span,
    button[data-baseweb="button"][kind="secondary"] div {
        color: #ffffff !important;
    }

    button[kind="primary"]:hover, button[kind="secondary"]:hover,
    button[data-testid="baseButton-primary"]:hover,
    button[data-testid="baseButton-secondary"]:hover,
    div[data-testid="stForm"] button:hover {
        transform: translate(-2px, -2px);
        box-shadow: 9px 9px 0 var(--retro-shadow);
    }

    button[kind="primary"]:active, button[kind="secondary"]:active,
    button[data-testid="baseButton-primary"]:active,
    button[data-testid="baseButton-secondary"]:active,
    div[data-testid="stForm"] button:active {
        transform: translate(1px, 1px);
        box-shadow: 4px 4px 0 var(--retro-shadow);
    }

    .stAlert {
        border-radius: 16px;
        border: 3px solid #54858c;
        background-color: #54858c;
        box-shadow: 6px 6px 0 rgba(39, 20, 29, 0.12);
    }

    .stAlert > div,
    .stAlert *,
    .stAlert p,
    .stAlert span,
    .stAlert div {
        font-size: 12px;
        color: #ffffff !important;
    }

    .stSuccess,
    .stWarning,
    .stError,
    .stInfo {
        border-radius: 16px;
        border: 3px solid #54858c !important;
        background-color: #54858c !important;
        box-shadow: 6px 6px 0 rgba(39, 20, 29, 0.12);
    }

    .stSuccess > div,
    .stWarning > div,
    .stError > div,
    .stInfo > div,
    .stSuccess *,
    .stWarning *,
    .stError *,
    .stInfo * {
        color: #ffffff !important;
    }

    .stSuccess > div {
        border-left: 6px solid #77aba7;
    }

    .stWarning > div {
        border-left: 6px solid #d35b2b;
    }

    .stError > div {
        border-left: 6px solid #c64639;
    }

    .stInfo > div {
        border-left: 6px solid #54858c;
    }

    .stMetric {
        background: rgba(255, 255, 255, 0.82);
        border: 3px solid var(--retro-line);
        border-radius: 16px;
        box-shadow: 8px 8px 0 rgba(39, 20, 29, 0.12);
        padding: 1rem 1.25rem;
        color: var(--retro-text) !important;
    }

    .stMetricValue,
    .stMetricValue *,
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] *,
    [data-testid="stMetricValue"] p,
    [data-testid="stMetricValue"] span,
    [data-testid="stMetricValue"] div {
        color: var(--retro-text) !important;
    }

    .stMetricLabel,
    .stMetricLabel *,
    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] *,
    [data-testid="stMetricLabel"] p,
    [data-testid="stMetricLabel"] span,
    [data-testid="stMetricLabel"] div {
        color: var(--retro-muted) !important;
    }

    div[data-testid="stMetric"],
    div[data-testid="stMetric"] *,
    div[data-testid="stMetric"] > div,
    div[data-testid="stMetric"] > div > div,
    div[data-testid="stMetric"] > div > div > p,
    div[data-testid="stMetric"] > div > div > span,
    div[data-testid="stMetric"] > div > div > div {
        color: var(--retro-text) !important;
    }

    /* Override any white text that might be set */
    div[data-testid="stMetric"] p,
    div[data-testid="stMetric"] span,
    div[data-testid="stMetric"] div,
    div[data-testid="stMetric"] h1,
    div[data-testid="stMetric"] h2,
    div[data-testid="stMetric"] h3,
    div[data-testid="stMetric"] h4 {
        color: var(--retro-text) !important;
    }

    .dino-divider {
        height: 14px;
        background-image: linear-gradient(90deg, var(--retro-line) 0, var(--retro-line) 24px, transparent 24px, transparent 40px);
        background-size: 40px 14px;
        opacity: 0.3;
        margin-top: 2.5rem;
    }

    /* Mobile-friendly expander styling */
    [data-testid="stExpander"] {
        background-color: transparent !important;
    }

    [data-testid="stExpander"] > details {
        background-color: transparent !important;
    }

    [data-testid="stExpander"] > details > summary {
        font-family: 'Press Start 2P', 'Courier New', monospace !important;
        font-size: 10px !important;
        padding: 0.75rem 1rem !important;
        background-color: var(--retro-card) !important;
        border: 2px solid var(--retro-line) !important;
        border-radius: 12px !important;
        box-shadow: 4px 4px 0 var(--retro-shadow) !important;
        margin-bottom: 0.5rem !important;
        color: var(--retro-text) !important;
        cursor: pointer !important;
    }

    [data-testid="stExpander"] > details > summary:hover {
        background-color: rgba(255, 255, 255, 0.95) !important;
    }

    [data-testid="stExpander"] > details[open] > summary {
        border-radius: 12px 12px 0 0 !important;
        margin-bottom: 0 !important;
    }

    [data-testid="stExpander"] > details > div {
        padding: 0.75rem 1rem !important;
        background-color: rgba(255, 255, 255, 0.8) !important;
        border: 2px solid var(--retro-line) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
        margin-bottom: 0.75rem !important;
        color: var(--retro-text) !important;
    }

    [data-testid="stExpander"] > details > div ul {
        margin: 0 !important;
        padding-left: 1.25rem !important;
        color: var(--retro-text) !important;
    }

    [data-testid="stExpander"] > details > div li {
        margin-bottom: 0.5rem !important;
        font-size: 11px !important;
        line-height: 1.8 !important;
        color: var(--retro-text) !important;
    }

    [data-testid="stExpander"] > details > div p,
    [data-testid="stExpander"] > details > div * {
        color: var(--retro-text) !important;
        font-size: 11px !important;
    }

    [data-testid="stExpander"] > details > div strong {
        font-size: 11px !important;
    }

    @media (max-width: 768px) {
        [data-testid="stExpander"] > details > summary {
            font-size: 9px !important;
            padding: 0.6rem 0.8rem !important;
        }

        [data-testid="stExpander"] > details > div {
            padding: 0.6rem 0.8rem !important;
        }

        [data-testid="stExpander"] > details > div li {
            font-size: 10px !important;
        }

        [data-testid="stExpander"] > details > div p,
        [data-testid="stExpander"] > details > div * {
            font-size: 10px !important;
        }
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Load T-Rex image
DINO_IMAGE_PATH = Path(__file__).with_name("pngegg.png")
DINO_IMAGE_B64: str | None = None
try:
    if DINO_IMAGE_PATH.exists():
        image_bytes = DINO_IMAGE_PATH.read_bytes()
        DINO_IMAGE_B64 = base64.b64encode(image_bytes).decode()
except Exception:
    DINO_IMAGE_B64 = None


LEVEL_ORDER: Tuple[int, ...] = (3, 2, 1, 0)
LEVEL_LABELS: Dict[int, str] = {
    3: "🔴 Never",
    2: "❌ Avoid",
    1: "🟡 Moderation",
    0: "🟢 Safe",
}
def build_results_markdown(categorized: Dict[int, List[Tuple[str, Dict[str, str]]]]) -> str:
    """Create a markdown summary grouped by risk level."""
    lines: List[str] = []

    any_items = False
    for level in LEVEL_ORDER:
        items = categorized.get(level, [])
        if not items:
            continue
        any_items = True
        header = LEVEL_LABELS[level]
        lines.append(f"### {header}")
        for food_item, info in items:
            cleaned_name = clean_food_item_name(food_item).title()
            bullet = f"- **{cleaned_name}**"
            if info.get("count", 0) > 1:
                bullet += f" ×{info['count']}"
            if info.get("notes"):
                bullet += f" — {info['notes']}"
            lines.append(bullet)
        lines.append("")

    if not any_items:
        lines.append("No flagged ingredients detected.")

    return "\n".join(lines)


def build_all_ingredients_cards(all_ingredients: Dict[str, Dict]) -> Tuple[Dict[str, Dict], List[str]]:
    """Display ingredients as cards with status badges. Returns ingredients dict and list of unknown ingredients."""
    if not all_ingredients:
        st.info("No ingredients detected in the recipe.")
        return {}, []
    
    st.markdown("### All Ingredients")
    
    # Status color mapping
    status_colors = {
        "❓ Unknown": "#9d7766",
        "🔴 Never": "#c64639",
        "❌ Avoid": "#d35b2b",
        "🟡 Moderation": "#d4a574",
        "🟢 Safe": "#77aba7",
    }
    
    unknown_ingredients = []
    
    for ingredient, info in sorted(all_ingredients.items()):
        matched = info.get('matched', False)
        level = info.get('level')
        notes = info.get('notes', '')
        
        # Determine status
        if matched:
            if level is not None:
                status = LEVEL_LABELS.get(level, f"Level {level}")
            else:
                status = "🟢 Safe"
        else:
            status = "❓ Unknown"
            unknown_ingredients.append(ingredient)
        
        color = status_colors.get(status, "#9d7766")
        
        # Create card using markdown with custom styling
        card_html = f"""
        <div style="
            background-color: rgba(255, 255, 255, 0.9);
            border: 2px solid {color};
            border-radius: 12px;
            padding: 0.75rem 1rem;
            margin-bottom: 0.75rem;
            box-shadow: 4px 4px 0 rgba(39, 20, 29, 0.12);
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <strong style="font-size: 12px; color: var(--retro-text);">{ingredient.title()}</strong>
                <span style="
                    background-color: {color};
                    color: white;
                    padding: 0.25rem 0.5rem;
                    border-radius: 8px;
                    font-size: 9px;
                    font-weight: bold;
                ">{status}</span>
            </div>
            {f'<div style="font-size: 10px; color: var(--retro-muted);">{notes if notes else ("Not in food map" if not matched else "")}</div>' if (notes or not matched) else ''}
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
    
    return all_ingredients, unknown_ingredients


# Main application
# Hero banner with T-Rex image
if DINO_IMAGE_B64:
    dino_img_src = f"data:image/png;base64,{DINO_IMAGE_B64}"
    dino_html = f'<img src="{dino_img_src}" alt="T-Rex" class="hero-dino">'
else:
    dino_html = '<span class="hero-dino" style="font-size: 62px;">🦖</span>'

st.markdown(
    f"""
    <div class="hero-banner">
        <div class="hero-line"></div>
        <div class="hero-circle">
            {dino_html}
        </div>
        <div class="hero-line"></div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("recipe_form", clear_on_submit=False):
    recipe_text = st.text_area(
        "Recipe",
        height=220,
        placeholder="Paste your recipe here...\nExample:\n2 cups rice\n1 lb chicken\n3 cloves garlic\n2 tbsp butter"
    )
    run_scan = st.form_submit_button("Check It!", use_container_width=True)

if 'scan_results' not in st.session_state:
    st.session_state.scan_results = None
if 'recipe_text_state' not in st.session_state:
    st.session_state.recipe_text_state = ""

if run_scan:
    if not recipe_text.strip():
        st.warning("Please enter a recipe before running the scan.")
        st.session_state.scan_results = None
    else:
        results = analyze_recipe(recipe_text, excel_path="Food_Map_Levels.xlsx")
        st.session_state.scan_results = results
        st.session_state.recipe_text_state = recipe_text

# Display results if they exist in session state
if st.session_state.scan_results:
    results = st.session_state.scan_results
    
    if "error" in results:
        st.error(results["error"])
    else:
        categorized = results.get("categorized", {})
        total_score = results.get("total_score", 0)
        all_ingredients = results.get("all_ingredients", {})

        st.metric("Total Risk Score", str(total_score))

        st.divider()
        
        all_ingredients_dict, unknown_ingredients = build_all_ingredients_cards(all_ingredients)
        
        if unknown_ingredients:
            st.divider()
            st.markdown("### Categorize Unknown Ingredients")
            st.markdown("Select unknown ingredients and assign them to a risk category:")
            
            cols = st.columns(2)
            checkbox_states = {}
            
            for i, ingredient in enumerate(sorted(unknown_ingredients)):
                with cols[i % 2]:
                    checkbox_states[ingredient] = st.checkbox(ingredient.title(), key=f"unknown_{ingredient}")
            
            selected_ingredients = [ing for ing, selected in checkbox_states.items() if selected]
            
            if selected_ingredients:
                st.markdown("**Assign category:**")
                category_cols = st.columns(4)
                
                with category_cols[0]:
                    if st.button("🟢 Safe", key="btn_safe", use_container_width=True):
                        added_count = 0
                        for ingredient in selected_ingredients:
                            if add_food_item("Food_Map_Levels.xlsx", ingredient, 0):
                                added_count += 1
                        if added_count > 0:
                            st.success(f"Added {added_count} ingredient(s) as Safe!")
                            results = analyze_recipe(st.session_state.recipe_text_state, excel_path="Food_Map_Levels.xlsx")
                            st.session_state.scan_results = results
                            st.rerun()
                
                with category_cols[1]:
                    if st.button("🟡 Moderation", key="btn_mod", use_container_width=True):
                        added_count = 0
                        for ingredient in selected_ingredients:
                            if add_food_item("Food_Map_Levels.xlsx", ingredient, 1):
                                added_count += 1
                        if added_count > 0:
                            st.success(f"Added {added_count} ingredient(s) as Moderation!")
                            results = analyze_recipe(st.session_state.recipe_text_state, excel_path="Food_Map_Levels.xlsx")
                            st.session_state.scan_results = results
                            st.rerun()
                
                with category_cols[2]:
                    if st.button("❌ Avoid", key="btn_avoid", use_container_width=True):
                        added_count = 0
                        for ingredient in selected_ingredients:
                            if add_food_item("Food_Map_Levels.xlsx", ingredient, 2):
                                added_count += 1
                        if added_count > 0:
                            st.success(f"Added {added_count} ingredient(s) as Avoid!")
                            results = analyze_recipe(st.session_state.recipe_text_state, excel_path="Food_Map_Levels.xlsx")
                            st.session_state.scan_results = results
                            st.rerun()
                
                with category_cols[3]:
                    if st.button("🔴 Never", key="btn_never", use_container_width=True):
                        added_count = 0
                        for ingredient in selected_ingredients:
                            if add_food_item("Food_Map_Levels.xlsx", ingredient, 3):
                                added_count += 1
                        if added_count > 0:
                            st.success(f"Added {added_count} ingredient(s) as Never!")
                            results = analyze_recipe(st.session_state.recipe_text_state, excel_path="Food_Map_Levels.xlsx")
                            st.session_state.scan_results = results
                            st.rerun()
        
        st.divider()
        st.markdown(build_results_markdown(categorized))
        st.markdown("<div class='dino-divider'></div>", unsafe_allow_html=True)


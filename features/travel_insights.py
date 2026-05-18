import random

# =====================================================
# TRAVEL INSIGHTS ENGINE
# =====================================================

def generate_travel_insights(style):

    insights = {

        "Weather Score": round(
            random.uniform(7, 10),
            1
        ),

        "Budget Friendliness": round(
            random.uniform(6, 10),
            1
        ),

        "Safety Score": round(
            random.uniform(7, 10),
            1
        ),

        "Adventure Level": round(
            random.uniform(5, 10),
            1
        ),

        "Family Friendly": round(
            random.uniform(6, 10),
            1
        )
    }

    # STYLE BASED IMPROVEMENTS

    if style == "Adventure":

        insights["Adventure Level"] = 9.5

    elif style == "Family":

        insights["Family Friendly"] = 9.5

    elif style == "Relaxation":

        insights["Weather Score"] = 9.2

    return insights
import json
from pathlib import Path
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Harbin Global Buddy",
    page_icon="❄️",
    layout="wide"
)


# ============================================================
# LOAD CAMPUS DATA
# ============================================================

DATA_FILE = Path(__file__).resolve().parent / "data" / "campus_data.json"


@st.cache_data
def load_campus_data():
    if not DATA_FILE.exists():
        return None

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError:
        st.error("❌ campus_data.json contains invalid JSON.")
        return None


data = load_campus_data()


# ============================================================
# HEADER
# ============================================================

st.title("❄️ Harbin Global Buddy — Campus Onboarding & Survival Hub")

st.caption(
    "A digital companion for international students navigating "
    "campus life, winter survival, and dining."
)


# ============================================================
# CHECK DATA
# ============================================================

if not data:
    st.error(
        f"❌ Could not load the campus data.\n\n"
        f"Expected file:\n`{DATA_FILE}`\n\n"
        "Please make sure `data/campus_data.json` exists."
    )
    st.stop()


# ============================================================
# MAIN TABS
# ============================================================

tab_check, tab_winter, tab_dining, tab_cards, tab_faq = st.tabs(
    [
        "📋 Day 1–7 Checklist",
        "🧊 Sub-Zero Winter Guide",
        "🍜 Dining & Halal",
        "🗣️ Visual Flashcards",
        "❓ Campus FAQ"
    ]
)


# ============================================================
# TAB 1 — CHECKLIST
# ============================================================

with tab_check:

    st.subheader("Arrival Compliance & Registration Tracker")

    st.write(
        "Complete these important tasks during your first week "
        "on campus."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.checkbox(
            "Step 1: Police Registration (住宿登记) within 24 hours"
        )

        st.checkbox(
            "Step 2: Collect Physical Campus Smart Card (一卡通)"
        )

        st.checkbox(
            "Step 3: Buy SIM card (China Mobile/Unicom) with passport"
        )

        st.checkbox(
            "Step 4: Activate Alipay & WeChat Pay"
        )

    with col2:

        st.checkbox(
            "Step 5: Schedule mandatory Health Check (出入境体检)"
        )

        st.checkbox(
            "Step 6: Convert X1 Visa to Foreigner Residence Permit (居留许可)"
        )

        st.checkbox(
            "Step 7: Join official faculty WeChat groups"
        )

        st.checkbox(
            "Step 8: Connect to Campus Wi-Fi using Student ID"
        )


# ============================================================
# TAB 2 — WINTER SURVIVAL
# ============================================================

with tab_winter:

    st.subheader("🧊 Surviving Harbin at -25°C")

    st.write(
        "Practical tips for staying warm, safe, and comfortable "
        "during Harbin's extreme winter."
    )

    survival_tips = data.get("survival_tips", [])

    if survival_tips:

        for tip in survival_tips:

            category = tip.get("category", "Winter Tip")
            description = tip.get("tip", "")

            with st.expander(f"📌 {category}"):

                st.write(description)

    else:

        st.info("No winter survival tips available.")


# ============================================================
# TAB 3 — DINING & HALAL
# ============================================================

with tab_dining:

    st.subheader("🍜 Campus Canteens & Operating Hours")

    filter_halal = st.toggle(
        "☪️ Show Halal Certified Only"
    )

    dining_halls = data.get("dining_halls", [])

    if dining_halls:

        for canteen in dining_halls:

            is_halal = canteen.get("halal", False)

            # Hide non-halal locations if filter is enabled
            if filter_halal and not is_halal:
                continue

            name = canteen.get("name", "Unknown Canteen")
            hours = canteen.get("hours", "Not available")
            recommendation = canteen.get(
                "recommendation",
                "Not available"
            )

            with st.container(border=True):

                st.markdown(f"### {name}")

                if is_halal:
                    st.success("✅ Halal Certified")
                else:
                    st.info("ℹ️ Standard Canteen")

                st.write(f"⏰ **Hours:** {hours}")

                st.write(
                    f"🍲 **Must Try:** {recommendation}"
                )

    else:

        st.info("No dining information available.")


# ============================================================
# TAB 4 — VISUAL FLASHCARDS
# ============================================================

with tab_cards:

    st.subheader("🗣️ Show-to-Driver / Show-to-Chef Flashcards")

    st.write(
        "Show these cards directly on your phone when ordering "
        "food or traveling."
    )

    flashcards = data.get("flashcards", [])

    if flashcards:

        for card in flashcards:

            chinese = card.get("chinese", "")
            pinyin = card.get("pinyin", "")
            english = card.get("english", "")

            # Each flashcard gets its own bordered container
            with st.container(border=True):

                # Large Chinese phrase
                st.markdown(
                    f"# {chinese}"
                )

                # Pinyin
                st.markdown(
                    f"### {pinyin}"
                )

                # English meaning
                st.markdown(
                    f"**Meaning:** {english}"
                )

    else:

        st.info("No flashcards available.")


# ============================================================
# TAB 5 — FAQ
# ============================================================

with tab_faq:

    st.subheader("❓ Frequently Asked Questions")


    # FAQ 1
    with st.expander(
        "💵 Can I use cash or international credit cards on campus?"
    ):

        st.markdown(
            """
            Cash is accepted by law, but cashiers may not always
            have change available.

            Foreign credit cards may not work directly at campus
            canteens. Linking your international card to Alipay or
            WeChat Pay can make everyday payments easier.
            """
        )


    # FAQ 2
    with st.expander(
        "🏥 What should I do if I get sick during the weekend?"
    ):

        st.markdown(
            """
            Visit the Campus Hospital for minor symptoms or the
            appropriate university-affiliated hospital for emergencies.

            Always carry your passport and student insurance information.
            """
        )


    # FAQ 3
    with st.expander(
        "⚡ How do I recharge electricity for my dorm?"
    ):

        st.markdown(
            """
            Use the university WeChat mini-program or the self-service
            smart-card kiosks located in your dormitory lobby.
            """
        )
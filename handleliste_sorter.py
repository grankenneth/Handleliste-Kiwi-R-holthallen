import streamlit as st
from fuzzywuzzy import fuzz
from fpdf import FPDF

# Standard rekkefølge basert på Kiwi Råholthallen
standard_rekkefolge = [
    "Frukt", "Grønnsaker", "Salater", "Brød", "Kylling", "Svinekjøtt", "Oksekjøtt", "Biff", "Kjøttdeig",
    "Kjøttpålegg", "Pølser", "Ost", "Egg", "Ferdigretter", "Baguetter", "Knekkebrød", "Taco", "Asiatisk mat",
    "Syltetøy", "Skjokoladepålegg", "Ris", "Pasta", "Ketchup", "Sennep", "Oljer", "Sauser", "Supper", "Krydder",
    "Hermetikk", "Meieriprodukter", "Fryste rundstykker", "Frossenpizza", "Frosne hvitløksbrød", "Kaffe/te",
    "Bakevarer", "Kaker", "Kjeks", "Desserter", "Frokostblanding", "Vaskemidler", "Dyremat", "Brødposer",
    "Aluminiumsfolie", "Plastfolie", "Engangsbestikk og tallerkener", "Is", "Bind og tamponger", "Lyspærer",
    "Godteri", "Såper", "Deodorant", "Tannkrem", "Papir", "Saft og juice", "Pommes frites", "Fryst kjøtt",
    "Fryste grønnsaker", "Fryst fisk", "Øl", "Brus", "Potetgull", "Snacks", "Skjokolade", "Klær", "Vitaminer",
    "Batterier"
]

# Synonym mapping
synonyms = {
    "Melk": "Meieriprodukter",
    "Yoghurt": "Meieriprodukter",
    "Juice": "Saft og juice",
    "Pølsebrød": "Brød",
    "Gelatin": "Bakevarer",
    "Brettet": "Papir",
    "Tørkepapir": "Papir",
    "Tannbørste": "Tannkrem"
}

# Function to match item to standard list
def match_item(item):
    item_lower = item.lower()
    # Check synonyms
    for key, value in synonyms.items():
        if item_lower == key.lower():
            return value
    # Fuzzy match
    for standard_item in standard_rekkefolge:
        if fuzz.partial_ratio(item_lower, standard_item.lower()) >= 80:
            return standard_item
    return None

# PDF export function
def export_to_pdf(sorted_list, unmatched_list):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Sortert Handleliste", ln=True, align='L')
    pdf.ln(5)
    for item in sorted_list:
        pdf.cell(200, 10, txt=f"- {item}", ln=True, align='L')
    if unmatched_list:
        pdf.ln(10)
        pdf.cell(200, 10, txt="Ikke gjenkjente varer:", ln=True, align='L')
        pdf.ln(5)
        for item in unmatched_list:
            pdf.cell(200, 10, txt=f"- {item}", ln=True, align='L')
    pdf.output("sortert_handleliste.pdf")

# Streamlit UI
st.title("Kiwi Handleliste Sortering")
user_input = st.text_area("Lim inn handlelisten din (én vare per linje):")

if st.button("Sorter handleliste"):
    items = [line.strip() for line in user_input.split("\n") if line.strip()]
    matched = {}
    unmatched = []

    for item in items:
        match = match_item(item)
        if match:
            matched[item] = match
        else:
            unmatched.append(item)

    # Sort according to standard order
    sorted_items = []
    for standard_item in standard_rekkefolge:
        for original, matched_item in matched.items():
            if matched_item == standard_item:
                sorted_items.append(original)

    st.subheader("✅ Sortert handleliste:")
    for item in sorted_items:
        st.write(f"- {item}")

    if unmatched:
        st.subheader("⚠️ Ikke gjenkjente varer:")
        for item in unmatched:
            st.write(f"- {item}")

    if st.button("Last ned som PDF"):
        export_to_pdf(sorted_items, unmatched)
        with open("sortert_handleliste.pdf", "rb") as f:
            st.download_button("📄 Last ned PDF", f, file_name="sortert_handleliste.pdf")

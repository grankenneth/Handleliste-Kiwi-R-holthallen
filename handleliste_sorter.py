
import streamlit as st
from fuzzywuzzy import process
from fpdf import FPDF

# Rekkefølge i Kiwi Råholthallen
category_order = [
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

# Synonymer
synonyms = {
    "Melk": "Meieriprodukter",
    "Smør": "Meieriprodukter",
    "Brelett": "Meieriprodukter",
    "Yoghurt": "Meieriprodukter",
    "Juice": "Saft og juice",
    "Pølsebrød": "Brød",
    "Gelatin": "Bakevarer",
    "Sjokolade": "Skjokolade",
    "Taco-kit": "Taco",
    "Folie": "Aluminiumsfolie",
    "Tørkepapir": "Papir",
    "Tannbørste": "Tannkrem"
}

# Alle kjente varer
all_items = category_order + list(synonyms.keys())

st.title("🛒 Kiwi Handleliste-sortering")
st.write("Lim inn handlelisten din nedenfor. Appen sorterer varene etter rekkefølgen i Kiwi Råholthallen og viser kategori.")

user_input = st.text_area("Handleliste (én vare per linje)")
if st.button("Sorter handleliste"):
    raw_items = [item.strip() for item in user_input.split("\n") if item.strip()]
    sorted_items = []
    unmatched_items = []

    for item in raw_items:
        match, score = process.extractOne(item, all_items)
        if score >= 80:
            category = synonyms.get(match, match)
            sorted_items.append((item, category))
        else:
            unmatched_items.append(item)

    sorted_items.sort(key=lambda x: category_order.index(x[1]) if x[1] in category_order else 999)

    st.subheader("✅ Sortert handleliste")
    for item, category in sorted_items:
        st.write(f"- {item} → *{category}*")

    if unmatched_items:
        st.subheader("⚠️ Ikke gjenkjente varer")
        for item in unmatched_items:
            st.write(f"- {item}")

    if st.button("Last ned som PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Sortert handleliste", ln=True)
        for item, category in sorted_items:
            pdf.cell(200, 10, txt=f"{item} → {category}", ln=True)
        if unmatched_items:
            pdf.cell(200, 10, txt="Ikke gjenkjente varer:", ln=True)
            for item in unmatched_items:
                pdf.cell(200, 10, txt=f"- {item}", ln=True)
        pdf.output("handleliste.pdf")
        with open("handleliste.pdf", "rb") as f:
            st.download_button("📄 Last ned PDF", f, file_name="handleliste.pdf")

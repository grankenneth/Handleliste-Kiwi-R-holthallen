
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

# Utvidet synonymliste
synonyms = {
    # Meieriprodukter
    "Melk": "Meieriprodukter", "Smør": "Meieriprodukter", "Brelett": "Meieriprodukter",
    "Yoghurt": "Meieriprodukter", "Fløte": "Meieriprodukter", "Rømme": "Meieriprodukter",
    # Brus og drikke
    "Villa Farris": "Brus", "Farris": "Brus", "Cola": "Brus", "Coca Cola": "Brus",
    "Pepsi": "Brus", "Pepsi Max": "Brus", "Fanta": "Brus", "Solo": "Brus", "Sprite": "Brus",
    "Mozell": "Brus", "Urge": "Brus", "Red Bull": "Brus", "Battery": "Brus", "Monster": "Brus",
    "Burn": "Brus", "Capri-Sun": "Brus", "Bonaqua": "Brus", "Imsdal": "Brus", "Olden": "Brus",
    # Saft og juice
    "Juice": "Saft og juice", "Appelsinjuice": "Saft og juice", "Eplejuice": "Saft og juice",
    # Brød og bakst
    "Pølsebrød": "Brød", "Hamburgerbrød": "Brød", "Rundstykker": "Brød", "Baguette": "Brød",
    "Kneipp": "Brød", "Polarbrød": "Brød", "Lomper": "Brød", "Tortilla": "Brød",
    # Frysevarer
    "Grandiosa": "Frossenpizza", "Pizza": "Frossenpizza", "Fiskepinner": "Fryst fisk",
    "Laks": "Fryst fisk", "Torsk": "Fryst fisk",
    # Snacks og godteri
    "Potetgull": "Potetgull", "Chips": "Potetgull", "Sørlandschips": "Potetgull",
    "Smash": "Snacks", "Stratos": "Skjokolade", "Kvikk Lunsj": "Skjokolade",
    "Melkesjokolade": "Skjokolade", "Non Stop": "Skjokolade",
    # Husholdning
    "Tørkepapir": "Papir", "Dopapir": "Papir", "Zalo": "Vaskemidler", "Jif": "Vaskemidler",
    "Folie": "Aluminiumsfolie", "Bakepapir": "Aluminiumsfolie"
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

    # Lagre PDF til en bytes-buffer
    import io
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    st.download_button(
        label="📄 Last ned PDF",
        data=pdf_buffer,
        file_name="handleliste.pdf",
        mime="application/pdf"
    )

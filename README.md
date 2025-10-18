# Kiwi Handleliste Sortering

Dette er en Streamlit-app som sorterer handlelisten din etter rekkefølgen i Kiwi Råholthallen.

## Funksjoner
- Case-insensitiv matching
- Fuzzy matching med 80 % terskel
- Synonym-støtte (f.eks. "Melk" → "Meieriprodukter")
- Viser ikke-gjenkjente varer
- Eksport til PDF

## Slik publiserer du på Streamlit Cloud

1. **Opprett GitHub-repo**
   - Gå til [GitHub](https://github.com) og opprett et nytt offentlig repo
   - Last opp følgende filer:
     - `handleliste_sorter.py`
     - `requirements.txt`
     - `README.md`

2. **Publiser på Streamlit Cloud**
   - Gå til [Streamlit Cloud](https://streamlit.io/cloud)
   - Logg inn med GitHub
   - Trykk "New app"
   - Velg repoet du nettopp opprettet
   - Sett `Main file path` til `handleliste_sorter.py`
   - Trykk "Deploy"

3. **Bruk appen**
   - Lim inn handlelisten din
   - Trykk "Sorter handleliste"
   - Last ned PDF hvis ønskelig


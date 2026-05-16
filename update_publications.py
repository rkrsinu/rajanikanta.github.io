from scholarly import scholarly
import json

SCHOLAR_ID = "H2VrG5gAAAAJ"

print("Fetching author...")

author = scholarly.search_author_id(SCHOLAR_ID)

author = scholarly.fill(author)

publications = []

for i, pub in enumerate(author['publications']):

    try:

        print(f"Fetching publication {i+1}")

        filled_pub = scholarly.fill(pub)

        bib = filled_pub['bib']

        title = bib.get('title', '')

        authors = bib.get('author', '')

        year = bib.get('pub_year', '')

        journal = (
            bib.get('journal')
            or bib.get('conference')
            or bib.get('booktitle')
            or ''
        )

        pub_url = filled_pub.get('pub_url', '#')

        publications.append({

            "year": int(year) if year else 0,
            "title": title,
            "authors": authors,
            "journal": journal,
            "link": pub_url,
            "image": "default.jpg"

        })

    except Exception as e:

        print("Error fetching publication:", e)

publications.sort(
    key=lambda x: x["year"],
    reverse=True
)

with open("publications.json", "w", encoding="utf-8") as f:

    json.dump(
        publications,
        f,
        indent=2,
        ensure_ascii=False
    )

print("publications.json updated successfully")
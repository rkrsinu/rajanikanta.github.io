from scholarly import scholarly
import json

SCHOLAR_ID = "H2VrG5gAAAAJ"

author = scholarly.search_author_id(SCHOLAR_ID)

author = scholarly.fill(author)

publications = []

for pub in author['publications']:

    try:

        filled_pub = scholarly.fill(pub)

        bib = filled_pub['bib']

        title = bib.get('title', '')

        authors = bib.get('author', '')

        year = bib.get('pub_year', '')

        journal = bib.get('journal', bib.get('conference', ''))

        publications.append({

            "year": int(year) if year else 0,
            "title": title,
            "authors": authors,
            "journal": journal,
            "link": filled_pub.get('pub_url', '#'),
            "image": "default.jpg"

        })

    except Exception as e:

        print("Error:", e)

with open("publications.json", "w", encoding="utf-8") as f:

    json.dump(publications, f, indent=2, ensure_ascii=False)

print("publications.json updated")
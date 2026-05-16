from scholarly import scholarly
import json
import os
import time

# ==========================================
# GOOGLE SCHOLAR ID
# ==========================================

SCHOLAR_ID = "H2VrG5gAAAAJ"

# ==========================================
# CREATE IMAGES FOLDER
# ==========================================

os.makedirs("images", exist_ok=True)

# ==========================================
# CHECK DEFAULT IMAGE
# ==========================================

default_image = "images/default.jpg"

if not os.path.exists(default_image):

    print("\nWARNING:")
    print("Please add:")
    print("images/default.jpg\n")

# ==========================================
# FETCH AUTHOR
# ==========================================

print("\nFetching Google Scholar profile...\n")

author = scholarly.search_author_id(SCHOLAR_ID)

author = scholarly.fill(author)

print("Author Found:", author["name"])

# ==========================================
# TEMP PUBLICATIONS
# ==========================================

temp_publications = []

# ==========================================
# FETCH PUBLICATIONS
# ==========================================

for pub in author['publications']:

    try:

        filled_pub = scholarly.fill(pub)

        bib = filled_pub['bib']

        title = bib.get(
            'title',
            'No Title'
        )

        authors = bib.get(
            'author',
            'Unknown Authors'
        )

        year = bib.get(
            'pub_year',
            '0'
        )

        journal = (
            bib.get('journal')
            or bib.get('conference')
            or bib.get('booktitle')
            or 'Unknown Journal'
        )

        # ==================================
        # SKIP CHEMRXIV
        # ==================================

        if "ChemRxiv" in journal:

            print(f"\nSkipping ChemRxiv paper:")
            print(title)

            continue

        # ==================================
        # JOURNAL DETAILS
        # ==================================

        volume = bib.get('volume', '')

        issue = (
            bib.get('number')
            or bib.get('issue')
            or ''
        )

        pages = bib.get('pages', '')

        journal_info = journal

        if volume:

            journal_info += f" {volume}"

        if issue:

            journal_info += f" ({issue})"

        if pages:

            journal_info += f", {pages}"

        pub_url = filled_pub.get(
            'pub_url',
            '#'
        )

        # ==================================
        # STORE TEMP DATA
        # ==================================

        temp_publications.append({

            "year": int(year)
            if year else 0,

            "title": title,

            "authors": authors,

            "journal": journal_info,

            "link": pub_url

        })

        print("\nFetched:")
        print(title)

        time.sleep(1)

    except Exception as e:

        print("\nError:")
        print(e)

# ==========================================
# SORT BY YEAR ASCENDING
# OLDEST FIRST
# ==========================================

temp_publications.sort(
    key=lambda x: x["year"]
)

# ==========================================
# FINAL PUBLICATIONS
# ==========================================

publications = []

# ==========================================
# ASSIGN IMAGE NUMBERS
# ==========================================

for idx, pub in enumerate(temp_publications):

    image_number = idx + 1

    manual_image = (
        f"images/pub_{image_number}.jpg"
    )

    if os.path.exists(manual_image):

        image_path = manual_image

    else:

        image_path = "images/default.jpg"

    publications.append({

        "year": pub["year"],

        "title": pub["title"],

        "authors": pub["authors"],

        "journal": pub["journal"],

        "link": pub["link"],

        "image": image_path

    })

# ==========================================
# SAVE JSON
# ==========================================

with open(
    "publications.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        publications,
        f,
        indent=2,
        ensure_ascii=False
    )

# ==========================================
# FINISHED
# ==========================================

print("\n====================================")
print("publications.json updated successfully")
print("====================================")
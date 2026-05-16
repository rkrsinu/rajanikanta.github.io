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
# FETCH GOOGLE SCHOLAR PROFILE
# ==========================================

print("\nFetching Google Scholar profile...\n")

author = scholarly.search_author_id(SCHOLAR_ID)

author = scholarly.fill(author)

print("Author Found:", author["name"])

# ==========================================
# PUBLICATIONS LIST
# ==========================================

publications = []

# ==========================================
# LOOP OVER PAPERS
# ==========================================

for idx, pub in enumerate(author['publications']):

    print("\n====================================")
    print(f"Processing Paper {idx+1}")
    print("====================================")

    try:

        # ----------------------------------
        # FETCH FULL PUBLICATION DETAILS
        # ----------------------------------

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

        pub_url = filled_pub.get(
            'pub_url',
            '#'
        )

        # ----------------------------------
        # MANUAL TOC IMAGE CHECK
        # ----------------------------------

        manual_image = f"images/pub_{idx+1}.jpg"

        if os.path.exists(manual_image):

            image_path = manual_image

            print("\nTOC Image Found:")
            print(manual_image)

        else:

            image_path = "images/default.jpg"

            print("\nUsing Default Image")

        # ----------------------------------
        # PRINT INFO
        # ----------------------------------

        print("\nTitle:")
        print(title)

        print("\nYear:")
        print(year)

        print("\nJournal:")
        print(journal)

        print("\nLink:")
        print(pub_url)

        # ----------------------------------
        # STORE DATA
        # ----------------------------------

        publications.append({

            "year": int(year)
            if year else 0,

            "title": title,

            "authors": authors,

            "journal": journal,

            "link": pub_url,

            "image": image_path

        })

        # ----------------------------------
        # SMALL DELAY
        # ----------------------------------

        time.sleep(1)

    except Exception as e:

        print("\nError Fetching Publication:")
        print(e)

# ==========================================
# SORT BY YEAR DESCENDING
# ==========================================

publications.sort(
    key=lambda x: x["year"],
    reverse=True
)

# ==========================================
# SAVE JSON FILE
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
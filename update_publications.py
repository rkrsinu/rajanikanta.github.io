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
# FETCH AUTHOR PROFILE
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

        # ----------------------------------
        # BASIC INFO
        # ----------------------------------

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

        # ==================================
        # SKIP CHEMRXIV
        # ==================================

        if (
            "chemrxiv" in pub_url.lower()
            or
            "ChemRxiv" in journal
        ):

            print("\nSkipping ChemRxiv:")
            print(title)

            continue

        # ----------------------------------
        # JOURNAL DETAILS
        # ----------------------------------

        volume = bib.get(
            'volume',
            ''
        )

        issue = (
            bib.get('number')
            or bib.get('issue')
            or ''
        )

        pages = bib.get(
            'pages',
            ''
        )

        journal_info = journal

        if volume:

            journal_info += f" {volume}"

        if issue:

            journal_info += f" ({issue})"

        if pages:

            journal_info += f", {pages}"

        # ----------------------------------
        # STORE TEMP DATA
        # ----------------------------------

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
# SORT:
# NEWEST FIRST
# ==========================================

temp_publications.sort(

    key=lambda x: (
        x["year"],
        x["title"]
    ),

    reverse=True

)

# ==========================================
# TOTAL PAPERS
# ==========================================

total_papers = len(temp_publications)

# ==========================================
# FINAL PUBLICATIONS
# ==========================================

publications = []

# ==========================================
# ASSIGN WEBSITE NUMBER
# ==========================================

for idx, pub in enumerate(temp_publications):

    # ----------------------------------
    # WEBSITE NUMBER
    # ----------------------------------

    publication_number = (
        total_papers - idx
    )

    # ----------------------------------
    # IMAGE FILES
    # ----------------------------------

    jpg_file = (
        f"images/pub_{publication_number}.jpg"
    )

    jpeg_file = (
        f"images/pub_{publication_number}.jpeg"
    )

    png_file = (
        f"images/pub_{publication_number}.png"
    )

    # ----------------------------------
    # CHECK IMAGE EXISTS
    # ----------------------------------

    if os.path.exists(jpg_file):

        image_path = jpg_file

    elif os.path.exists(jpeg_file):

        image_path = jpeg_file

    elif os.path.exists(png_file):

        image_path = png_file

    else:

        image_path = "images/default.jpg"

    print(
        f"\nPublication No: {publication_number}"
    )

    print(
        f"Assigned Image: {image_path}"
    )

    # ----------------------------------
    # STORE FINAL DATA
    # ----------------------------------

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
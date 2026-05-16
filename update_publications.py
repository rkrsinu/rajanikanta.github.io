from scholarly import scholarly
import json
import os
import time
import re

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

        # ==================================
        # DOI IMAGE NAME
        # ==================================

        doi_match = re.search(
            r'10\.\S+',
            pub_url
        )

        image_path = "images/default.jpg"

        if doi_match:

            doi = doi_match.group(0)

            safe_doi = (
                doi
                .replace("/", "_")
                .replace(".", "_")
            )

            jpg_file = (
                f"images/{safe_doi}.jpg"
            )

            jpeg_file = (
                f"images/{safe_doi}.jpeg"
            )

            png_file = (
                f"images/{safe_doi}.png"
            )

            if os.path.exists(jpg_file):

                image_path = jpg_file

            elif os.path.exists(jpeg_file):

                image_path = jpeg_file

            elif os.path.exists(png_file):

                image_path = png_file

            print("\nDOI:")
            print(doi)

            print("Assigned Image:")
            print(image_path)

        # ----------------------------------
        # STORE DATA
        # ----------------------------------

        temp_publications.append({

            "year": int(year)
            if year else 0,

            "title": title,

            "authors": authors,

            "journal": journal_info,

            "link": pub_url,

            "image": image_path

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
# SAVE JSON
# ==========================================

with open(
    "publications.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        temp_publications,
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
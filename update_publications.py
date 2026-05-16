from scholarly import scholarly
import requests
from bs4 import BeautifulSoup
import json
import os

SCHOLAR_ID = "H2VrG5gAAAAJ"

os.makedirs("images", exist_ok=True)

author = scholarly.search_author_id(SCHOLAR_ID)

author = scholarly.fill(author)

publications = []

for idx, pub in enumerate(author['publications']):

    try:

        filled_pub = scholarly.fill(pub)

        bib = filled_pub['bib']

        title = bib.get('title', '')

        authors = bib.get('author', '')

        year = bib.get('pub_year', '')

        journal = (
            bib.get('journal')
            or bib.get('conference')
            or ''
        )

        pub_url = filled_pub.get('pub_url', '#')

        image_path = "images/default.jpg"

        try:

            headers = {
                "User-Agent":
                "Mozilla/5.0"
            }

            response = requests.get(
                pub_url,
                headers=headers,
                timeout=15
            )

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            og_image = soup.find(
                "meta",
                property="og:image"
            )

            if og_image:

                image_url = og_image.get("content")

                img_data = requests.get(
                    image_url,
                    headers=headers
                ).content

                image_filename = f"images/pub_{idx+1}.jpg"

                with open(image_filename, "wb") as f:

                    f.write(img_data)

                image_path = image_filename

                print(
                    f"Downloaded image for paper {idx+1}"
                )

        except Exception as e:

            print("Image extraction failed:", e)

        publications.append({

            "year": int(year) if year else 0,
            "title": title,
            "authors": authors,
            "journal": journal,
            "link": pub_url,
            "image": image_path

        })

    except Exception as e:

        print("Paper fetch error:", e)

publications.sort(
    key=lambda x: x["year"],
    reverse=True
)

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

print("Finished updating publications")
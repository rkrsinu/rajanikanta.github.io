async function loadPublications() {

    const response = await fetch('publications.json');

    let data = await response.json();

    // =====================================
    // SORT BY YEAR DESCENDING
    // =====================================

    data.sort((a, b) => b.year - a.year);

    const container =
        document.getElementById(
            "publicationsContainer"
        );

    // =====================================
    // GROUP BY YEAR
    // =====================================

    const grouped = {};

    data.forEach(pub => {

        if (!grouped[pub.year]) {

            grouped[pub.year] = [];

        }

        grouped[pub.year].push(pub);

    });

    // =====================================
    // TOTAL PUBLICATIONS
    // =====================================

    let totalPapers = data.length;

    Object.keys(grouped)
        .sort((a, b) => b - a)
        .forEach(year => {

            // =====================================
            // YEAR TITLE
            // =====================================

            const yearTitle =
                document.createElement("h2");

            yearTitle.className =
                "pub-year";

            yearTitle.innerHTML =
                `[ ${year} ]`;

            container.appendChild(
                yearTitle
            );

            // =====================================
            // EACH PAPER
            // =====================================

            grouped[year].forEach(pub => {

                const div =
                    document.createElement("div");

                div.className =
                    "publication-card";

                div.innerHTML = `

                <div class="publication-grid">

                    <!-- LEFT -->

                    <div class="publication-left">

                        <div class="publication-title">

                            ${totalPapers}. "${pub.title}"

                        </div>

                        <div class="publication-authors">

                            ${pub.authors}

                        </div>

                        <div class="publication-journal">

                            ${pub.journal}

                        </div>

                        <a href="${pub.link}"
                           target="_blank"
                           class="paper-link">

                            View Paper

                        </a>

                    </div>

                    <!-- RIGHT -->

                    <div class="publication-right">

                        <img src="${pub.image}"
                             alt="TOC Image"
                             class="publication-image">

                    </div>

                </div>

                `;

                container.appendChild(div);

                totalPapers--;

            });

        });

}

loadPublications();
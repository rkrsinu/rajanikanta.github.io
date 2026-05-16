async function loadPublications() {

    const response = await fetch('publications.json');

    let data = await response.json();

    // Sort newest first
    data.sort((a, b) => {

        if (b.year !== a.year) {
            return b.year - a.year;
        }

        return 0;
    });

    const container = document.getElementById(
        "publicationsContainer"
    );

    // ======================================
    // GROUP BY YEAR
    // ======================================

    const grouped = {};

    data.forEach(pub => {

        if (!grouped[pub.year]) {

            grouped[pub.year] = [];

        }

        grouped[pub.year].push(pub);

    });

    // ======================================
    // TOTAL PAPER COUNT
    // ======================================

    let totalPapers = data.length;

    // ======================================
    // LOOP YEARS
    // ======================================

    Object.keys(grouped)
        .sort((a, b) => b - a)
        .forEach(year => {

            // -------------------------------
            // YEAR TITLE
            // -------------------------------

            const yearTitle = document.createElement("h2");

            yearTitle.innerHTML = `[ ${year} ]`;

            yearTitle.style.margin =
                "50px 0 30px 0";

            yearTitle.style.color = "red";

            yearTitle.style.textAlign =
                "center";

            yearTitle.style.fontSize =
                "2.2rem";

            container.appendChild(yearTitle);

            // -------------------------------
            // PAPERS
            // -------------------------------

            grouped[year].forEach(pub => {

                const div =
                    document.createElement("div");

                div.className = "pub-card";

                div.innerHTML = `

                <div class="pub-grid">

                    <div>

                        <div class="pub-title">

                            ${totalPapers}. 
                            "${pub.title}"

                        </div>

                        <div class="pub-authors">

                            ${pub.authors}

                        </div>

                        <div class="pub-journal">

                            <i>${pub.journal}</i>

                        </div>

                        <br>

                        <a href="${pub.link}" 
                        target="_blank">

                            View Paper

                        </a>

                    </div>

                    <div>

                        <img 
                        src="${pub.image}" 
                        class="toc-img"

                        onerror="
                        this.src='images/default.jpg'
                        ">

                    </div>

                </div>

                `;

                container.appendChild(div);

                totalPapers--;

            });

        });

}

loadPublications();
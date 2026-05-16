async function loadPublications() {

    const response = await fetch('publications.json');

    let data = await response.json();

    // Sort publications by year descending
    data.sort((a, b) => b.year - a.year);

    const container = document.getElementById("publicationsContainer");

    // Group by year
    const grouped = {};

    data.forEach(pub => {

        if (!grouped[pub.year]) {
            grouped[pub.year] = [];
        }

        grouped[pub.year].push(pub);

    });

    // Total publication count
    let totalPapers = data.length;

    Object.keys(grouped)
        .sort((a, b) => b - a)
        .forEach(year => {

            // Year Heading
            const yearTitle = document.createElement("h2");

            yearTitle.innerHTML = `[ ${year} ]`;

            yearTitle.style.margin = "50px 0 30px 0";
            yearTitle.style.color = "red";
            yearTitle.style.textAlign = "center";
            yearTitle.style.fontSize = "2.2rem";

            container.appendChild(yearTitle);

            grouped[year].forEach(pub => {

                const div = document.createElement("div");

                div.className = "pub-card";

                div.innerHTML = `

                <div class="pub-grid">

                    <div>

                        <div class="pub-title">

                            ${totalPapers}. "${pub.title}"

                        </div>

                        <div class="pub-authors">

                            ${pub.authors}

                        </div>

                        <div class="pub-journal">

                            ${pub.journal}

                        </div>

                        <a href="${pub.link}" target="_blank">
                            View Paper
                        </a>

                    </div>

                    <div>

                        <img src="${pub.image}" class="toc-img">

                    </div>

                </div>

                `;

                container.appendChild(div);

                totalPapers--;

            });

        });

}

loadPublications();
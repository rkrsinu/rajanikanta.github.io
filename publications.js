async function loadPublications(){

    const response = await fetch('publications.json');

    const data = await response.json();

    const container = document.getElementById("publicationsContainer");

    const grouped = {};

    data.forEach(pub => {

        if(!grouped[pub.year]){

            grouped[pub.year] = [];

        }

        grouped[pub.year].push(pub);

    });

    Object.keys(grouped)
    .sort((a,b)=>b-a)
    .forEach(year => {

        const yearTitle = document.createElement("h2");

        yearTitle.innerHTML = `[ ${year} ]`;

        yearTitle.style.margin = "50px 0 30px 0";

        yearTitle.style.color = "red";

        container.appendChild(yearTitle);

        grouped[year].forEach(pub => {

            const div = document.createElement("div");

            div.className = "pub-card";

            div.innerHTML = `

            <div class="pub-title">
                ${pub.title}
            </div>

            <div>
                ${pub.authors}
            </div>

            <div class="pub-journal">
                ${pub.journal}
            </div>

            <a href="${pub.link}" target="_blank">
                View Paper
            </a>

            `;

            container.appendChild(div);

        });

    });

}

loadPublications();
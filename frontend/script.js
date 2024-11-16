async function fetchData(location) {
    // Fetch the entire countries.json file
    const response = await fetch('data/countries.json');
    const allData = await response.json();

    // Check if the location exists in the data
    const users = allData[location.toLowerCase()];
    
    if (!users) {
        console.log("No data found for " + location);
        return;
    }

    // Clear existing table data
    const tableBody = document.getElementById('user-data');
    tableBody.innerHTML = "";

    // Loop through the user data and append rows to the table
    users.forEach(user => {
        const row = document.createElement('tr');

        // Add country flag
        const flagCell = document.createElement('td');
        const flagImg = document.createElement('img');
        flagImg.src = `https://flagcdn.com/16x12/${location.toLowerCase()}.png`;  // Dynamic country flag
        flagImg.alt = location;
        flagCell.appendChild(flagImg);
        row.appendChild(flagCell);

        // Add user data
        const usernameCell = document.createElement('td');
        usernameCell.textContent = user.username;
        row.appendChild(usernameCell);

        const nameCell = document.createElement('td');
        nameCell.textContent = user.name;
        row.appendChild(nameCell);

        const followersCell = document.createElement('td');
        followersCell.textContent = user.followers;
        row.appendChild(followersCell);

        const contributionsCell = document.createElement('td');
        contributionsCell.textContent = user.contributions;
        row.appendChild(contributionsCell);

        const topLanguageCell = document.createElement('td');
        topLanguageCell.textContent = user.top_language;
        row.appendChild(topLanguageCell);

        // Append the row to the table body
        tableBody.appendChild(row);
    });
}

function loadCountryData() {
    const selectElement = document.getElementById('country-select');
    const selectedCountry = selectElement.value;
    fetchData(selectedCountry);
}

// Initial data load for default country (India)
window.onload = function() {
    loadCountryData();
};

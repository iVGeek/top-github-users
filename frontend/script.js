async function fetchData(location) {
    const response = await fetch(`../data/${location.toLowerCase()}.json`);
    const users = await response.json();

    const table = `
        <table>
            <thead>
                <tr>
                    <th>Country</th>
                    <th>Username</th>
                    <th>Name</th>
                    <th>Followers</th>
                    <th>Contributions</th>
                    <th>Top Language</th>
                </tr>
            </thead>
            <tbody>
                ${users.map(user => `
                    <tr>
                        <td>
                            <img src="https://flagcdn.com/w40/${location.toLowerCase().replace(' ', '-')}.png" alt="Flag">
                            ${location}
                        </td>
                        <td>${user.username}</td>
                        <td>${user.name || 'N/A'}</td>
                        <td>${user.followers}</td>
                        <td>${user.contributions}</td>
                        <td>${user.top_language || 'N/A'}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
    document.getElementById('app').innerHTML = table;
}

fetchData("india"); // Example country

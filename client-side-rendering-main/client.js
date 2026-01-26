/* Den här funktionen hämtar data från en given URL. */
async function fetchData(url) {
  try {
    // Hämtar med fetch(), await används för att vänta på svaret
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    // Parsar JSON-svaret så att det blir ett JavaScript-objekt
    const data = await response.json();  
    return data;
  } catch (error) {
    console.error('Error fetching data:', error);
    return null;
  }
}

/* Här är hårdkodad exempeldata.
Samma data finns på denna URL: 
https://raw.githubusercontent.com/martinloman/demo-json-files/refs/heads/main/planets.json
 */
let data = {
  "planets": [
    {
      "id": 1,
      "name": "Mercury",
      "distance_from_sun": "57.9 million km",
      "has_rings": false
    },
    {
      "id": 2,
      "name": "Venus",
      "distance_from_sun": "108.2 million km",
      "has_rings": false
    },
    {
      "id": 3,
      "name": "Earth",
      "distance_from_sun": "149.6 million km",
      "has_rings": false
    },
    {
      "id": 4,
      "name": "Mars",
      "distance_from_sun": "227.9 million km",
      "has_rings": false
    },
    {
      "id": 5,
      "name": "Jupiter",
      "distance_from_sun": "778.5 million km",
      "has_rings": true
    }
  ]
};

/**  
    Funktion för att rendera planetdata i DOM:en. 
*/
async function renderPlanets() {
  const container = document.getElementById('container');
  // 1. Hämta data från URL (avkommentera raden nedan för att använda fetch)
  // data = await fetchData('https://raw.githubusercontent.com/martinloman/demo-json-files/refs/heads/main/planets.json');
  
  container.innerHTML = ''; // Rensa tidigare innehåll

  // loopar igenom varje planet i data och skapar en div för att visa informationen
  data.planets.forEach(planet => {
    const planetDiv = document.createElement('div');

    // den här raden lägger till en CSS-klass baserat på om planeten har ringar eller inte
    planetDiv.classList.add('planet')
    if (planet.has_rings) {
      planetDiv.classList.add('has-rings');
    }

    //3. Se koden ovan. 
    // Lägg till en css-klass om planeten heter Earth. 
    // Styla den så att den ser annorlunda ut i styles.css
    // Använd en villkorssats för att lägga till klassen 'earth' om planet.name är 'Earth'
    
    // 2. Översätt texten till svenska
    planetDiv.innerHTML = `
      <h2>${planet.name}</h2>
      <p><strong>Distance from Sun:</strong> ${planet.distance_from_sun}</p>
      <p><strong>Has Rings:</strong> ${planet.has_rings ? 'Yes' : 'No'}</p>
    `;
    
    container.appendChild(planetDiv);
  });
}

// Väntar på att DOM:en är laddad innan vi lägger till eventlyssnare på knappen
document.addEventListener('DOMContentLoaded', () => {
  const fetchBtn = document.getElementById('fetchBtn');
  // Kör renderPlanets när knappen klickas
  fetchBtn.addEventListener('click', renderPlanets);
});

//4. Kan du anpassa koden så att den kan visa annan data från någon av 
//   de andra JSON-filerna i samma GitHub-repo? 
//   Se filerna här: https://github.com/martinloman/demo-json-files/tree/main
//   Öppna filerna på GitHub och klicka på "Raw"-knappen för att få URL:en till json-datan.
//   Studera sedan json-strukturen och anpassa renderingskoden ovan för att visa den datan istället.
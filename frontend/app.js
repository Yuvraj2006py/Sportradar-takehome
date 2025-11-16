const sportSelect = document.getElementById("sportFilter");
const dateInput = document.getElementById("dateFilter");
const searchInput = document.getElementById("searchFilter");
const statusEl = document.getElementById("status");
const eventsContainer = document.getElementById("eventsContainer");
const filterButton = document.getElementById("filterButton");
const resetButton = document.getElementById("resetButton");

const API = {
    sports: "/sports",
    events: "/events"
};

filterButton.addEventListener("click", () => loadEvents());
resetButton.addEventListener("click", () => {
    sportSelect.value = "";
    dateInput.value = "";
    searchInput.value = "";
    loadEvents();
});

searchInput.addEventListener("keydown", event => {
    if (event.key === "Enter") {
        event.preventDefault();
        loadEvents();
    }
});

async function init() {
    await Promise.all([populateSports(), loadEvents()]);
}

async function populateSports() {
    try {
        const response = await fetch(API.sports);
        if (!response.ok) {
            throw new Error("Unable to load sports");
        }
        const data = await response.json();
        data.sports
            .sort((a, b) => a.name.localeCompare(b.name))
            .forEach(sport => {
                const option = document.createElement("option");
                option.value = sport.id;
                option.textContent = sport.name;
                sportSelect.appendChild(option);
            });
    } catch (error) {
        setStatus(error.message, "error");
    }
}

async function loadEvents() {
    setStatus("Loading events…");
    eventsContainer.innerHTML = "";

    const params = new URLSearchParams();
    if (sportSelect.value) params.set("sport_id", sportSelect.value);
    if (dateInput.value) params.set("date", dateInput.value);
    const searchText = searchInput.value.trim();
    if (searchText) params.set("search", searchText);

    const url = params.toString() ? `${API.events}?${params}` : API.events;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error("Unable to load events");
        }
        const data = await response.json();
        renderEvents(data.events || []);
    } catch (error) {
        setStatus(error.message, "error");
    }
}

function renderEvents(events) {
    if (!events.length) {
        setStatus("No events match your filters. Try adjusting them.", "info");
        eventsContainer.innerHTML = `<div class="empty-state">No events to display.</div>`;
        return;
    }

    const fragment = document.createDocumentFragment();
    events.forEach(event => {
        const card = document.createElement("article");
        card.className = "event-card";

        card.innerHTML = `
            <div class="pill">${event.sport?.name ?? "Unknown sport"}</div>
            <h3>${event.description || "Untitled event"}</h3>
            <div class="event-meta">
                <span>Kickoff: ${formatDate(event.start_datetime)}</span>
                <span>Venue: ${event.venue?.name ?? "TBD"} (${event.venue?.city ?? ""} ${event.venue?.country ?? ""})</span>
            </div>
            <div class="teams" aria-label="Teams"></div>
        `;

        const teamsContainer = card.querySelector(".teams");
        if (event.teams?.length) {
            event.teams.forEach(team => {
                const teamChip = document.createElement("span");
                teamChip.textContent = team.name;
                teamsContainer.appendChild(teamChip);
            });
        } else {
            teamsContainer.textContent = "Teams TBD";
        }

        fragment.appendChild(card);
    });

    eventsContainer.innerHTML = "";
    eventsContainer.appendChild(fragment);
    setStatus(`Showing ${events.length} event${events.length === 1 ? "" : "s"}.`);
}

function formatDate(value) {
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) {
        return value;
    }

    return new Intl.DateTimeFormat(undefined, {
        weekday: "short",
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit"
    }).format(date);
}

function setStatus(message, variant = "info") {
    statusEl.textContent = message;
    statusEl.dataset.variant = variant;
}

init();

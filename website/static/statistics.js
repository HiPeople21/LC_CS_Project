const barForm = document.querySelector("#bar-form");
const barSelectHoliday = document.querySelector("#bar-select-holiday");
const barChart = document.querySelector("#barchart");

async function changeBar() {
    const holiday = barSelectHoliday.value;
    barChart.src = `/static/charts/bar/${holiday}.html`
}

barForm.addEventListener("submit", async e => {
    e.preventDefault();
    await changeBar(); 
});


const heatmapForm = document.querySelector("#heatmap-form");
const heatmapSelectHoliday = document.querySelector("#heatmap-select-holiday");
const heatmapSelectYear = document.querySelector("#heatmap-select-year");
const heatmapParent = document.querySelector("#heatmap");

const fullDates = [
    "New Year's Day",
    "St Brigid's Day",
    "St Patrick's Day",
    "Easter Monday",
    "May Bank Holiday",
    "June Bank Holiday",
    "August Bank Holiday",
    "October Bank Holiday",
    "Christmas Day",
    "St Stephen's Day"
]

const missingDates = [
    "Easter Monday",
    "October Bank Holiday",
    "Christmas Day",
    "St Stephen's Day"
]

const missingDateOptions = []

for (const date of missingDates) {
    missingDateOptions.push(document.querySelectorAll(`option[value="${date}"]`)[1]);
}

async function changeHeatmap() {
    const holiday = heatmapSelectHoliday.value;
    const year = heatmapSelectYear.value;

    heatmap.src = `/static/charts/heatmap/${holiday}-${year}.html`
}

heatmapForm.addEventListener("submit", async e => {
    e.preventDefault();
    await changeHeatmap(); 
});

heatmapSelectYear.addEventListener("change", e => {
    const year = e.target.value;
    if (year === "2024") {
        if (missingDates.includes(heatmapSelectHoliday.value)) {
            heatmapSelectHoliday.value = fullDates[0];
        }
        for (const option of missingDateOptions) {
            option.disabled = true;
        }
    } else {
        for (const option of missingDateOptions) {
            option.disabled = false;
        }
    }
});
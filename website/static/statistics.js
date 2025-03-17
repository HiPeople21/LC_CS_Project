const barForm = document.querySelector("#bar-form");
const barSelectHoliday = document.querySelector("#bar-select-holiday");
const barChart = document.querySelector("#barchart");

// Changes iframe source to display bar chart
async function changeBar() {
    const holiday = barSelectHoliday.value;
    barChart.src = `/static/charts/bar/${holiday}.html`
}

// Changes bar chart when form is submitted
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

// Changes iframe source to display heatmap
async function changeHeatmap() {
    const holiday = heatmapSelectHoliday.value;
    const year = heatmapSelectYear.value;

    heatmap.src = `/static/charts/heatmap/${holiday}-${year}.html`
}


// Changes heatmap when form is submitted
heatmapForm.addEventListener("submit", async e => {
    e.preventDefault();
    await changeHeatmap();
});


// Disables missing dates for 2024
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
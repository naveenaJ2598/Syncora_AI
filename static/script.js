
// Upload and Analyze Meeting
async function uploadMeeting() {

    const fileInput = document.getElementById("meetingFile");
    const status = document.getElementById("uploadStatus");
    const output = document.getElementById("insightOutput");

    if (fileInput.files.length === 0) {
        status.innerText = "Please select a meeting file.";
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    status.innerText = "Analyzing meeting... Please wait.";
    output.innerText = "";

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Upload failed");
        }

        status.innerText = "Meeting analyzed successfully!";
        output.innerText = data.insights;

        // Refresh meeting history
        await loadMeetings();

    } catch (error) {
        status.innerText = "Error: " + error.message;
    }
}


// Ask Questions About Meeting
async function askQuestion() {

    const questionInput = document.getElementById("question");
    const answerOutput = document.getElementById("answerOutput");

    const question = questionInput.value.trim();

    if (!question) {
        answerOutput.innerText = "Please enter a question.";
        return;
    }

    answerOutput.innerText = "AI is finding the answer...";

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to get answer");
        }

        answerOutput.innerText = data.answer;

    } catch (error) {
        answerOutput.innerText = "Error: " + error.message;
    }
}


// Clear Question and Answer
function clearQuestion() {

    document.getElementById("question").value = "";
    document.getElementById("answerOutput").innerText = "";

}


// Load Meeting History
async function loadMeetings() {

    const historyOutput = document.getElementById("meetingHistory");

    if (!historyOutput) return;

    historyOutput.innerText = "Loading meeting history...";

    try {

        const response = await fetch("/meetings");
        const meetings = await response.json();

        if (!response.ok) {
            throw new Error("Unable to load meeting history");
        }

        historyOutput.innerHTML = "";

        if (meetings.length === 0) {
            historyOutput.innerText = "No meetings uploaded yet.";
            return;
        }

        meetings.forEach(function(meeting) {

            const card = document.createElement("div");
            card.className = "history-card";

            const title = document.createElement("h3");
            title.textContent = meeting.title;

            const date = document.createElement("p");
            date.textContent = "Uploaded: " + meeting.created_at;

            const summary = document.createElement("p");
            summary.textContent = meeting.summary;

            card.appendChild(title);
            card.appendChild(date);
            card.appendChild(summary);

            historyOutput.appendChild(card);

        });

    } catch (error) {

        historyOutput.innerText = "Error: " + error.message;

    }
}


// Load history when dashboard opens
loadMeetings();


function showSection(sectionId) {

    document.querySelectorAll(".feature-page").forEach(function(section) {
        section.classList.remove("active");
    });

    document.getElementById(sectionId).classList.add("active");

    document.getElementById(sectionId).scrollIntoView({
        behavior: "smooth"
    });
}


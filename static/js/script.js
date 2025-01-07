const API_URL = "http://127.0.0.1:5000";

document.getElementById("uploadForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const fileInput = document.getElementById("file");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        // Upload file trước
        const uploadResponse = await fetch(`${API_URL}/upload`, {
            method: "POST",
            body: formData,
        });

        const uploadResult = await uploadResponse.json();
        if (!uploadResponse.ok) {
            alert(`Upload Error: ${uploadResult.error}`);
            return;
        }

        // Gọi predict sau khi upload thành công
        const predictResponse = await fetch(`${API_URL}/predict`, {
            method: "POST",
        });

        const predictResult = await predictResponse.json();
        if (predictResponse.ok) {
            alert("Analysis complete. You can download the results.");
            document.getElementById("dashboardLink").style.display = "block";
        } else {
            alert(`Error: ${predictResult.error}`);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An unexpected error occurred. Please try again.");
    }
});
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('resume-form'); // Ensure form is accessed only after the DOM is fully loaded

    form.addEventListener('submit', async function (event) {
        event.preventDefault(); // Prevent the default form submission behavior

        console.log("Form submission intercepted");

        const fileInput = document.getElementById("fileInput");
        const file = fileInput.files[0];

        if (!file) {
            alert("Please select a file before submitting.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file); // Append the file to the FormData object

        const apiKey = 'YOUR_API_KEY'; // Replace with your actual API key

        try {
            const response = await fetch(`http://127.0.0.1:5000/parse_resume/`, {
                method: "POST",
                headers:{
                    "API-Key": "8726d0e9c5b16722a784d7662cba921e793e7ae43f0ef0633976422885dc8fe0"
                },
                body: formData,
                mode: 'cors'
            });

            if (response.ok) {
                const result = await response.json();
                document.getElementById("responseMessage").innerText = `Resume processed successfully. Name: ${result.name}, Email: ${result.email}`;
            } else {
                const errorText = await response.text();
                document.getElementById("responseMessage").innerText = `Error: ${errorText}`;
            }
        } catch (error) {
            console.error("Error:", error);
            document.getElementById("responseMessage").innerText = `An error occurred while uploading the resume.`;
        }
    });
});

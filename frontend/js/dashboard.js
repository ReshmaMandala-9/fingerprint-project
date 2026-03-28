// dashboard.js

const fileInput = document.getElementById("fileInput");
const preview = document.getElementById("preview");
const result = document.getElementById("result");
const results = document.getElementById("results");

// ----------------------
// 🔐 TOKEN & ROLE PROTECTION
// ----------------------
const token = localStorage.getItem("token");
const role = localStorage.getItem("role");

// Redirect if not logged in
if (!token || !role) {
  alert("Please login first");
  window.location.href = "login.html";
}

// Role-based access
if (
  (window.location.pathname.includes("user.html") && role !== "user") ||
  (window.location.pathname.includes("researcher.html") && role !== "researcher")
) {
  alert("Access denied for your role");
  window.location.href = "login.html";
}

// ----------------------
// 🖼 IMAGE PREVIEW + VALIDATION
// ----------------------
if (fileInput) {
  fileInput.onchange = () => {
    const file = fileInput.files[0];
    if (!file) return;

    // File type check
    if (!file.type.startsWith("image/")) {
      alert("Only image files allowed");
      fileInput.value = "";
      return;
    }

    // File size check
    if (file.size > 5 * 1024 * 1024) {
      alert("File size must be < 5MB");
      fileInput.value = "";
      return;
    }

    preview.src = URL.createObjectURL(file);
  };
}

// ----------------------
// 👤 USER PREDICTION
// ----------------------
async function predictUser() {
  const file = fileInput?.files[0];
  if (!file) return alert("Please upload a fingerprint image");

  const fd = new FormData();
  fd.append("file", file);

  result.innerText = "Predicting...";

  try {
    const res = await fetch("http://127.0.0.1:5000/api/predict", {
      method: "POST",
      body: fd,
      headers: {
        "Authorization": "Bearer " + token
      }
    });

    const data = await res.json();

    if (data.error) {
      result.innerText = "Error: " + data.error;
      return;
    }

    if (data.user && data.user.blood_group) {
      result.innerText =
        `Blood Group: ${data.user.blood_group} (Confidence: ${(data.user.confidence * 100).toFixed(2)}%)`;
    } else {
      result.innerText = "Blood Group: No prediction";
    }

  } catch (err) {
    console.error(err);
    result.innerText = "Server error";
  }
}

// ----------------------
// 🧪 RESEARCHER PREDICTION (MULTI-MODEL)
// ----------------------
async function predictResearcher() {
  const file = fileInput?.files[0];
  if (!file) return alert("Please upload a fingerprint image");

  const fd = new FormData();
  fd.append("file", file);

  results.innerHTML = "<li>Processing...</li>";

  try {
    const res = await fetch("http://127.0.0.1:5000/api/predict", {
      method: "POST",
      body: fd,
      headers: {
        "Authorization": "Bearer " + token
      }
    });

    const data = await res.json();

    if (data.error) {
      results.innerHTML = `<li>Error: ${data.error}</li>`;
      return;
    }

    results.innerHTML = "";

    // ✅ MULTI MODEL DISPLAY
    if (data.researcher && typeof data.researcher === "object") {

      for (const [modelName, modelData] of Object.entries(data.researcher)) {

        results.innerHTML += `
          <li style="margin-bottom:10px;">
            <strong>${modelName.toUpperCase()}</strong><br>
            Blood Group: ${modelData.blood_group}<br>
            Confidence: ${(modelData.confidence * 100).toFixed(2)}%
          </li>
        `;

        // Show probabilities
        if (modelData.all_probabilities) {
          results.innerHTML += "<ul>";
          for (const [bg, val] of Object.entries(modelData.all_probabilities)) {
            results.innerHTML += `<li>${bg}: ${(val * 100).toFixed(2)}%</li>`;
          }
          results.innerHTML += "</ul><hr>";
        }
      }

    } else {
      results.innerHTML = "<li>No researcher data available</li>";
    }

  } catch (err) {
    console.error(err);
    results.innerHTML = "<li>Server error</li>";
  }
}

// ----------------------
// 🔗 EVENT BINDING
// ----------------------
document.getElementById("predictUserBtn")?.addEventListener("click", predictUser);
document.getElementById("predictResearcherBtn")?.addEventListener("click", predictResearcher);
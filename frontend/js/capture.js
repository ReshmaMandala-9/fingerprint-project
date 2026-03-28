import { post } from "./api.js";

const fileInput = document.getElementById("fileInput");
const preview = document.getElementById("preview");
const status = document.getElementById("status");

// ----------------------
// 🔐 TOKEN & ROLE PROTECTION
// ----------------------
const token = localStorage.getItem("token");
if (!token) {
  alert("Please login first");
  location.href = "login.html";
}

// ----------------------
// IMAGE PREVIEW + VALIDATION
// ----------------------
if (fileInput) {
  fileInput.onchange = () => {
    const file = fileInput.files[0];
    if (!file) return;

    if (!file.type.startsWith("image/")) {
      alert("Only image files allowed");
      fileInput.value = "";
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      alert("File must be <5MB");
      fileInput.value = "";
      return;
    }

    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";
  };
}

// ----------------------
// UPLOAD & PREDICT
// ----------------------
async function uploadFingerprint() {
  const file = fileInput.files[0];
  if (!file) return alert("Please select a fingerprint image");

  const fd = new FormData();
  fd.append("file", file);

  status.innerText = "Predicting...";

  try {
    const res = await fetch("http://127.0.0.1:5000/api/predict", {
      method: "POST",
      body: fd,
      headers: { "Authorization": "Bearer " + token }
    });
    const data = await res.json();

    status.innerText = data.error ? "Error: " + data.error : "Predicted Blood Group: " + (data.user ?? "No prediction");

  } catch (err) {
    console.error(err);
    status.innerText = "Server error";
  }
}

window.uploadFingerprint = uploadFingerprint;
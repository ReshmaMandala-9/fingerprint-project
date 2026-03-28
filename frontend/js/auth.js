// auth.js
import { post } from "./api.js";

// ----------------------
// 🔍 VALIDATION HELPERS
// ----------------------
function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function isValidAge(age) {
  return !isNaN(age) && age >= 1 && age <= 120;
}

// ----------------------
// 🔑 LOGIN FUNCTION
// ----------------------
async function login() {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  // Validation
  if (!email || !password) {
    alert("All fields are required");
    return;
  }
  if (!isValidEmail(email)) {
    alert("Invalid email format");
    return;
  }

  try {
    // Call backend login endpoint
    const res = await post("/api/login", { email, password });

    if (res.error) {
      alert(res.error);
      return;
    }

    // Store JWT token and user info
    localStorage.setItem("token", res.token || res.access_token); // support both
    localStorage.setItem("role", res.role);
    localStorage.setItem("name", res.name);

    // Redirect based on role
    if (res.role === "user") window.location.href = "user.html";
    else if (res.role === "researcher") window.location.href = "researcher.html";
    else window.location.href = "capture.html";

  } catch (err) {
    console.error("Login error:", err);
    alert("Server error. Try again later.");
  }
}

// ----------------------
// 📝 REGISTER FUNCTION
// ----------------------
async function register() {
  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const gender = document.getElementById("gender").value;
  const age = document.getElementById("age").value;
  const password = document.getElementById("password").value.trim();
  const role = document.getElementById("role").value;

  // Validation
  if (!name || !email || !gender || !age || !password || !role) {
    alert("All fields are required");
    return;
  }
  if (!isValidEmail(email)) {
    alert("Invalid email format");
    return;
  }
  if (!isValidAge(age)) {
    alert("Age must be between 1 and 120");
    return;
  }
  if (password.length < 6) {
    alert("Password must be at least 6 characters");
    return;
  }

  try {
    // Call backend register endpoint
    const res = await post("/api/register", { name, email, gender, age, password, role });

    if (res.error) {
      alert(res.error);
      return;
    }

    alert("Registered Successfully!");
    window.location.href = "login.html";

  } catch (err) {
    console.error("Registration error:", err);
    alert("Server error. Try again later.");
  }
}

// ----------------------
// 🔗 EVENT BINDING
// ----------------------
document.getElementById("loginBtn")?.addEventListener("click", login);
document.getElementById("registerBtn")?.addEventListener("click", register);
export const BASE_URL = "http://127.0.0.1:5000";

// ----------------------
// POST REQUEST
// ----------------------
export async function post(endpoint, data) {
  try {
    const token = localStorage.getItem("token");

    const options = {
      method: "POST",
      headers: {}
    };

    // Handle FormData vs JSON
    if (data instanceof FormData) {
      options.body = data;
    } else {
      options.headers["Content-Type"] = "application/json";
      options.body = JSON.stringify(data);
    }

    // Add token if exists
    if (token) {
      options.headers["Authorization"] = "Bearer " + token;
    }

    const res = await fetch(BASE_URL + endpoint, options);

    if (!res.ok) {
      throw new Error("Server error: " + res.status);
    }

    return await res.json();

  } catch (err) {
    console.error("POST Error:", err);
    return { error: "Request failed. Try again." };
  }
}

// ----------------------
// GET REQUEST
// ----------------------
export async function get(endpoint) {
  try {
    const token = localStorage.getItem("token");

    const options = {
      headers: {}
    };

    if (token) {
      options.headers["Authorization"] = "Bearer " + token;
    }

    const res = await fetch(BASE_URL + endpoint, options);

    if (!res.ok) {
      throw new Error("Server error");
    }

    return await res.json();

  } catch (err) {
    console.error("GET Error:", err);
    return { error: "Request failed" };
  }
}
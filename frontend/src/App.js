import React, { useState } from "react";

function App() {
  const [url, setUrl] = useState("");
  const [shortUrl, setShortUrl] = useState("");

  const handleSubmit = async () => {
    const response = await fetch("http://184.72.211.88:8000/shorten", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ original_url: url }),
    });

    const data = await response.json();
    setShortUrl(data.short_url);
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>URL Shortener</h2>

      <input
        type="text"
        placeholder="Enter URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{ width: "300px", padding: "10px" }}
      />

      <br /><br />

      <button onClick={handleSubmit}>Shorten</button>

      {shortUrl && (
        <div>
          <h3>Short URL:</h3>
          <a href={shortUrl}>{shortUrl}</a>
        </div>
      )}
    </div>
  );
}

export default App;

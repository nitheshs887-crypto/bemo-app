import React, { useState } from "react";

/**
 * Simple phone-shaped UI component that shows output on its "screen".
 * Drop this into your React project and import it wherever needed:
 *
 *   import Phone from "./Phone";
 *   <Phone />
 *
 * Type something in the input, press "Send", and it appears on the phone screen.
 */
export default function Phone() {
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("Hello! Waiting for input...");

  const handleSend = () => {
    if (input.trim() === "") return;
    setOutput(input);
    setInput("");
  };

  return (
    <div style={styles.wrapper}>
      {/* Phone frame */}
      <div style={styles.phone}>
        <div style={styles.notch}></div>
        <div style={styles.screen}>
          <p style={styles.outputText}>{output}</p>
        </div>
        <div style={styles.homeButton}></div>
      </div>

      {/* Controls below the phone */}
      <div style={styles.controls}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type something..."
          style={styles.input}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button onClick={handleSend} style={styles.button}>
          Send
        </button>
      </div>
    </div>
  );
}

const styles = {
  wrapper: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: "20px",
    fontFamily: "sans-serif",
  },
  phone: {
    width: "260px",
    height: "500px",
    backgroundColor: "#1c1c1e",
    borderRadius: "36px",
    padding: "16px",
    boxShadow: "0 10px 30px rgba(0,0,0,0.3)",
    position: "relative",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  notch: {
    width: "80px",
    height: "18px",
    backgroundColor: "#000",
    borderRadius: "10px",
    marginBottom: "10px",
  },
  screen: {
    flex: 1,
    width: "100%",
    backgroundColor: "#fff",
    borderRadius: "20px",
    padding: "16px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    textAlign: "center",
    overflowY: "auto",
  },
  outputText: {
    fontSize: "18px",
    color: "#111",
    wordBreak: "break-word",
  },
  homeButton: {
    width: "40px",
    height: "40px",
    borderRadius: "50%",
    border: "2px solid #555",
    marginTop: "10px",
  },
  controls: {
    display: "flex",
    gap: "10px",
  },
  input: {
    padding: "8px 12px",
    borderRadius: "8px",
    border: "1px solid #ccc",
    fontSize: "14px",
    width: "220px",
  },
  button: {
    padding: "8px 16px",
    borderRadius: "8px",
    border: "none",
    backgroundColor: "#007aff",
    color: "#fff",
    fontSize: "14px",
    cursor: "pointer",
  },
};

import React from "react";

function App() {
  const loginWithGoogle = () => {
    window.location.href = "http://127.0.0.1:5000/api/login/google";
  };

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h1>Login with Google</h1>
      <button onClick={loginWithGoogle}>
        Login
      </button>
    </div>
  );
}

export default App;

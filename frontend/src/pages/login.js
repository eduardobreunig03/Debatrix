import { useState } from "react";
import Link from "next/link";
import cookie from "react-cookies";
const PUBLIC_IP = "54.80.13.110";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault(); // Prevent form from reloading the page
    try {
      const res = await fetch(`http://${PUBLIC_IP}/auth/auth_login/`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }), // Send username and password in the request body
      });

      if (res.ok) {
        const data = await res.json();
        console.log("Received data:", data);
        // Save the token in a cookie
        cookie.save("user_token", data.token, {
          path: "/",
          sameSite: "lax", // Adjust this based on your needs
          secure: false, // Ensure it's true in a production HTTPS environment
        });

        // Redirect to the home page after successful login
        window.location.href = "/home";
      } else {
        // Handle error response (invalid credentials, etc.)
        const errorData = await res.json();
        setErrorMessage(errorData.detail || "Invalid credentials");
      }
    } catch (error) {
      // Handle any network errors
      setErrorMessage("Something went wrong. Please try again.");
    }
  };

  const handleGuestLogin = () => {
    // Simply redirect to the home page as a guest
    window.location.href = "/home";
  };

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="w-[90%] max-w-md h-auto bg-black text-white border border-gray-700 rounded-lg p-6">
        <img
          className="rounded-lg"
          src="/images/mainlogo.png"
          alt="Debatrix Logo"
        />
        <h1 className="text-white text-4xl font-bold text-center mb-6 mt-3">
          Welcome to{" "}
          <span
            className="font-bold text-purple-800"
            style={{ color: "#6F4062" }}
          >
            Debatrix
          </span>
        </h1>
        <p className="text-white text-lg mb-4 text-center">
          Where we discuss worldwide topics with powerful
          <span
            className="font-bold text-purple-800"
            style={{ color: "#6F4062" }}
          >
            AI tools
          </span>
        </p>
        <div className="flex flex-col items-center">
          {errorMessage && <p className="text-red-500 mb-4">{errorMessage}</p>}
          <form onSubmit={handleLogin} className="w-full">
            <input
              placeholder="Username"
              className="w-full mb-4 h-10 rounded-md bg-transparent border border-gray-700 px-4 py-2"
              type="text"
              aria-label="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)} // Controlled input
            />
            <input
              placeholder="Password"
              className="w-full mb-6 h-10 rounded-md bg-transparent border border-gray-700 px-4 py-2"
              type="password"
              aria-label="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)} // Controlled input
            />
            <button className="w-full bg-white text-black font-bold text-lg py-2 rounded-lg mb-4">
              Sign in
            </button>
          </form>
          <p className="text-white text-sm font-bold mb-4">Not a user?</p>
          <Link href="/signup" className="w-full">
            <button className="w-full bg-white text-black font-bold text-lg py-2 rounded-lg mb-4">
              Sign up
            </button>
          </Link>
          {/* Continue as Guest Button */}
          <button
            onClick={handleGuestLogin}
            className="w-full bg-white text-black font-bold text-lg py-2 rounded-lg mb-4"
          >
            Continue as Guest
          </button>
        </div>
      </div>
    </div>
  );
}

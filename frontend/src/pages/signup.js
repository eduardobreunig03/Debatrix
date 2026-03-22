import { useState } from "react";
import Link from "next/link";
const PUBLIC_IP = "54.80.13.110";

export default function SignUp() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleSignUp = async (e) => {
    e.preventDefault(); // Prevent form from reloading the page

    try {
      const res = await fetch(`http://${PUBLIC_IP}/auth/auth_register/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password }), // Send username, email, and password in the request body
      });

      if (res.ok) {
        // Assuming successful signup redirects to login page
        window.location.href = "/login";
      } else {
        // Handle error response (invalid credentials, etc.)
        const errorData = await res.json();

        if (errorData.username) {
          setErrorMessage(errorData.username[0]); // Display the first error for username
        } else if (errorData.email) {
          setErrorMessage(errorData.email[0]); // Display the first error for email
        } else if (errorData.password) {
          setErrorMessage(errorData.password[0]); // Display the first error for password
        } else {
          setErrorMessage("Sign-up failed. Please try again.");
        }
      }
    } catch (error) {
      // Handle any network errors
      setErrorMessage("Something went wrong. Please try again.");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="w-[90%] max-w-md h-auto bg-black text-white border border-gray-700 rounded-lg p-6">
        <img className="rounded-lg" src="/images/mainlogo.png" alt="Main Logo" />
        <h1 className="text-white text-4xl font-bold text-center mb-6 mt-3">
          Welcome to{" "}
          <span className="font-bold text-purple-800" style={{ color: "#6F4062" }}>
            Debatrix
          </span>
        </h1>
        <p className="text-white text-lg mb-4 text-center">
          Join the conversation with powerful
          <span className="font-bold text-purple-800" style={{ color: "#6F4062" }}>
            AI tools
          </span>
        </p>
        <div className="flex flex-col items-center">
          {errorMessage && <p className="text-red-500 mb-4">{errorMessage}</p>}
          <form onSubmit={handleSignUp} className="w-full">
            <input
              placeholder="Username"
              className="w-full mb-4 h-10 rounded-md bg-transparent border border-gray-700 px-4 py-2"
              type="text"
              aria-label="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)} // Controlled input
            />
            <input
              placeholder="Email"
              className="w-full mb-4 h-10 rounded-md bg-transparent border border-gray-700 px-4 py-2"
              type="email"
              aria-label="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)} // Controlled input
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
              Sign up
            </button>
          </form>
          <p className="text-white text-sm font-bold mb-4">
            Already have an account?
          </p>
          <Link href="/login" className="w-full">
            <button className="w-full bg-white text-black font-bold text-lg py-2 rounded-lg">
              Sign in
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}

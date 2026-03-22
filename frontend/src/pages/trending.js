import React, { useState, useEffect } from "react";
import NavBar from "../components/NavBar";
import Debate from "../components/Debate";
import { useRouter } from "next/router";
import Cookies from "js-cookie";

const PUBLIC_IP = "54.80.13.110";

function Trending({ loadingUser, userData }) {
  const [debates, setDebates] = useState([]);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  console.log("userData IN TRENDINNGGGG", userData);

  useEffect(() => {
    const token = Cookies.get("user_token");
    setIsLoggedIn(!!token);
  }, []);

  useEffect(() => {
    const fetchDebates = async () => {
      try {
        console.log("Connecting to API");
        const response = await fetch(
          `http://${PUBLIC_IP}/api/debates/?trending=true`
        );
        if (response.ok) {
          const data = await response.json();
          setDebates(data);
        } else {
          console.error("Failed to fetch debates");
        }
      } catch (error) {
        console.error("Error fetching debates:", error);
      }
    };

    fetchDebates();
  }, []); // Add empty dependency array to avoid infinite loop

  return (
    <div
      className="min-h-screen flex flex-col bg-gray-900 items-center"
      style={{
        backgroundImage: "url(/images/background.jpeg)",
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      <NavBar isLoggedIn={isLoggedIn} />
      <div className="flex-grow w-full p-10">
        <>
          <h2 className="text-white mb-5">All Debates</h2>
          {debates.length > 0 ? (
            debates.map((debate) => (
              <Debate
                key={debate.id}
                data={debate}
                isLoggedIn={isLoggedIn}
                loadingUser={!isLoggedIn}
              />
            ))
          ) : (
            <p className="text-white">No debates available.</p>
          )}
        </>
      </div>
    </div>
  );
}

export default Trending;


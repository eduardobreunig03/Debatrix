import React, { useState, useEffect } from "react";
import NavBar from "../components/NavBar";
import Debate from "../components/Debate";
import Cookies from "js-cookie";
import Link from "next/link";
import { useRouter } from "next/router";
const PUBLIC_IP = "54.80.13.110";

function MainPage() {
  const [data, setData] = useState([]); // Data regarding each debate.
  const [pinnedDebates, setPinnedDebates] = useState([]); // State for pinned debates
  const [loadingUser, setLoadingUser] = useState(true); // Tracks if we are loading in the current user or not
  const [isLoggedIn, setIsLoggedIn] = useState(false); // Checks if a user is logged in or not
  const [userData, setUserData] = useState(null); // Tracks the data of the user that is logged in.

  const router = useRouter();

  const fetchUserProfile = async () => {
    const token = Cookies.get("user_token"); // Getting the user token and seeing if it exists
    if (token) {
      try {
        const response = await fetch(
          `http://${PUBLIC_IP}:8000/auth/user_profile/`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
            credentials: "include",
          }
        );

        if (response.ok) {
          const data = await response.json();
          setUserData(data); // Setting the logged in user data to userData
          setIsLoggedIn(true); // Setting logged in status to true
        } else {
          console.error("Failed to fetch user profile.");
        }
      } catch (error) {
        console.error("Error fetching user profile:", error);
      } finally {
        setLoadingUser(false); // When the user is loaded, we set loading user to false
      }
    } else {
      setLoadingUser(false); // Set to false if no token found
      setIsLoggedIn(false);
    }
  };

  useEffect(() => {
    if (userData === null) {
      fetchUserProfile();
    }
  }, []); // Empty dependency array means this useEffect runs only once

  useEffect(() => {
    const fetchPinnedDebates = async () => {
      const token = Cookies.get("user_token"); // Getting the user token and seeing if it exists
      if (token) {
        try {
          const response = await fetch(
            `http://${PUBLIC_IP}:8000/api/get_pinned_debates/`,
            {
              method: "GET",
              headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
              },
            }
          );

          if (response.ok) {
            const result = await response.json();
            setPinnedDebates(result); // Update with pinned debates data
          } else {
            console.error("Failed to fetch pinned debates.");
          }
        } catch (error) {
          console.error("Error fetching pinned debates:", error);
        }
      }
    };

    // Fetching data for the debates
    const fetchData = async () => {
      try {
        const response = await fetch(`http://${PUBLIC_IP}:8000/api/debates`);
        const result = await response.json();
        setData(result); // Setting the data for the debate.
      } catch (error) {
        console.error("Error fetching debates:", error);
      }
    };

    // Running each function to populate fields
    fetchData();
    fetchPinnedDebates();

    const interval = setInterval(fetchData, 10000); // Ensuring it's constantly updated in case someone creates a new debate while on the website
    return () => clearInterval(interval);
  }, [isLoggedIn]); // Only refetch when login status changes

  // Function to handle debate deletion
  const handleDeleteDebate = (debateId) => {
    setData((prevData) =>
      prevData.filter((debate) => debate.debateId !== debateId)
    );
  };

  // Function for logging out by removing user token
  const handleLogout = () => {
    Cookies.remove("user_token"); // Remove the token cookie
    setIsLoggedIn(false); // Setting logged in to false to prevent authorized features
    setLoadingUser(true);
    router.push("/login"); // Redirect to login page after logout
  };

  // Filter out pinned debates from the regular debates list
  const unpinnedDebates = data.filter(
    (debate) =>
      !pinnedDebates.some((pinned) => pinned.debateId === debate.debateId)
  );

  return (
    <div
      className="min-h-screen flex flex-col bg-gray-900 relative"
      style={{
        backgroundImage: "url(/images/background.jpeg)",
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      {/* Logout Button */}
      {isLoggedIn && (
        <button
          className="absolute top-5 right-5 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition duration-300"
          onClick={handleLogout}
        >
          Log Out
        </button>
      )}

      {/* Navigation Bar takes in loadingUser and also the userData to display the user specific details */}
      <NavBar isLoggedIn={isLoggedIn} />

      <div className="flex justify-center mt-10">
        {/* An unauthorized user cannot make a debate */}
        {!isLoggedIn ? (
          <div className="flex w-full h-10 items-center justify-center">
            <h1 className="text-white">You must log in to create a debate</h1>
          </div>
        ) : (
          <Link href="/createDebate">
            <button className="flex w-full h-10 custom_button">
              <h1 className="text-white">Create Debate</h1>
            </button>
          </Link>
        )}
      </div>

      <div className="m-10 flex-grow">
        {/* Check if the user is logged in */}
        {isLoggedIn ? (
          // If logged in, show loading indicator or debates
          loadingUser ? (
            <div className="flex w-full h-10 items-center justify-center">
              <h1 className="text-white">Loading debates...</h1>
            </div>
          ) : (
            <>
              {/* FOR PINNED DEBATES */}
              {pinnedDebates.length > 0 && (
                <div>
                  <h2 className="text-white mb-5">Pinned Debates</h2>
                  {pinnedDebates.map((debate) => (
                    <Debate
                      key={debate.debateId} // Setting a unique key for the debate
                      data={debate} // All debate data is passed in
                      loadingUser={loadingUser} // Passing in loading user as prop
                      isPinned={true} // Checks if debate is pinned
                      onDelete={handleDeleteDebate} // Passing in delete function for debate so it can update automatically
                      userData={userData} // Passing in current logged in user into debate for conditional rendering of delete button
                    />
                  ))}
                </div>
              )}
              {/* FOR ALL DEBATES */}
              <h2 className="text-white mt-10 mb-5">All Debates</h2>
              {unpinnedDebates.map((debate) => (
                <Debate
                  key={debate.debateId} // Setting a unique key for the debate
                  data={debate} // All debate data is passed in
                  loadingUser={loadingUser} // Passing in loading user as prop
                  isPinned={false} // Checks if debate is pinned
                  onDelete={handleDeleteDebate} // Passing in delete function for debate so it can update automatically
                  userData={userData} // Passing in current logged in user into debate for conditional rendering of delete button
                />
              ))}
            </>
          )
        ) : (
          // If not logged in, still show debates
          <>
            <h2 className="text-white mt-10 mb-5">All Debates</h2>
            {data.length > 0 ? (
              unpinnedDebates.map((debate) => (
                <Debate
                  key={debate.debateId}
                  data={debate}
                  loadingUser={loadingUser}
                  isPinned={false}
                  onDelete={handleDeleteDebate}
                  userData={userData} // Passing in current logged in user into debate for conditional rendering of delete button
                  isLoggedIn={isLoggedIn}
                />
              ))
            ) : (
              // Display no debates available to not confuse the user if nothing shows up.
              <div className="flex w-full h-10 items-center justify-center">
                <h1 className="text-white">No debates available.</h1>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default MainPage;

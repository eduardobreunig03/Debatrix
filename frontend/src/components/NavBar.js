import Image from "next/image";
import Link from "next/link";
import NavBarLink from "./NavBarLink";
import { HomeIcon, EyeIcon, FireIcon } from "@heroicons/react/24/outline";
const PUBLIC_IP = "54.80.13.110";

import Cookies from "js-cookie";
import React, { useState, useEffect } from "react";

export default function NavBar({ isLoggedIn }) {
  const [userData, setUserData] = React.useState(null); // setting the userData to null

  // Fetching the data for the logged in user
  const fetchUserProfile = async () => {
    console.log("Fetching user profile");
    const token = Cookies.get("user_token"); // getting the user token and seeing if it exists
    if (token) {
      try {
        const response = await fetch(
          `http://${PUBLIC_IP}/auth/user_profile/`, // Using the PUBLIC_IP constant
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
          setUserData(data); // setting the logged in user data to userData
        } else {
          console.error("Failed to fetch user profile.");
        }
      } catch (error) {
        console.error("Error fetching user profile:", error);
      }
    }
  };

  useEffect(() => {
    if (userData === null) {
      fetchUserProfile();
    }
  }, []); // Empty dependency array means this useEffect runs only once

  return (
    <div className="w-full bg-black flex justify-center items-center">
      <Link href="/home">
        <img
          className="rounded-lg h-20 w-auto m-3"
          src="/images/mainlogo.png"
          alt="Main Logo"
        />
      </Link>
      <NavBarLink
        text="Home"
        Icon={HomeIcon}
        link="/home"
        userData={userData}
        isLoggedIn={isLoggedIn}
      />
      <NavBarLink
        text="Explore"
        Icon={EyeIcon}
        link="/explore"
        userData={userData}
        isLoggedIn={isLoggedIn}
      />
      <NavBarLink
        text="Trending"
        Icon={FireIcon}
        link="/trending"
        userData={userData}
        isLoggedIn={isLoggedIn}
      />

      {!isLoggedIn ? (
        <Link href="/">
          <button className="ml-10 p-2 bg-gray-500 text-white rounded-lg transform transition-all duration-200 hover:scale-105">
            Log in
          </button>
        </Link>
      ) : (
        <Link href={`/profile/${userData?.id}`}>
          <div className="flex border-2 rounded-full border-white p-2 ml-10 h-15 items-center justify-center blur_background">
            <img
              className="rounded-full h-14 w-14 m-1 object-cover zoom" // Scale effect applied to the image
              src={
                userData?.profile_picture
                  ? `http://${PUBLIC_IP}${userData.profile_picture}` // Updated profile picture URL to use PUBLIC_IP
                  : "/images/defaultProfilePic.png"
              }
              alt="User Profile"
            />
          </div>
        </Link>
      )}
    </div>
  );
}


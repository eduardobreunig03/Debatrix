import {
  ChatBubbleOvalLeftIcon,
  PlusCircleIcon,
  TrashIcon,
} from "@heroicons/react/24/outline"; // Importing default icons outlined

const PUBLIC_IP = "54.80.13.110";

import { PlusCircleIcon as PlusCircleIconSolid } from "@heroicons/react/24/solid"; // Importing default icons full

import { useRouter } from "next/router";
import React, { useState, useEffect } from "react";
import Cookies from "js-cookie";

export default function Debate({
  data,
  loadingUser,
  onDelete,
  isPinned,
  userData,
  isLoggedIn,
}) {
  const [userProfile, setUserProfile] = useState(); // Tracks the information of each user that has posted a debate.
  const [loadingUserProfile, setLoadingUserProfile] = useState(); // tracks the profile being loaded into debate
  const [isFilled, setIsFilled] = useState(isPinned); // State to track filled/unfilled for pinned debates logo
  const [isNavigating, setIsNavigating] = useState(null);
  const [averagePercentage, setAveragePercentage] = useState(0);

  const router = useRouter();

  // Function to truncate the content after 20 words
  const truncateContent = (content) => {
    const words = content.split(" "); // Split content into words
    if (words.length > 40) {
      return words.slice(0, 20).join(" ") + " ..."; // Join the first 20 words and append "..."
    }
    return content; // If it's less than or equal to 20 words, return it as is
  };

  const fetchUserProfile = async () => {
    try {
      const username = data.creatorUserName;
      const url = `http://${PUBLIC_IP}/auth/userprofilebyUsername/${username}/`;
      const response = await fetch(url);
      const result = await response.json();
      setUserProfile(result);
    } catch (error) {
      console.error("Error fetching user profile:", error);
    }
  };

  useEffect(() => {
    if (!userProfile) {
      fetchUserProfile();
    }
    fetchAveragePercentage();
  }, []);

  const handleProfileClick = () => {
    setIsNavigating(true);

    router.push({
      pathname: `/profile/user_profiles`, // Redirect to the user's profile page
      query: {
        username: userProfile.username, // Pushing username of the user who created the debate
        profile_picture: userProfile.profile_picture, // Pushing the profile picture of the user
        profile_bio: userProfile.profile_bio, // Pushing the profile bio of the user
      },
    });
  };

  const handleDebateClick = () => {
    router.push(
      {
        pathname: `/home/${data.debateId}`,
        query: {
          debateId: data.debateId,
          username: data.creatorUserName,
          currentUser: userData?.username,
          title: data.title,
          created_at: data.created_at,
          content: data.content,
          percentage: data.percentage,
          comments: data.comments,
          userProfilePic: userProfile.profile_picture, // Use the profile pic
          loadingUser: loadingUser,
          userProfile: data.userProfile,
          numberComments: data.numberComments,
          currentProfilePic: userData?.profile_picture,
        },
      },
      undefined,
      { shallow: true }
    ); // Set shallow to true
  };

  const handlePlusClick = async (event) => {
    event.stopPropagation(); // Prevent click from bubbling up to debate card
    const newFilledState = !isFilled; // Toggle filled state
    setIsFilled(newFilledState);

    try {
      const token = Cookies.get("user_token");
      if (token) {
        const apiUrl = newFilledState
          ? `http://${PUBLIC_IP}/api/pin_debate`
          : `http://${PUBLIC_IP}/api/unpin_debate`; // Toggle pin/unpin

        const response = await fetch(apiUrl, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            debateId: data.debateId,
          }),
        });

        if (!response.ok) {
          throw new Error(
            `Error ${newFilledState ? "pinning" : "unpinning"} debate: ${
              response.statusText
            }`
          );
        }
        router.reload(); // Reload the page to reflect the change
        const responseData = await response.json();
        console.log(
          `Debate ${newFilledState ? "pinned" : "unpinned"} successfully:`,
          responseData
        );
      } else {
        throw new Error("No user token found");
      }
    } catch (error) {
      console.error(
        `Failed to ${newFilledState ? "pin" : "unpin"} debate:`,
        error.message
      );
    }
  };

  const fetchAveragePercentage = async () => {
    try {
      const response = await fetch(
        `http://${PUBLIC_IP}/api/average_percentage/${data.debateId}/`
      );
      if (response.ok) {
        const result = await response.json();
        setAveragePercentage(result.average_percentage);
      } else {
        console.error(
          "Error fetching average percentage:",
          response.statusText
        );
      }
    } catch (error) {
      console.error("Error fetching average percentage:", error);
    }
  };

  const handleDeleteClick = async (event) => {
    event.stopPropagation();
    const debateId = data.debateId;

    try {
      const response = await fetch(
        `http://${PUBLIC_IP}/api/debates/${debateId}/`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`Error deleting debate: ${response.statusText}`);
      }

      // Call the onDelete prop to remove the debate from the list immediately
      onDelete(debateId);
      console.log("Debate deleted successfully");
    } catch (error) {
      console.error("Failed to delete debate:", error.message);
    }
  };

  return (
    <div
      className="relative w-80% bg-gray-700 mb-5 cursor-pointer blur_background"
      onClick={handleDebateClick}
    >
      {/* Pin Icon in the top right corner - conditionally rendered */}
      {userData &&
        (isFilled ? (
          <PlusCircleIconSolid
            className="absolute top-3 right-3 w-8 h-8 text-white cursor-pointer zoom"
            onClick={handlePlusClick}
          />
        ) : (
          <PlusCircleIcon
            className="absolute top-3 right-3 w-8 h-8 text-white cursor-pointer zoom"
            onClick={handlePlusClick}
          />
        ))}

      {userProfile && userData?.username === data.creatorUserName && (
        <TrashIcon
          className="absolute top-3 right-12 w-8 h-8 text-white cursor-pointer zoom"
          onClick={handleDeleteClick}
        />
      )}

      <div className="flex w-full h-[200px] bg-gray-950 text-white items-center">
        <img
          onClick={(event) => {
            event.stopPropagation();
            handleProfileClick();
          }}
          className="rounded-full h-40 w-40 m-5 object-cover cursor-pointer"
          src={
            userProfile?.profile_picture
              ? `http://${PUBLIC_IP}${userProfile.profile_picture}`
              : "/images/defaultProfilePic.png"
          }
          alt="User Profile"
        />
        <div className="flex flex-col m-3 space-y-12 w-[300px] justify-start">
          <h1>{data.title}</h1>
          <div className="flex space-x-3">
            <h2>{data.creatorUserName}</h2>
            <h2>{new Date(data.created_at).toLocaleDateString("en-GB")}</h2>
          </div>
        </div>
        <div className="flex w-[500px] h-40 border-l-2 border-r-2 ml-5 mr-5">
          {/* Truncated debate content */}
          <p className="m-3">{truncateContent(data.content)}</p>
        </div>
        <div className="flex items-center space-x-5">
          <div className="border-2 h-10 flex align-center items-center">
            <p className="m-1">{averagePercentage}%</p>
          </div>
          <div className="flex items-center">
            <ChatBubbleOvalLeftIcon className="w-11 h-11 text-white ml-3 mr-0" />
            <p className="mr-3 ">{data.numberComments}</p>
          </div>
        </div>
      </div>
    </div>
  );
}


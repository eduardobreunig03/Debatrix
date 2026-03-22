import React, { useEffect, useState } from "react";
import { useRouter } from "next/router"; // Import Next.js router
import { ArrowLeftIcon } from "@heroicons/react/24/outline";
import Link from "next/link";
import Cookies from "js-cookie";
const PUBLIC_IP = "54.80.13.110";


export default function ProfilePage() {
  const router = useRouter(); // Initialize the router
  const [username, setUsername] = useState(router.query.username || ""); // Use router query if available
  const [loading, setLoading] = useState(true);
  const [selectedFile, setSelectedFile] = useState(null);
  const [debateData, setDebateData] = useState([]);

  const [profilePicture, setProfilePicture] = useState(
    router.query.profilePicture || "/images/defaultProfilePic.png"
  );
  const [bio, setBio] = useState(router.query.bio || "");
  const [isEditingBio, setIsEditingBio] = useState(false);

  useEffect(() => {
    if (username && profilePicture && bio) {
      setLoading(false);
      return;
    }

    const fetchUserProfile = async () => {
      const token = Cookies.get("user_token");

      if (token) {
        try {
          const response = await fetch(
            `http://${PUBLIC_IP}/auth/user_profile/`,
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
            setUsername(data.username);
            const profilePictureUrl = data.profile_picture
              ? `http://${PUBLIC_IP}${data.profile_picture}`
              : "/images/defaultProfilePic.png";
            setProfilePicture(profilePictureUrl);
            setBio(data.profile_bio || "");
          } else {
            console.error("Failed to fetch user profile.");
          }
        } catch (error) {
          console.error("Error fetching user profile:", error);
        } finally {
          setLoading(false);
        }
      }
    };

   
    if (!username || !profilePicture || !bio) {
      fetchUserProfile();
    }
  }, [username, profilePicture, bio]);

  const handleBioChange = (event) => {
    setBio(event.target.value);
  };

  const handleFileChange = async (event) => {
    setSelectedFile(event.target.files[0]);

    const token = Cookies.get("user_token");
    if (!token) return;

    const formData = new FormData();
    formData.append("profile_picture", event.target.files[0]);
    formData.append("profile_bio", bio);

    try {
      const response = await fetch(
        `http://${PUBLIC_IP}/auth/update_profile_picture/`
,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
          credentials: "include",
        }
      );

      if (response.ok) {
        const data = await response.json();
        setProfilePicture(URL.createObjectURL(event.target.files[0]));
        setBio(data.profile_bio);
        alert("Profile updated successfully.");
      } else {
        console.error("Failed to update profile.");
      }
    } catch (error) {
      console.error("Error updating profile:", error);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    // The profile picture and bio are already being updated in `handleFileChange`
  };

  //get all debates and then filter them by the user id
  const fetchDebates = async () => {
    try {
      const response = await fetch(`http://${PUBLIC_IP}/api/debates`);
      const result = await response.json();
      setDebateData(result); // Setting the data for the debate.
    } catch (error) {
      console.error("Error fetching debates:", error);
    }
  };

  useEffect(() => {
    fetchDebates();
  }, []);
  //filter the debates by the user id
  const userDebates = debateData.filter((debate) => debate.creatorUserName === username);


  return (

    <>
      <div
        className="min-h-screen flex flex-col bg-gray-900"
        style={{
          backgroundImage: "url(/images/background.jpeg)",
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      >
        <Link href="/home">
          <div className="w-full h-10">
            <ArrowLeftIcon className="w-12 m-3 border-2 border-white rounded-full z-10 text-white" />
          </div>
        </Link>
        <div className="ml-11 mt-5 flex items-center">
          <img
            className="rounded-full h-60 w-60 m-5 object-cover"
            src={profilePicture}
            alt="User Profile"
          />
          <h1 className="text-3xl font-bold text-white">
            {loading ? "Loading..." : username}
          </h1>

          <form encType="multipart/form-data" className="space-x-4 m-2 flex">
            <input
              type="file"
              onChange={handleFileChange}
              accept="image/*"
              className="hidden"
              id="fileInput"
            />
            <button
              type="button"
              className="custom_button"
              onClick={() => document.getElementById("fileInput").click()}
            >
              Update Profile Picture
            </button>
          </form>
          <button
            onClick={() => setIsEditingBio((prev) => !prev)}
            className="custom_button"
          >
            {isEditingBio ? "Cancel" : "Edit Bio"}
          </button>
        </div>

        {isEditingBio && (
          <div className="flex flex-col justify-center">
            <textarea
              value={bio}
              onChange={handleBioChange}
              className="bg-gray-800 text-white p-2 mt-2 rounded w-full"
              placeholder="Write your bio here"
            />
            <button
              onClick={handleSubmit}
              className="bg-black text-white p-2 rounded-md border ml-4 mt-2"
            >
              Save Bio
            </button>
          </div>
        )}

        <hr className="border-white mt-5" />

        {/* Debates Section */}
        <div className="flex flex-col justify-center items-start px-8 mt-10">
          <h2 className="text-2xl text-white mb-5">Your Debates</h2>
          {userDebates.length > 0 ? (
            userDebates.map((debate) => (
              <div
                key={debate.debateId}
                className="bg-gray-800 p-4 rounded-md mb-4 w-full"
              >
                <h3 className="text-xl font-semibold text-white">{debate.title}</h3>
                <p className="text-white mt-2">{debate.content}</p>
                <span className="text-gray-400 text-sm">
                  Created at: {new Date(debate.created_at).toLocaleString()}
                </span>
              </div>
            ))
          ) : (
            <p className="text-gray-400">You haven't created any debates yet.</p>
          )}
        </div>
      </div>
    </>

  );
}

import { useState, useEffect } from "react";
import { ArrowLeftIcon } from "@heroicons/react/24/outline";
import Link from "next/link";
import Cookies from "js-cookie";
import Router from "next/router";

export default function CreateDebate() {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [username, setUsername] = useState("");
  const [loading, setLoading] = useState(true);
  const [profilePicture, setProfilePicture] = useState(
    "/images/defaultProfilePic.png"
  );
  const [userProfile, setUserProfile] = useState(null);
  const PUBLIC_IP = "54.80.13.110";

  useEffect(() => {
    // Only calls this function once on component mount
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
            setUserProfile(data);
            setUsername(data.username);
            const profilePictureUrl = data.profile_picture
              ? `http://${PUBLIC_IP}${data.profile_picture}`
              : "/images/defaultProfilePic.png";
            setProfilePicture(profilePictureUrl);
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

    fetchUserProfile();
  }, []); // Empty dependency array to run once on mount

  const handleSubmit = async (e) => {
    e.preventDefault();

    const debateData = {
      title,
      content,
      creatorUserName: username,
      created_at: new Date().toISOString(),
    };

    try {
      const response = await fetch(`http://${PUBLIC_IP}/api/save_debate/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(debateData),
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Debate created:", data);
        setTitle("");
        setContent("");
        Router.push("/home");
      } else {
        console.error("Error creating debate:", response.statusText);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <>
      <div
        className="min-h-screen flex flex-col bg-gray-900 items-center justify-center relative"
        style={{
          backgroundImage: "url(/images/background.jpeg)",
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      >
        <Link href="/home">
          <div className="absolute top-0 left-0 m-4">
            <ArrowLeftIcon className="w-12 h-12 border-2 border-white rounded-full text-white p-2 cursor-pointer" />
          </div>
        </Link>

        <div className="flex flex-col items-center justify-center w-full h-full text-center">
          <h1 className="text-5xl text-white font-bold mb-8">
            CREATE A DEBATE
          </h1>
          <form
            onSubmit={handleSubmit}
            className="flex flex-col space-y-8 items-center justify-center w-1/2"
          >
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter a title..."
              className="p-2 border rounded-md text-white bg-black w-full"
            />
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Enter the content"
              className="border rounded-md text-white bg-black w-full h-40 p-2 resize-none"
            />
            <button
              type="submit"
              className="bg-black text-white p-2 rounded-md border"
            >
              Create Debate
            </button>
          </form>
        </div>
      </div>
    </>
  );
}


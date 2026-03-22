import React from "react";
import { useRouter } from "next/router";
import { ArrowLeftIcon } from "@heroicons/react/24/outline";
import Link from "next/link";
const PUBLIC_IP = "54.80.13.110";

export default function ProfilePage() {
  const router = useRouter();

  // Accessing data from router.query, with fallback values
  const username = router.query.username || "Guest User";
  const profilePicture = router.query.profile_picture
    ? `http://${PUBLIC_IP}${router.query.profile_picture}`
    : "/images/defaultProfilePic.png";
  const bio = router.query.profile_bio || "This user hasn't written a bio yet.";

  console.log("profile picture", profilePicture);

  return (
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
          <ArrowLeftIcon className="w-12 m-3 border-2 border-white rounded-full z-10 text-white cursor-pointer" />
        </div>
      </Link>

      <div className="ml-11 mt-5 flex items-center">
        <img
          className="rounded-full h-60 w-60 m-5 object-cover"
          src={profilePicture}
          alt="User Profile"
        />

        <div>
          <h1 className="text-3xl font-bold text-white">{username}</h1>
          <p className="text-lg text-gray-300 mt-2">{bio}</p>
        </div>
      </div>

      <hr className="border-white mt-5" />
    </div>
  );
}


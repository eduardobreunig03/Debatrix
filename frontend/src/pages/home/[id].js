import { ArrowLeftIcon } from "@heroicons/react/24/outline"; // Import the arrow icon
import { useRouter } from "next/router";
import React from "react";
import DebatePost from "../../components/DebatePost";
import NavBar from "@/src/components/NavBar";

export default function DebatePage() {
  const router = useRouter();
  const loadingUser = router.query.loadingUser === "true";

  // Function to handle the navigation back to home
  const handleGoBack = () => {
    router.push("/home"); // Navigate to home page
  };

  return (
    <div
      className="min-h-screen flex flex-col bg-gray-900"
      style={{
        backgroundImage: "url(/images/background.jpeg)",
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      <div className="mt-10">
        <button
          className="absolute top-5 left-5 px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition duration-300 flex items-center"
          onClick={handleGoBack}
        >
          <ArrowLeftIcon className="h-5 w-5 mr-2" /> {/* Left arrow icon */}
          Back Home
        </button>
        <DebatePost loadingUser={loadingUser} />
      </div>
    </div>
  );
}

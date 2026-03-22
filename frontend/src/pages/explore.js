import React, { useEffect, useState } from "react";
import NavBar from "../components/NavBar";
import Debate from "../components/Debate";
import SearchBar from "../components/SearchBar";
import { useRouter } from 'next/router';
import Cookies from "js-cookie";

const PUBLIC_IP = "54.80.13.110";


function Explore({ data, done }) {
  const hasDebates = data && data.length > 0;
  const { search } = useRouter().query;
  const [isLoggedIn, setIsLoggedIn] = useState(false); 

  useEffect(() => {
    const token = Cookies.get("user_token");
    setIsLoggedIn(!!token); 
  }, []);
  
  return (
    <div
      className="min-h-screen flex flex-col bg-gray-900 items-center"
      style={{
        backgroundImage: "url(/images/background.jpeg)",
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      <NavBar isLoggedIn={isLoggedIn}  />

      <SearchBar />
      {!search && (
        <p className="text-white">Type to search debates</p>
      )}
      {search && !hasDebates &&(
        <p className="text-white">No debates found</p>
      )}
      {search && hasDebates && (
        <div className="w-full p-10">
          {data.map((debate) => (
            <Debate key={debate.id}  data={debate} isLoggedIn={isLoggedIn} loadingUser={!isLoggedIn}/>
          ))}
        </div>
      )}  
    </div>
  );
}

export default Explore;

export async function getServerSideProps(context) {
  const { query } = context; // Get query parameters
  const searchQuery = query.search || ''; // Get the search query or default to an empty string

  // Fetch data based on the search query
  const response = await fetch(`http://${PUBLIC_IP}/api/debates/?search=${encodeURIComponent(searchQuery)}`);
  const data = await response.json();

  return {
    props: {
      data: data, // Pass the fetched data to the Explore page
      done: true,
    },
  };
}
  
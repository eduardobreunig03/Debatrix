import { MagnifyingGlassIcon} from "@heroicons/react/24/outline";
import { useRouter } from 'next/router';
import { useState } from 'react';
import StandardButton from "./StandardButton";

export default function SearchBar() {
  const router = useRouter();
  const { search } = router.query; 
  const [inputValue, setInputValue] = useState(search || '');

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') { // Check if the pressed key is Enter
      e.preventDefault(); // Prevent default form submission behavior
      const query = e.target.value; // Get the value from the input field

      if (query) {
        router.push(`/explore/?search=${encodeURIComponent(query)}`)
      }
    }
  };

  const handleClear = () => {
    setInputValue('');
    router.push('/explore');
  };

  const handleChange = (e) => {
    setInputValue(e.target.value);
  }


  return (
    <div className="flex justify-center w-[80%] bg-black m-5 rounded-full outline outline-standard">
      <MagnifyingGlassIcon className="w-11 h-11 text-white mr-3 mt-1 mb-1 ml-1" />
      <input
        type="text"
        name="query"
        placeholder="Search"
        value={inputValue}
        onChange={handleChange}
        onKeyDown={handleKeyPress} // Handle key press event
        className="flex-grow px-3 py-2 bg-transparent focus:outline-none focus:border-transparent text-white"
        required
      />

      {search && ( 
        <StandardButton text="Clear" action={handleClear}/>
      )}
    </div>
      

    
  );
}
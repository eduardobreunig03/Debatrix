import Image from "next/image";
import Link from "next/link";

export default function Standard_Button({ text, action }) {
  return (
    <button
        onClick={action}
        className="m-1 px-4 py-2 bg-transparent text-white rounded-full focus:outline-none"
    >
        {text}
    </button>
  );
}

import Image from "next/image";
import localFont from "next/font/local";
import Login from "./login";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});

const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export default function Home({ data, done }) {
  console.log(data);
  return (
    <div
      className="min-h-screen flex items-center justify-center bg-gray-900"
      style={{
        backgroundImage: "url(/images/background.jpeg)",
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      <Login />
    </div>
  );
}

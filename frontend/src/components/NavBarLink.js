import Link from "next/link";
import { useRouter } from "next/router";

export default function NavBarLink({ text, Icon, link, userData, isLoggedIn }) {
  const router = useRouter();

  const handleClick = () => {
    console.log(userData);
    router.push({
      pathname: link,
      query: { isLoggedIn: isLoggedIn },
    });
  };

  return (
    <li
      onClick={handleClick}
      className="flex flex-row justify-center border-r border-l border-white cursor-pointer"
    >
      <div className="flex m-4 hover:text-shadow-glow transition-all duration-300">
        <Icon className="w-11 h-11 text-white mr-3" />
        <span className="text-white text-5xl">{text}</span>
      </div>
    </li>
  );
}

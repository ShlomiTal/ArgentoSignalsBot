import { Link } from "react-router-dom";

const links = [
  { to: "/", label: "Backtest" },
  { to: "/export", label: "Export" },
  { to: "/performance", label: "Performance" },
  { to: "/settings", label: "Settings" }
];

export default function Sidebar() {
  return (
    <div className="w-60 bg-white border-r shadow-sm p-4 space-y-4">
      <h2 className="text-2xl font-bold mb-6">Argento</h2>
      <nav className="flex flex-col space-y-2">
        {links.map((link) => (
          <Link key={link.to} to={link.to} className="text-gray-700 hover:text-blue-600">
            {link.label}
          </Link>
        ))}
      </nav>
    </div>
  );
}
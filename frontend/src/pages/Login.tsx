import { Input } from "../components/ui/input";
import { Button } from "../components/ui/button";

export default function Login() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form className="bg-white p-8 rounded-2xl shadow-md space-y-4 w-full max-w-sm">
        <h2 className="text-2xl font-bold text-center">Login to Argento</h2>
        <Input placeholder="Enter password" type="password" />
        <Button className="w-full">Login</Button>
      </form>
    </div>
  );
}
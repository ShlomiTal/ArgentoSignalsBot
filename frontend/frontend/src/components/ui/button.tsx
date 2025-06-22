import { ButtonHTMLAttributes } from "react";
import { twMerge } from "tailwind-merge";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  className?: string;
}

export function Button({ className, ...props }: ButtonProps) {
  return (
    <button
      className={twMerge(
        "bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-xl shadow-md transition",
        className
      )}
      {...props}
    />
  );
}
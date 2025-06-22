import { ReactNode } from "react";

export function Card({ children }: { children: ReactNode }) {
  return <div className="bg-white shadow-md rounded-2xl overflow-hidden">{children}</div>;
}

export function CardContent({ children, className = "p-6" }: { children: ReactNode; className?: string }) {
  return <div className={className}>{children}</div>;
}
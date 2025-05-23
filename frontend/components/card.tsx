import React from "react";
import { cn } from "@/lib/utils";

interface CardProps {
  children: React.ReactNode;
  className?: string;
}

const Card = ({ children, className }: CardProps) => {
  return (
    <div
      className={cn(
        "w-full min-w-[300px] h-fit bg-muted border border-border rounded-lg",
        className
      )}
    >
      {children}
    </div>
  );
};

export default Card;

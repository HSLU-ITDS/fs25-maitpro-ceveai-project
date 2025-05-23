import React from "react";
import { LucideIcon } from "lucide-react";
import Icons from "./icon";

interface CardItemProps {
  icon: LucideIcon;
  title: string;
  description: string;
  size?: "default" | "large";
}

const CardItem = ({
  icon: Icon,
  title,
  description,
  size = "default",
}: CardItemProps) => {
  return (
    <div
      className={`${
        size === "large" ? "flex space-x-4" : "flex space-x-2"
      } col-span-1`}
    >
      <Icons>
        <Icon className="w-5 h-5" />
      </Icons>
      <div className="flex flex-col">
        <h1
          className={`font-bold ${
            size === "large" ? "text-sm" : "text-xs"
          } text-primary`}
        >
          {title}
        </h1>
        <p
          className={`${
            size === "large" ? "text-sm" : "text-xs"
          } text-muted-foreground`}
        >
          {description}
        </p>
      </div>
    </div>
  );
};

export default CardItem;

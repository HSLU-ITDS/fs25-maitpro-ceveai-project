import React from "react";
interface CardProps {
  children: React.ReactNode;
}
const Icons = ({ children }: CardProps) => {
  return (
    <div className="bg-muted-foreground p-2 w-fit h-fit rounded-md  flex justify-center text-white items-center">
      {" "}
      {children}
    </div>
  );
};

export default Icons;

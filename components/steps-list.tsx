import React from "react";
import { cn } from "@/lib/utils";

interface Step {
  title: string;
}

interface StepsListProps {
  steps: Step[];
  className?: string;
}

const StepsList = ({ steps, className }: StepsListProps) => {
  return (
    <div className={cn("flex flex-col space-y-4", className)}>
      {steps.map((step, index) => (
        <div key={index} className="flex items-center gap-4">
          <div className="flex items-center justify-center w-6 h-6 rounded-full bg-muted-foreground">
            <span className="text-sm font-bold text-background">
              {index + 1}
            </span>
          </div>
          <h2 className="text-sm text-primary font-medium">{step.title}</h2>
        </div>
      ))}
    </div>
  );
};

export default StepsList;

import React from "react";
import { cn } from "@/lib/utils";

interface ModelBadgesProps {
  models: string[];
  className?: string;
}

const ModelBadges = ({ models, className }: ModelBadgesProps) => {
  return (
    <div className={cn("flex gap-2 flex-wrap", className)}>
      {models.map((model, index) => (
        <div
          key={index}
          className="bg-muted-foreground/10 backdrop-blur-sm text-xs px-3 py-1.5 rounded-full font-semibold text-primary"
        >
          {model}
        </div>
      ))}
    </div>
  );
};

export default ModelBadges;

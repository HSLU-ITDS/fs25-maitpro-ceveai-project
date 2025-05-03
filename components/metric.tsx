import React from "react";
import { Trash2, Minus, Plus } from "lucide-react";
import { Criteria } from "@/lib/data";
import { Slider } from "@/components/ui/slider";

interface MetricProps {
  metric: Criteria;
  value: number;
  onChange: (value: number) => void;
  onDelete?: () => void;
}

const Metric = ({ metric, value, onChange, onDelete }: MetricProps) => {
  // Use 0 and 100 as min/max for the slider
  const min = 0;
  const max = 100;

  return (
    <div className="">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <h1 className="text-sm font-semibold text-primary">{metric.name}</h1>
          {onDelete && (
            <Trash2
              className="text-destructive hover:cursor-pointer"
              size={15}
              onClick={onDelete}
            />
          )}
        </div>

        <div className="flex items-center gap-2">
          <span className="text-primary text-xs">{value}%</span>
        </div>
      </div>
      <div className="flex items-center gap-4">
        <button
          className="text-primary hover:bg-muted-foreground rounded-full p-1"
          onClick={() => onChange(Math.max(min, value - 1))}
        >
          <Minus className="border-1 rounded-full border-primary" size={15} />
        </button>
        <div className="flex-1 relative">
          <Slider
            min={min}
            max={max}
            value={[value]}
            onValueChange={([newValue]) => onChange(newValue)}
            step={1}
            className="cursor-pointer"
          />
        </div>
        <button
          className="text-primary hover:bg-muted-foreground rounded-full p-1"
          onClick={() => onChange(Math.min(max, value + 1))}
        >
          <Plus className="border-1 rounded-full border-primary" size={15} />
        </button>
      </div>
    </div>
  );
};

export default Metric;

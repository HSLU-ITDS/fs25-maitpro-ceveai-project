import React from "react";
import { Trash2, Minus, Plus } from "lucide-react";
import { Metric as MetricType } from "@/lib/data";
import { Slider } from "@/components/ui/slider";

interface MetricProps {
  metric: MetricType;
  value: number;
  onChange: (value: number) => void;
  onDelete?: () => void;
}

const Metric = ({ metric, value, onChange, onDelete }: MetricProps) => {
  return (
    <div className="">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <h1 className="text-sm font-semibold text-primary">{metric.name}</h1>
          <Trash2
            className="text-destructive hover:cursor-pointer"
            size={15}
            onClick={onDelete}
          />
        </div>

        <div className="flex items-center gap-2">
          <span className="text-primary text-xs">{value}%</span>
        </div>
      </div>
      <div className="flex items-center gap-4">
        <button
          className="text-primary hover:bg-muted-foreground rounded-full p-1"
          onClick={() => onChange(Math.max(metric.min, value - 1))}
        >
          <Minus className="border-1 rounded-full border-primary" size={15} />
        </button>
        <div className="flex-1 relative">
          <Slider
            min={metric.min}
            max={metric.max}
            value={[value]}
            onValueChange={([newValue]) => onChange(newValue)}
            step={1}
            className="cursor-pointer"
          />
        </div>
        <button
          className="text-primary hover:bg-muted-foreground rounded-full p-1"
          onClick={() => onChange(Math.min(metric.max, value + 1))}
        >
          <Plus className="border-1 rounded-full border-primary" size={15} />
        </button>
      </div>
    </div>
  );
};

export default Metric;

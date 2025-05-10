import React from "react";
import Metric from "./metric";
import { criteria } from "@/lib/data";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogDescription,
} from "./ui/dialog";

interface MetricsPopupProps {
  values: { [key: string]: number };
  setValues: React.Dispatch<React.SetStateAction<{ [key: string]: number }>>;
}

const MetricsPopup = ({ values, setValues }: MetricsPopupProps) => {
  const [title, setTitle] = React.useState("");

  const handleChange = (criteriaName: string, newValue: number) => {
    setValues((prev) => {
      const currentTotal = Object.values(prev).reduce(
        (sum, value) => sum + value,
        0
      );
      const valueDiff = newValue - prev[criteriaName];
      // Handle exceeding 100
      if (currentTotal === 100 && valueDiff > 0) {
        const otherCriteria = criteria.filter((c) => c.name !== criteriaName);
        const otherCriteriaWithRoom = otherCriteria.filter(
          (c) => prev[c.name] > 0
        );
        if (otherCriteriaWithRoom.length === 0) return prev;
        const decreasePerCriteria = Math.ceil(
          valueDiff / otherCriteriaWithRoom.length
        );
        const updatedValues = { ...prev };
        updatedValues[criteriaName] = newValue;
        let remainingDecrease = valueDiff;
        for (const c of otherCriteriaWithRoom) {
          const currentValue = updatedValues[c.name];
          const maxDecrease = Math.min(
            decreasePerCriteria,
            remainingDecrease,
            currentValue
          );
          updatedValues[c.name] = currentValue - maxDecrease;
          remainingDecrease -= maxDecrease;
        }
        if (remainingDecrease > 0) {
          updatedValues[criteriaName] =
            prev[criteriaName] + (valueDiff - remainingDecrease);
        }
        return updatedValues;
      }
      if (newValue === 100) {
        const minValues = Object.fromEntries(criteria.map((c) => [c.name, 0]));
        return {
          ...minValues,
          [criteriaName]: 100,
        };
      }
      const updatedValues = {
        ...prev,
        [criteriaName]: newValue,
      };
      const total = Object.values(updatedValues).reduce(
        (sum, value) => sum + value,
        0
      );
      if (total > 100) {
        const availableSpace = 100 - newValue;
        const otherCriteria = criteria.filter((c) => c.name !== criteriaName);
        const otherTotal = otherCriteria.reduce(
          (sum, c) => sum + updatedValues[c.name],
          0
        );
        if (otherTotal === 0) {
          return {
            ...Object.fromEntries(criteria.map((c) => [c.name, 0])),
            [criteriaName]: newValue,
          };
        }
        const scaleFactor = availableSpace / otherTotal;
        const normalizedValues: { [key: string]: number } = {
          [criteriaName]: newValue,
        };
        otherCriteria.forEach((c) => {
          normalizedValues[c.name] = Math.round(
            updatedValues[c.name] * scaleFactor
          );
        });
        const normalizedTotal = Object.values(normalizedValues).reduce(
          (sum, value) => sum + value,
          0
        );
        if (normalizedTotal !== 100) {
          const lastOtherCriteria =
            otherCriteria[otherCriteria.length - 1]?.name;
          if (lastOtherCriteria) {
            normalizedValues[lastOtherCriteria] += 100 - normalizedTotal;
            normalizedValues[lastOtherCriteria] = Math.max(
              0,
              normalizedValues[lastOtherCriteria]
            );
          }
        }
        return normalizedValues;
      }
      return updatedValues;
    });
  };

  const total = Object.values(values).reduce((sum, value) => sum + value, 0);
  const showError = total !== 100;

  const handleEqualize = () => {
    const equalValue = Math.floor(100 / criteria.length);
    const remainder = 100 % criteria.length;
    setValues(
      Object.fromEntries(
        criteria.map((c, index) => [
          c.name,
          index === criteria.length - 1 ? equalValue + remainder : equalValue,
        ])
      )
    );
  };

  return (
    <div>
      <Dialog>
        <DialogTrigger className="py-2 rounded-md bg-foreground w-full h-fit text-primary-foreground text-sm font-medium">
          Adjust Criteria
        </DialogTrigger>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="hidden">Adjust Criteria</DialogTitle>
            <DialogDescription>
              Make adjustments on metrics weights and modify/add criteria
            </DialogDescription>

            <Input
              placeholder='Add existing criteria or enter a new one using "/" as prefix'
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="bg-background text-sm text-foreground"
            />
          </DialogHeader>
          <div>
            {criteria.map((c) => (
              <Metric
                key={c.name}
                metric={c}
                value={values[c.name]}
                onChange={(value) => handleChange(c.name, value)}
              />
            ))}
          </div>
          <div className="flex flex-col gap-2">
            <Button
              className="text-primary-foreground"
              onClick={handleEqualize}
            >
              Equalize
            </Button>
            {showError && (
              <p className="text-destructive text-sm text-center">
                Criteria percentage must equal 100
              </p>
            )}
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default MetricsPopup;

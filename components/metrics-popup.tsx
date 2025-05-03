import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

import React, { useState } from "react";
import Metric from "./metric";
import { metrics } from "@/lib/data";
import { Button } from "./ui/button";
import { Input } from "./ui/input";

const MetricsPopup = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [title, setTitle] = useState("");
  const equalValue = Math.floor(100 / metrics.length);
  const remainder = 100 % metrics.length;

  const initialValues = Object.fromEntries(
    metrics.map((m, index) => [
      m.name,
      // Add the remainder to the last metric to ensure total is exactly 100
      index === metrics.length - 1 ? equalValue + remainder : equalValue,
    ])
  );

  const [values, setValues] = useState<{ [key: string]: number }>(
    initialValues
  );

  const handleChange = (metricName: string, newValue: number) => {
    setValues((prev) => {
      const currentTotal = Object.values(prev).reduce(
        (sum, value) => sum + value,
        0
      );
      const valueDiff = newValue - prev[metricName];

      // If we're at 100% and trying to increase a value
      if (currentTotal === 100 && valueDiff > 0) {
        const otherMetrics = metrics.filter((m) => m.name !== metricName);
        const otherMetricsWithRoom = otherMetrics.filter(
          (m) => prev[m.name] > m.min
        );

        // If no other metrics can be decreased, prevent the increase
        if (otherMetricsWithRoom.length === 0) {
          return prev;
        }

        // Calculate how much to decrease from each other metric
        const decreasePerMetric = Math.ceil(
          valueDiff / otherMetricsWithRoom.length
        );
        const updatedValues = { ...prev };

        // First, try to apply the increase to the changed metric
        updatedValues[metricName] = newValue;

        // Then distribute the decrease among other metrics
        let remainingDecrease = valueDiff;
        for (const metric of otherMetricsWithRoom) {
          const currentValue = updatedValues[metric.name];
          const maxDecrease = Math.min(
            decreasePerMetric,
            remainingDecrease,
            currentValue - metric.min
          );
          updatedValues[metric.name] = currentValue - maxDecrease;
          remainingDecrease -= maxDecrease;
        }

        // If we couldn't distribute all the decrease, adjust the increase
        if (remainingDecrease > 0) {
          updatedValues[metricName] =
            prev[metricName] + (valueDiff - remainingDecrease);
        }

        return updatedValues;
      }

      // If the new value is 100, set all other metrics to their minimum
      if (newValue === 100) {
        const minValues = Object.fromEntries(
          metrics.map((m) => [m.name, m.min])
        );
        return {
          ...minValues,
          [metricName]: 100,
        };
      }

      // Otherwise, proceed with normal update
      const updatedValues = {
        ...prev,
        [metricName]: newValue,
      };

      // Calculate total of all values
      const total = Object.values(updatedValues).reduce(
        (sum, value) => sum + value,
        0
      );

      // If total exceeds 100, normalize all values except the changed one
      if (total > 100) {
        const minValues = Object.fromEntries(
          metrics.map((m) => [m.name, m.min])
        );

        // Calculate available space for other metrics
        const availableSpace = 100 - newValue;

        // Calculate the sum of other values above their minimums
        const otherMetrics = metrics.filter((m) => m.name !== metricName);
        const aboveMinTotal = otherMetrics.reduce((sum, m) => {
          return sum + Math.max(0, updatedValues[m.name] - m.min);
        }, 0);

        // If there's no space to distribute, set all other metrics to minimum
        if (aboveMinTotal === 0) {
          return {
            ...minValues,
            [metricName]: newValue,
          };
        }

        // Calculate scale factor for other values above minimum
        const scaleFactor = availableSpace / aboveMinTotal;

        // Create normalized values
        const normalizedValues: { [key: string]: number } = {
          [metricName]: newValue,
        };

        otherMetrics.forEach((m) => {
          const min = m.min;
          const aboveMin = Math.max(0, updatedValues[m.name] - min);
          normalizedValues[m.name] = Math.round(min + aboveMin * scaleFactor);
        });

        // Ensure the sum is exactly 100 by adjusting the last other metric
        const normalizedTotal = Object.values(normalizedValues).reduce(
          (sum, value) => sum + value,
          0
        );
        if (normalizedTotal !== 100) {
          const lastOtherMetric = otherMetrics[otherMetrics.length - 1]?.name;
          if (lastOtherMetric) {
            normalizedValues[lastOtherMetric] += 100 - normalizedTotal;
            // Ensure we don't go below minimum
            normalizedValues[lastOtherMetric] = Math.max(
              minValues[lastOtherMetric],
              normalizedValues[lastOtherMetric]
            );
          }
        }

        return normalizedValues;
      }

      return updatedValues;
    });
  };

  const handleDialogClose = () => {
    const total = Object.values(values).reduce((sum, value) => sum + value, 0);
    if (total !== 100) {
      return;
    }
    setIsOpen(false);
  };

  const total = Object.values(values).reduce((sum, value) => sum + value, 0);
  const showError = total !== 100;

  const handleEqualize = () => {
    const equalValue = Math.floor(100 / metrics.length);
    const remainder = 100 % metrics.length;

    setValues(
      Object.fromEntries(
        metrics.map((m, index) => [
          m.name,
          // Add the remainder to the last metric to ensure total is exactly 100
          index === metrics.length - 1 ? equalValue + remainder : equalValue,
        ])
      )
    );
  };

  return (
    <div>
      <Dialog
        open={isOpen}
        onOpenChange={(open) => {
          if (!open) {
            handleDialogClose();
          } else {
            setIsOpen(true);
          }
        }}
      >
        <DialogTrigger className="py-2 rounded-md bg-foreground w-full h-fit text-primary-foreground text-sm font-medium">
          Adjust Metrics
        </DialogTrigger>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="hidden">Adjust Metrics</DialogTitle>
            <Input
              placeholder='Add existing metric or enter a new one using "/" as prefix'
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="bg-background text-sm text-foreground"
            />
          </DialogHeader>
          <div>
            {metrics.map((metric) => (
              <Metric
                key={metric.name}
                metric={metric}
                value={values[metric.name]}
                onChange={(value) => handleChange(metric.name, value)}
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
                Metrics percentage must equal 100
              </p>
            )}
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default MetricsPopup;

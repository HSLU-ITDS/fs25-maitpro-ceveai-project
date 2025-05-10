import React, { useState, useEffect } from "react";
import Metric from "./metric";
import { Criteria } from "@/lib/data";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import AddMetrics from "./add-metrics";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogDescription,
} from "./ui/dialog";

const DEFAULT_METRICS = [
  "Grammar",
  "Relevance",
  "Experience",
  "Conciseness",
  "Engagement",
  "Cohesiveness",
];

const MetricsPopup = ({
  criteria,
  refetchCriteria,
}: {
  criteria: Criteria[];
  refetchCriteria: () => Promise<void>;
}) => {
  const [title, setTitle] = React.useState("");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [shownCriteria, setShownCriteria] = useState<string[]>(DEFAULT_METRICS);
  const [showAddMetrics, setShowAddMetrics] = useState(false);
  const [newCriteriaName, setNewCriteriaName] = useState("");
  const [weights, setWeights] = useState<{ [key: string]: number }>({});

  // Only show default metrics at initial boot
  const defaultCriteria = criteria.filter((c) =>
    shownCriteria.includes(c.name)
  );

  // Autocomplete suggestions: criteria not already shown, matching input
  const suggestions = criteria.filter(
    (c) =>
      !shownCriteria.includes(c.name) &&
      c.name.toLowerCase().startsWith(title.trim().toLowerCase()) &&
      title.trim() !== "" &&
      !title.startsWith("/") // Don't show suggestions when typing a new criteria with "/"
  );

  // On initial mount, equalize weights for default metrics only
  useEffect(() => {
    if (Object.keys(weights).length === 0) {
      const equalValue = Math.floor(100 / DEFAULT_METRICS.length);
      const remainder = 100 % DEFAULT_METRICS.length;
      const initialWeights = Object.fromEntries(
        DEFAULT_METRICS.map((name, idx) => [
          name,
          idx === DEFAULT_METRICS.length - 1
            ? equalValue + remainder
            : equalValue,
        ])
      );
      setWeights(initialWeights);
    }
  }, []);

  // When shownCriteria changes, keep weights in sync (only for displayed criteria)
  useEffect(() => {
    setWeights((prev) => {
      const updated: { [key: string]: number } = {};
      shownCriteria.forEach((name) => {
        updated[name] = prev[name] ?? 0;
      });
      return updated;
    });
  }, [shownCriteria]);

  // Only allow closing dialog if weights sum to 100 or in add metrics mode
  const total = Object.values(weights).reduce((sum, value) => sum + value, 0);
  const showError = Math.round(total) !== 100;
  const handleDialogOpen = (open: boolean) => {
    if (!open) {
      if (showAddMetrics) {
        setShowAddMetrics(false);
        setTitle("");
      } else if (showError) {
        return;
      }
    }
    setDialogOpen(open);
  };

  const handleAddCriteria = (name: string) => {
    setShownCriteria((prev) => [...prev, name]);
    setTitle("");
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      e.preventDefault();
      if (title.startsWith("/") && title.length > 1) {
        const criteriaName = title.slice(1).trim();
        if (criteriaName) {
          setShowAddMetrics(true);
          setNewCriteriaName(criteriaName);
        }
      } else if (suggestions.length > 0) {
        handleAddCriteria(suggestions[0].name);
      }
    }
  };

  const handleSaveNewCriteria = async (name: string, description: string) => {
    if (refetchCriteria) {
      await refetchCriteria();
    }
    setShowAddMetrics(false);
    setTitle("");
    setNewCriteriaName("");
  };

  const handleCancelAddCriteria = () => {
    setShowAddMetrics(false);
    setTitle("");
    setNewCriteriaName("");
  };

  const handleChange = (criteriaName: string, newValue: number) => {
    setWeights((prev) => {
      const updatedWeights = { ...prev, [criteriaName]: newValue };
      const total = Object.values(updatedWeights).reduce(
        (sum, val) => sum + val,
        0
      );
      if (total === 100) return updatedWeights;
      if (newValue === 100) {
        const result = Object.fromEntries(
          Object.keys(updatedWeights).map((key) => [
            key,
            key === criteriaName ? 100 : 0,
          ])
        );
        return result;
      }
      const otherCriteriaNames = Object.keys(updatedWeights).filter(
        (name) => name !== criteriaName && updatedWeights[name] > 0
      );
      if (otherCriteriaNames.length === 0) {
        return Object.fromEntries(
          Object.keys(updatedWeights).map((key) => [
            key,
            key === criteriaName ? 100 : 0,
          ])
        );
      }
      const excess = total - 100;
      const otherTotal = otherCriteriaNames.reduce(
        (sum, name) => sum + updatedWeights[name],
        0
      );
      const result = { ...updatedWeights };
      if (otherTotal > 0) {
        otherCriteriaNames.forEach((name) => {
          const proportion = updatedWeights[name] / otherTotal;
          result[name] = Math.max(
            0,
            Math.round(updatedWeights[name] - excess * proportion)
          );
        });
      }
      const newTotal = Object.values(result).reduce((sum, val) => sum + val, 0);
      if (newTotal !== 100 && otherCriteriaNames.length > 0) {
        const diff = 100 - newTotal;
        const lastCriteriaName =
          otherCriteriaNames[otherCriteriaNames.length - 1];
        result[lastCriteriaName] = Math.max(0, result[lastCriteriaName] + diff);
      } else if (newTotal !== 100) {
        result[criteriaName] = 100;
      }
      return result;
    });
  };

  const handleRemoveCriteria = (name: string) => {
    const updated = shownCriteria.filter((n) => n !== name);
    setShownCriteria(updated);
    setWeights((old) => {
      const newWeights = { ...old };
      delete newWeights[name];
      return Object.fromEntries(
        Object.entries(newWeights).filter(([k]) => updated.includes(k))
      );
    });
  };

  const handleEqualize = () => {
    const equalValue = Math.floor(100 / shownCriteria.length);
    const remainder = 100 % shownCriteria.length;
    setWeights(
      Object.fromEntries(
        shownCriteria.map((name, idx) => [
          name,
          idx === shownCriteria.length - 1
            ? equalValue + remainder
            : equalValue,
        ])
      )
    );
  };

  return (
    <div>
      <Dialog open={dialogOpen} onOpenChange={handleDialogOpen}>
        <DialogTrigger className="py-2 rounded-md bg-foreground w-full h-fit text-primary-foreground text-sm font-medium">
          Adjust Criteria
        </DialogTrigger>

        <DialogContent>
          {!showAddMetrics ? (
            <>
              <DialogHeader>
                <DialogTitle className="hidden">Adjust Criteria</DialogTitle>
                <DialogDescription className="hidden">
                  Make adjustments on metrics weights and modify/add criteria
                </DialogDescription>

                {/* Input and suggestions wrapper */}
                <div className="relative">
                  <Input
                    placeholder='Add existing criteria or enter a new one using "/" as prefix'
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className="bg-background text-sm text-foreground"
                    autoComplete="off"
                    onKeyDown={handleKeyDown}
                  />

                  {/* Autocomplete suggestions */}
                  {suggestions.length > 0 && (
                    <div className="absolute left-0 right-0 top-full border bg-background mt-1 max-h-40 overflow-auto rounded-md z-50">
                      {suggestions.map((c) => (
                        <div
                          key={c.id}
                          className="px-3 py-1 hover:bg-muted cursor-pointer text-left"
                          onClick={() => handleAddCriteria(c.name)}
                        >
                          {c.name}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </DialogHeader>

              {/* Show metrics */}
              <div className="max-h-65 overflow-auto">
                {defaultCriteria.map((c) => (
                  <Metric
                    key={c.id}
                    metric={c}
                    value={weights[c.name] ?? 0}
                    onChange={(value) => handleChange(c.name, value)}
                    onDelete={() => handleRemoveCriteria(c.name)}
                  />
                ))}
              </div>

              {/* Equalize button and error */}
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
            </>
          ) : (
            /* Show AddMetrics when in add mode - outside of DialogHeader for better layout */
            <AddMetrics
              initialName={newCriteriaName}
              onSave={handleSaveNewCriteria}
              onCancel={handleCancelAddCriteria}
            />
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default MetricsPopup;

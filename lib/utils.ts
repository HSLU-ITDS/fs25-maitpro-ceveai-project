import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { Criteria } from "./data";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
/**
 * Merges the original criteria array with a map of updated weights (percentages),
 * returning a new array with the updated weights (as decimals).
 * If a criterion's weight is 0, it is excluded from the result.
 * @param criteria The original criteria array
 * @param weights A map of { [criteriaName]: weightPercent }
 * @returns A new array of criteria with updated weights, excluding those with weight 0
 */
export function mergeCriteriaWeights(
  criteria: Criteria[],
  weights: { [key: string]: number }
): Criteria[] {
  return criteria
    .map((c) => ({
      ...c,
      weight: (weights[c.name] ?? Math.round(c.weight * 100)) / 100,
    }))
    .filter((c) => c.weight > 0);
}

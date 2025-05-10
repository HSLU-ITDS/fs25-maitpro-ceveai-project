import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { Criteria } from "./data";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Filters and returns criteria that have non-zero weights, including only name and description.
 * @param criteria The original criteria array
 * @param weights A map of { [criteriaName]: weightPercent }
 * @returns A new array of criteria with only name and description, excluding those with weight 0
 */
export function mergeCriteriaWeights(
  criteria: Criteria[],
  weights: { [key: string]: number }
): { name: string; description: string }[] {
  return criteria
    .filter((c) => (weights[c.name] ?? Math.round(c.weight * 100)) > 0)
    .map((c) => ({
      name: c.name,
      description: c.description,
    }));
}

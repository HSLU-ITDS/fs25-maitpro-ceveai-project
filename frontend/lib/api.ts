export const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const endpoints = {
  results: (id: string) => `${API_URL}/results/${id}`,
  criteria: `${API_URL}/criteria`,
  jobAnalyses: `${API_URL}/job-analyses`,
  analyzeCVs: `${API_URL}/analyze-cvs`,
  generatePDF: `${API_URL}/generate-pdf`,
} as const;

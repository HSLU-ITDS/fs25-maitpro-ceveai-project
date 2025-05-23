function getRuntimeConfig() {
  if (typeof window !== "undefined" && (window as any).__CONFIG__) {
    return (window as any).__CONFIG__;
  }
  return { API_URL: "" };
}

export function getApiUrl() {
  return getRuntimeConfig().API_URL;
}

export const endpoints = {
  results: (id: string) => `${getApiUrl()}/results/${id}`,
  criteria: () => `${getApiUrl()}/criteria`,
  jobAnalyses: () => `${getApiUrl()}/job-analyses`,
  analyzeCVs: () => `${getApiUrl()}/analyze-cvs`,
  generatePDF: () => `${getApiUrl()}/generate-pdf`,
} as const;

// Export a getter function for API_URL instead of a constant
export const getAPI_URL = getApiUrl;

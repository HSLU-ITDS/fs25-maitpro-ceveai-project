"use client";

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
} from "@/components/ui/sidebar";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { FileUploader } from "@/components/FileUpload";
import { useState, useEffect } from "react";
import MetricsPopup from "./metrics-popup";
import { useRouter } from "next/navigation";
import { Criteria } from "@/lib/data";
import { HistoryDialog } from "./history-dialog";
import { endpoints } from "@/lib/api";

type JobAnalysis = {
  id: string;
  created_at: string;
};

type AnalysisResult = {
  job_analysis_id: string;
  // Add other result properties as needed
};

export function AppSidebar() {
  const [files, setFiles] = useState<File[]>([]);
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [criteria, setCriteria] = useState<Criteria[]>([]);
  const [shownCriteria, setShownCriteria] = useState<string[]>([]);
  const [weights, setWeights] = useState<{ [key: string]: number }>({});
  const [jobAnalyses, setJobAnalyses] = useState<JobAnalysis[]>([]);

  // Fetch criteria from backend
  const fetchCriteria = async () => {
    const response = await fetch(endpoints.criteria());
    const data = await response.json();
    setCriteria(data.criteria);
  };

  // Fetch job analyses
  const fetchJobAnalyses = async () => {
    try {
      const response = await fetch(endpoints.jobAnalyses());
      if (!response.ok) {
        throw new Error("Failed to fetch job analyses");
      }
      const data = await response.json();
      setJobAnalyses(data.job_analyses);
    } catch (error) {
      console.error("Error fetching job analyses:", error);
    }
  };

  useEffect(() => {
    fetchCriteria();
    fetchJobAnalyses();
  }, []);

  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    // Get the criteria with their weights
    const criteriaWithWeights = criteria
      .filter((c) => shownCriteria.includes(c.name)) // Only include shown criteria
      .map((c) => ({
        id: c.id,
        name: c.name,
        description: c.description,
        weight: weights[c.name] / 100, // Convert percentage to decimal
      }));

    // Add these logs
    console.log("Criteria:", criteria);
    console.log("Shown Criteria:", shownCriteria);
    console.log("Weights:", weights);
    console.log("Criteria with Weights:", criteriaWithWeights);

    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));
    formData.append("criteria", JSON.stringify(criteriaWithWeights));
    formData.append("prompt", JSON.stringify({ job_description: prompt }));

    // Log the actual data being sent
    console.log("Form Data Criteria:", formData.get("criteria"));

    try {
      const response = await fetch(endpoints.analyzeCVs(), {
        method: "POST",
        body: formData,
      });
      if (!response.ok) {
        throw new Error(`Request failed: ${response.statusText}`);
      }
      const data = await response.json();
      const jobAnalysisId = data.job_analysis_id;

      // Fetch updated job analyses after successful evaluation
      await fetchJobAnalyses();

      router.push(`/results/${jobAnalysisId}`);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const handleCriteriaChange = (
    shown: string[],
    newWeights: { [key: string]: number }
  ) => {
    setShownCriteria(shown);
    setWeights(newWeights);
  };

  return (
    <Sidebar>
      <SidebarContent className="px-3">
        <SidebarGroup>
          <SidebarHeader className="pt-5">
            <h1 className="font-extrabold text-4xl">CEVEAI</h1>
          </SidebarHeader>
          <p className="text-sm text-muted-foreground">
            CEVEAI is an intelligent resume assessment platform designed to
            streamline the hiring process and enhance job applications. Using
            advanced AI, it analyzes CVs for structure, relevance, and key
            qualifications, providing instant feedback and actionable
            improvement suggestions.
          </p>
        </SidebarGroup>
        <form onSubmit={handleSubmit} className="space-y-4">
          <SidebarGroup>
            <FileUploader selectedFiles={files} onFilesSelected={setFiles} />
          </SidebarGroup>

          <SidebarGroup>
            <div className="grid gap-1.5">
              <Label htmlFor="message" className="text-sm">
                Job Description
              </Label>
              <Textarea
                id="message"
                placeholder="Type your message here."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className="min-h-36 max-h-38 overflow-auto resize-none"
              />
            </div>
          </SidebarGroup>

          <SidebarGroup className="flex flex-col space-y-2">
            <MetricsPopup
              criteria={criteria}
              refetchCriteria={fetchCriteria}
              onCriteriaChange={handleCriteriaChange}
            />
            <Button
              type="submit"
              disabled={loading || files.length === 0}
              className="bg-foreground"
            >
              {loading ? "Evaluating..." : "Evaluate"}
            </Button>
            {error && <p className="text-destructive text-sm">{error}</p>}
          </SidebarGroup>
        </form>

        <SidebarGroup className="h-10 w-full mt-auto flex flex-col">
          <HistoryDialog
            jobAnalyses={jobAnalyses}
            onRefresh={fetchJobAnalyses}
          />
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter />
    </Sidebar>
  );
}

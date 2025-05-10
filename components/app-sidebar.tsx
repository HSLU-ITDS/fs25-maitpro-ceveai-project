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
import { useState } from "react";
import MetricsPopup from "./metrics-popup";

import { criteria } from "@/lib/data";
import { mergeCriteriaWeights } from "@/lib/utils";
import { useRouter } from "next/navigation";


export function AppSidebar() {
  const [files, setFiles] = useState<File[]>([]);
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);


  const router = useRouter();

  // Call the /analyze-cvs endpoint with files and merged criteria
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    const adjustedCriteria = mergeCriteriaWeights(criteria, criteriaWeights);
    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));
    formData.append("criteria", JSON.stringify(adjustedCriteria));
    formData.append("prompt", JSON.stringify({ job_description: prompt }));
    try {

      const response = await fetch("http://localhost:8000/analyze-cvs", {
        method: "POST",
        body: formData,
      });
      if (!response.ok) {
        throw new Error(`Request failed: ${response.statusText}`);
      }
      const data = await response.json();
      const jobAnalysisId = data.job_analysis_id;
      router.push(`/results/${jobAnalysisId}`);

    } catch (err) {
      console.error("Evaluation error:", err);
      let errorMessage = "An error occurred while evaluating the CVs";

      if (err instanceof Error) {
        errorMessage = err.message;
      }

      // Try to extract more detailed error from response if available
      if (err instanceof Error && "cause" in err) {
        try {
          const responseData = await (err.cause as Response).json();
          if (responseData.detail) {
            errorMessage = `Error: ${responseData.detail}`;
          }
        } catch {
          // Unable to parse response JSON
        }
      }

      setError(errorMessage);
    } finally {
      setLoading(false);
    }
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
            advanced AI, it analyzes CVs and images for structure, relevance,
            and key qualifications, providing instant feedback and actionable
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
                placeholder="Enter your evaluation criteria for PDFs or images..."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className="h-10 max-h-16 overflow-auto resize-none"
              />
            </div>
          </SidebarGroup>

          <SidebarGroup className="">
            <MetricsPopup
              values={criteriaWeights}
              setValues={setCriteriaWeights}
            />
            <Button type="submit" disabled={loading || files.length === 0}>
              {loading ? "Evaluating..." : "Evaluate"}
            </Button>
            {error && <p className="text-destructive text-sm">{error}</p>}

          </SidebarGroup>
        </form>
      </SidebarContent>

      <SidebarFooter />
    </Sidebar>
  );
}

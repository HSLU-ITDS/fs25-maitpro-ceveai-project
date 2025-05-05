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

// Define the response type for the rank-cvs endpoint
interface RankCVsResponse {
  status: string;
  ranked_cvs: Array<{
    filename: string;
    summary: {
      skills?: string[];
      experience?: string[];
      education?: string[];
      overall_match?: string;
      [key: string]: unknown;
    };
    score?: number;
  }>;
}

async function evaluateFiles(files: File[], prompt: string) {
  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));

  // The backend expects criteria as a List[str]
  // In FastAPI, to send a list via FormData, we need to append the same key multiple times
  // For now, we're just sending a single criteria item (the prompt)
  formData.append("criteria", prompt);

  const response = await fetch("http://localhost:8000/rank-cvs", {
    method: "POST",
    headers: {
      Accept: "application/json",
    },
    body: formData,
  });

  if (!response.ok) {
    // Create error with response attached for more details
    const error = new Error(
      `Evaluation failed: ${response.statusText}`
    ) as Error & { cause: Response };
    error.cause = response;
    throw error;
  }

  return (await response.json()) as RankCVsResponse;
}

export function AppSidebar() {
  const [files, setFiles] = useState<File[]>([]);
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<RankCVsResponse | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      if (!prompt.trim()) {
        throw new Error("Please enter criteria for evaluating the CVs");
      }

      const data = await evaluateFiles(files, prompt);
      setResult(data);
      // Don't clear files and prompt so user can see what they submitted
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
                Prompt
              </Label>
              <Textarea
                id="message"
                placeholder="Enter your evaluation criteria for PDFs or images..."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
              />
            </div>
          </SidebarGroup>

          <SidebarGroup className="">
            {" "}
            <MetricsPopup />
            <Button type="submit" disabled={loading || files.length === 0}>
              {loading ? "Evaluating..." : "Evaluate"}
            </Button>
            {error && <p className="text-destructive text-sm">{error}</p>}
            {result && (
              <div className="mt-2 p-2 border rounded text-sm">
                <p className="text-green-600">✓ Successfully ranked CVs</p>
                <div className="mt-2">
                  <p className="font-semibold">Ranked CV Results:</p>
                  <ul className="mt-1 space-y-1">
                    {result.ranked_cvs.map((cv, index) => (
                      <li key={index} className="text-xs">
                        {index + 1}. {cv.filename}
                        {cv.score && <span className="ml-1">({cv.score})</span>}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </SidebarGroup>
        </form>
      </SidebarContent>

      <SidebarFooter />
    </Sidebar>
  );
}

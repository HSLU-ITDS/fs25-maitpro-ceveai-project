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

async function evaluateFiles(files: File[], prompt: string) {
  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));
  formData.append("prompt", prompt);

  const response = await fetch("http://localhost:8000/upload-preview", {
    method: "POST",
    headers: {
      Accept: "application/json",
    },
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Upload failed: ${response.statusText}`);
  }

  return await response.json();
}

export function AppSidebar() {
  const [files, setFiles] = useState<File[]>([]);
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null); // optionally type this later

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await evaluateFiles(files, prompt);
      setResult(data);
      setFiles([]);
      setPrompt("");
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Sidebar>
      <SidebarHeader className="pt-5">
        <h1 className="font-extrabold text-4xl px-3">CEVEAI</h1>
      </SidebarHeader>

      <SidebarContent className="px-3">
        <form onSubmit={handleSubmit} className="space-y-4">
          <SidebarGroup>
            <p className="text-sm text-muted-foreground">
              CEVEAI is an intelligent resume assessment platform designed to
              streamline the hiring process and enhance job applications. Using
              advanced AI, it analyzes CVs for structure, relevance, and key
              qualifications, providing instant feedback and actionable
              improvement suggestions.
            </p>
          </SidebarGroup>

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
                placeholder="Type your message here."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
              />
              <Button type="submit" disabled={loading || files.length === 0}>
                {loading ? "Evaluating..." : "Evaluate"}
              </Button>
              {error && <p className="text-destructive text-sm">{error}</p>}
              {result && (
                <div className="mt-2 p-2 border rounded text-sm">
                  <p className="text-green-600">✓ {result.message}</p>
                  <p className="text-gray-600 mt-1 text-xs">{result.prompt}</p>
                </div>
              )}
            </div>
          </SidebarGroup>
        </form>
      </SidebarContent>

      <SidebarFooter />
    </Sidebar>
  );
}

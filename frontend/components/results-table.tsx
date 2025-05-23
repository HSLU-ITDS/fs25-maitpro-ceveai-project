"use client";
import { useState } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { toast } from "sonner";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "./ui/button";
import { endpoints } from "@/lib/api";

type Candidate = {
  index: number;
  filename: string;
  candidate_name: string;
  summary: string;
  total_score: number;
  scores: CandidateScore[];
};

type CandidateScore = {
  criterion: string;
  score: number;
  explanation?: string;
};

type ResultsTableProps = {
  candidates: Candidate[];
  selected: Candidate;
  onSelect: (candidate: Candidate) => void;
};

export function ResultsTable({
  candidates,
  selected,
  onSelect,
}: ResultsTableProps) {
  const [expanded, setExpanded] = useState(true);

  // Get all unique criteria from all candidates
  const allCriteria = Array.from(
    new Set(candidates.flatMap((c) => c.scores.map((s) => s.criterion)))
  );

  return (
    <div className="w-full">
      <div className="h-fit w-full flex justify-between pb-2 items-end">
        <h1 className=" text-muted-foreground">Top Candidates</h1>
        <Button
          className="bg-transparent text-primary border-2 border-border hover:bg-muted"
          onClick={async () => {
            const response = await fetch(endpoints.generatePDF, {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ candidates }),
            });

            if (!response.ok) {
              toast.error("Failed to generate PDF");
              return;
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "candidates-report.pdf";
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
            toast.success("PDF report generated successfully");
          }}
        >
          Export to PDF
        </Button>
      </div>

      {/* Table container with relative positioning */}
      <div className="relative">
        {/* Scroll container */}
        <div className="max-h-[300px] overflow-y-auto border rounded-md">
          <Table className="min-w-full table-auto">
            <TableHeader className="sticky top-0 z-10">
              <TableRow className="">
                <TableHead className="bg-background border-r border-border">
                  Rank
                </TableHead>
                <TableHead className="bg-background border-r border-border">
                  Candidate
                </TableHead>
                <TableHead className="bg-background border-r border-border">
                  Total
                </TableHead>
                {expanded &&
                  allCriteria.map((criterion) => (
                    <TableHead
                      key={criterion}
                      className="bg-background border-r border-border"
                    >
                      {criterion}
                    </TableHead>
                  ))}
              </TableRow>
            </TableHeader>

            <TableBody>
              {candidates.map((c, index) => (
                <TableRow
                  key={c.filename}
                  onClick={() => onSelect(c)}
                  className={
                    (index % 2 === 0 ? "bg-muted" : "bg-background") +
                    (selected.filename === c.filename ? " font-bold" : "")
                  }
                >
                  <TableCell>{c.index}</TableCell>
                  <TableCell>{c.candidate_name}</TableCell>
                  <TableCell>{c.total_score}</TableCell>
                  {expanded &&
                    allCriteria.map((criterion) => {
                      const scoreObj = c.scores.find(
                        (s) => s.criterion === criterion
                      );
                      return (
                        <TableCell key={criterion}>
                          {scoreObj ? scoreObj.score : "-"}
                        </TableCell>
                      );
                    })}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>

        {/* Retractable UI Element - now matches table height */}
        <div
          onClick={() => setExpanded(!expanded)}
          className="absolute top-0 -right-4 w-4 bg-accent hover:bg-muted-foreground transition-colors flex items-center justify-center cursor-pointer border-l z-20"
          aria-label={expanded ? "Collapse table" : "Expand table"}
          role="button"
          tabIndex={0}
        >
          <div className="h-8 w-4 flex items-center justify-center">
            {expanded ? (
              <ChevronRight className="h-4 w-4 text-primary" />
            ) : (
              <ChevronLeft className="h-4 w-4 text-primary" />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

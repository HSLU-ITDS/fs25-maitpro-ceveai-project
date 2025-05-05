"use client";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { candidates } from "@/lib/data";

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
  // Get all unique criteria from all candidates
  const allCriteria = Array.from(
    new Set(candidates.flatMap((c) => c.scores.map((s) => s.criterion)))
  );

  return (
    <div className="w-full">
      <h1 className="py-1 text-muted-foreground">Top Candidates</h1>

      {/* Scroll container */}
      <div className="max-h-[300px] overflow-y-auto border rounded-md">
        <Table className="min-w-full table-auto">
          <TableHeader>
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
              {allCriteria.map((criterion) => (
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
                {allCriteria.map((criterion) => {
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
    </div>
  );
}

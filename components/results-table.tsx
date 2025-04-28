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

export function ResultsTable() {
  return (
    <div className="w-full">
      <h1 className="py-1 text-slate-400">Top Candidates</h1>

      {/* Scroll container */}
      <div className="max-h-[300px] overflow-y-auto border rounded-md">
        <Table className="min-w-full table-auto">
          <TableHeader>
            <TableRow className="">
              <TableHead className="bg-background border-r">
                Candidate
              </TableHead>
              <TableHead className="bg-background border-r">Total</TableHead>
              <TableHead className="bg-background border-r">
                Relevance
              </TableHead>
              <TableHead className="bg-background border-r">Grammar</TableHead>
              <TableHead className="bg-background border-r">
                Experience
              </TableHead>
              <TableHead className="bg-background border-r">
                Cohesiveness
              </TableHead>
            </TableRow>
          </TableHeader>

          <TableBody>
            {candidates.map((candidate, index) => (
              <TableRow
                key={index}
                className={index % 2 === 0 ? "bg-muted/50" : "bg-background"}
              >
                <TableCell className="border-r">{candidate.Name}</TableCell>
                <TableCell className="border-r">{candidate.Total}</TableCell>
                <TableCell className="border-r">
                  {candidate.Relevance}
                </TableCell>
                <TableCell className="border-r">{candidate.Grammar}</TableCell>
                <TableCell className="border-r">
                  {candidate.Experience}
                </TableCell>
                <TableCell className="border-r">
                  {candidate.Cohesiveness}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}

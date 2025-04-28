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
      <h1 className="py-1 text-muted-foreground">Top Candidates</h1>

      {/* Scroll container */}
      <div className="max-h-[300px] overflow-y-auto border rounded-md">
        <Table className="min-w-full table-auto">
          <TableHeader>
            <TableRow className="">
              <TableHead className="bg-background border-r border-border">
                Candidate
              </TableHead>
              <TableHead className="bg-background border-r border-border">
                Total
              </TableHead>
              <TableHead className="bg-background border-r border-border">
                Relevance
              </TableHead>
              <TableHead className="bg-background border-r border-border">
                Grammar
              </TableHead>
              <TableHead className="bg-background border-r border-border">
                Experience
              </TableHead>
              <TableHead className="bg-background border-r border-border">
                Cohesiveness
              </TableHead>
            </TableRow>
          </TableHeader>

          <TableBody>
            {candidates.map((candidate, index) => (
              <TableRow
                key={index}
                className={index % 2 === 0 ? "bg-muted" : "bg-background "}
              >
                <TableCell>{candidate.Name}</TableCell>
                <TableCell>{candidate.Total}</TableCell>
                <TableCell>{candidate.Relevance}</TableCell>
                <TableCell>{candidate.Grammar}</TableCell>
                <TableCell>{candidate.Experience}</TableCell>
                <TableCell>{candidate.Cohesiveness}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}

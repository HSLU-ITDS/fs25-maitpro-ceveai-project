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
import React from "react";

export type CandidateScore = {
  criterion: string;
  score: number;
};

export function IndivScore({ scores }: { scores: CandidateScore[] }) {
  return (
    <div className="w-full">
      <div className="max-h-[300px] overflow-y-auto border border-border rounded-md">
        <Table className="min-w-full table-auto">
          <TableHeader>
            <TableRow className="">
              <TableHead className="bg-background border-r  border-border text-primary">
                Metric
              </TableHead>
              <TableHead className="bg-background border-r  border-border text-primary">
                Score
              </TableHead>
            </TableRow>
          </TableHeader>

          <TableBody>
            {scores.map((item, index) => {
              const isEven = index % 2 === 0;
              const baseBg = isEven ? "bg-muted" : "bg-background";
              const hoverBg = isEven
                ? "hover:bg-muted hover:font-normal text-primary"
                : "hover:bg-background hover:font-normal text-primary";

              return (
                <TableRow
                  key={`${item.criterion}-${index}`}
                  className={`${baseBg} ${hoverBg}`}
                >
                  <TableCell>{item.criterion}</TableCell>
                  <TableCell>{item.score}</TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}

export default IndivScore;

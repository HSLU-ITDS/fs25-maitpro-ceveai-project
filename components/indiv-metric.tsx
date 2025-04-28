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
import { scores } from "@/lib/data";

export function IndivScore() {
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
            {scores.map((score, index) => (
              <React.Fragment key={index}>
                {[
                  { label: "Relevance", value: score.Relevance },
                  { label: "Grammar", value: score.Grammar },
                  { label: "Experience", value: score.Experience },
                  { label: "Cohesiveness", value: score.Cohesiveness },
                ].map((item, subIndex) => {
                  const isEven = (index * 4 + subIndex) % 2 === 0;
                  const baseBg = isEven ? "bg-muted" : "bg-background";
                  const hoverBg = isEven
                    ? "hover:bg-muted hover:font-normal text-primary"
                    : "hover:bg-background hover:font-normal text-primary";

                  return (
                    <TableRow
                      key={`${item.label}-${index}`}
                      className={`${baseBg} ${hoverBg}`}
                    >
                      <TableCell>{item.label}</TableCell>
                      <TableCell>{item.value}</TableCell>
                    </TableRow>
                  );
                })}
              </React.Fragment>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}

export default IndivScore;

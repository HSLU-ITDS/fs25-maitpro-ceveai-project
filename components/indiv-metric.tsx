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
      <div className="max-h-[300px] overflow-y-auto border rounded-md">
        <Table className="min-w-full table-auto">
          <TableHeader>
            <TableRow className="">
              <TableHead className="bg-background border-r">Metric</TableHead>
              <TableHead className="bg-background border-r">Score</TableHead>
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
                  const isEven = (index * 4 + subIndex) % 2 === 0; // 4 rows per score item
                  const baseBg = isEven ? "bg-muted/50" : "bg-background";
                  const hoverBg = isEven
                    ? "hover:bg-muted/50 hover:font-normal"
                    : "hover:bg-background hover:font-normal"; // adjust hover matching base

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

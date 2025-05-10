"use client";
import React, { useState } from "react";
import { ResultsTable } from "@/components/results-table";
import Summary from "@/components/individual-summary";
import Header from "@/components/header";

type CandidateScore = {
  criterion: string;
  score: number;
};

type Candidate = {
  index: number;
  filename: string;
  candidate_name: string;
  summary: string;
  total_score: number;
  scores: CandidateScore[];
};

type ResultsPageProps = {
  data: {
    candidates: Candidate[];
  };
};

const ResultsPage = ({ data }: ResultsPageProps) => {
  const [selected, setSelected] = useState<Candidate>(data.candidates[0]);

  return (
    <div className="flex flex-col flex-1 h-full min-h-0">
      <div className="mx-10 flex-1 flex flex-col space-y-6">
        <div className="h-full flex-5/12">
          <ResultsTable
            candidates={data.candidates}
            selected={selected}
            onSelect={setSelected}
          />
        </div>
        <div className="h-full flex-7/12">
          <Summary candidate={selected} />
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;

import React from "react";
import IndivScore from "./indiv-metric";

type Candidate = {
  index: number;
  filename: string;
  candidate_name: string;
  summary: string;
  total_score: number;
  scores: { criterion: string; score: number }[];
};

type SummaryProps = {
  candidate: Candidate;
};

const Summary = ({ candidate }: SummaryProps) => {
  return (
    <>
      <div className="w-full h-full flex space-x-8">
        <div className="flex-2 h-full flex flex-col ">
          <div className="grid grid-cols-6">
            <div className="col-span-5 flex space-x-8 px-6 pb-4">
              <h1 className="text-gray-600 text-4xl font-bold">
                #{candidate.index}
              </h1>
              <h1 className="font-semibold text-3xl">
                {candidate.candidate_name}
              </h1>
            </div>
          </div>
          <div className="flex-1 overflow-auto px-6">
            <p className="text-muted-foreground text-sm">{candidate.summary}</p>
          </div>
        </div>
        <div className="h-full flex-1 grid grid-row-6">
          <h1 className="text-primary text-4xl font-bold row-span-1 justify-self-end">
            {candidate.total_score}/10
          </h1>
          <div className="row-span-5">
            <IndivScore scores={candidate.scores} />
          </div>
        </div>
      </div>
      <div className="mt-4">
        <h2 className="text-2xl font-bold mb-2">Scores</h2>
        <ul className="list-disc pl-8">
          {candidate.scores.map((s) => (
            <li key={s.criterion}>
              {s.criterion}: {s.score}
            </li>
          ))}
        </ul>
      </div>
    </>
  );
};

export default Summary;

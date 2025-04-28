import * as React from "react";
import { ResultsTable } from "@/components/results-table";
import Summary from "@/components/individual-summary";
import Header from "@/components/header";

const Home = () => {
  return (
    <div className="flex flex-col h-screen">
      <div className="mx-10 flex-1 flex flex-col ">
        <div className="h-full flex-5/12">
          <ResultsTable />
        </div>
        <div className="h-full flex-7/12">
          <Summary />
        </div>
      </div>
    </div>
  );
};

export default Home;

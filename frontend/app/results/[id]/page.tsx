import ResultsPage from "./ResultsPage";
import React, { Suspense } from "react";

function Loading() {
  return (
    <div className="flex items-center justify-center h-full text-xl">
      Loading results...
    </div>
  );
}

export default async function Page({ params }: { params: { id: string } }) {
  const resolvedParams = await params;
  const fetchData = async () => {
    const res = await fetch(
      `http://localhost:8000/results/${resolvedParams.id}`
    );
    const data = await res.json();
    console.log(data);
    return data;
  };

  // Use Suspense to show loading while waiting for data
  return (
    <Suspense fallback={<Loading />}>
      <ResultsPage data={await fetchData()} />
    </Suspense>
  );
}

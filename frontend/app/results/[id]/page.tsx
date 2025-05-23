import ResultsPage from "./ResultsPage";
import React, { Suspense } from "react";
import { endpoints } from "@/lib/api";

function Loading() {
  return (
    <div className="flex items-center justify-center h-full text-xl">
      Loading results...
    </div>
  );
}

export default async function Page(props: any) {
  const fetchData = async () => {
    const res = await fetch(endpoints.results(props.params.id));
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

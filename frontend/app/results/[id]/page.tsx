"use client";
import React, { useState, useEffect, use } from "react";
import ResultsPage from "./ResultsPage";
import { endpoints } from "@/lib/api";

function Loading() {
  return (
    <div className="flex items-center justify-center h-full text-xl">
      Loading results...
    </div>
  );
}

export default function Page({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch(endpoints.results(resolvedParams.id));
        if (!res.ok) {
          throw new Error(`Failed to fetch results: ${res.statusText}`);
        }
        const data = await res.json();
        setData(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [resolvedParams.id]);

  if (loading) {
    return <Loading />;
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-full text-xl text-red-500">
        Error: {error}
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex items-center justify-center h-full text-xl">
        No data found
      </div>
    );
  }

  return <ResultsPage data={data} />;
}

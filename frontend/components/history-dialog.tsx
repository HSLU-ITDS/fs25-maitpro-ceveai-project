import React from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "./ui/dialog";
import { History } from "lucide-react";
import { useRouter } from "next/navigation";
import { format } from "date-fns";

type JobAnalysis = {
  id: string;
  created_at: string;
};

interface HistoryDialogProps {
  jobAnalyses: JobAnalysis[];
  onRefresh: () => Promise<void>;
}

export function HistoryDialog({ jobAnalyses, onRefresh }: HistoryDialogProps) {
  const router = useRouter();

  return (
    <Dialog>
      <DialogTrigger className="w-full h-20 flex items-center justify-center space-x-2 hover:bg-muted rounded-md transition-colors">
        <History className="w-4 h-4 text-muted-foreground" />
        <h1 className="w-fit text-muted-foreground">Assessment History</h1>
      </DialogTrigger>

      <DialogContent>
        <DialogHeader>
          <DialogTitle className="text-muted-foreground">
            Assessment History
          </DialogTitle>
        </DialogHeader>
        <div className="max-h-[400px] overflow-y-auto">
          {jobAnalyses.length === 0 ? (
            <p className="text-center text-muted-foreground">
              No assessments found
            </p>
          ) : (
            <div className="space-y-2">
              {jobAnalyses.map((analysis) => (
                <button
                  key={analysis.id}
                  onClick={() => router.push(`/results/${analysis.id}`)}
                  className="w-full p-3 text-left hover:bg-muted rounded-md transition-colors"
                >
                  <div className="flex justify-between items-center">
                    <span className="font-medium text-xs">{analysis.id}</span>
                    <span className="text-sm text-muted-foreground">
                      {format(
                        new Date(analysis.created_at),
                        "MMM d, yyyy 'at' h:mm a"
                      )}
                    </span>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}

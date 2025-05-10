"use client";

import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";

interface FileUploaderProps {
  onFilesSelected: (files: File[]) => void;
  selectedFiles: File[];
}

export function FileUploader({
  onFilesSelected,
  selectedFiles,
}: FileUploaderProps) {
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const fileList = e.target.files;
    if (fileList) {
      const pdfFiles = Array.from(fileList).filter((file) =>
        file.name.endsWith(".pdf")
      );
      onFilesSelected(pdfFiles);
    }
  };

  return (
    <div className="grid w-full max-w-sm items-center gap-1.5">
      <Label htmlFor="cv-upload" className="text-sm">
        Upload CVs
      </Label>
      <Input
        id="cv-upload"
        type="file"
        accept=".pdf"
        multiple
        className="mt-2"
        onChange={handleFileChange}
      />

      {selectedFiles.length > 1 && (
        <div className="w-full border rounded-md overflow-y-scroll mt-2 max-h-30 text-muted-foreground">
          {selectedFiles.map((file, index) => (
            <div key={index} className="text-sm py-0.5 px-2 truncate">
              {file.name}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

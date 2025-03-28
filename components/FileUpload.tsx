"use client";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { useState } from "react";

export function FileUploader() {
  const [selectedFiles, setSelectedFiles] = useState<FileList | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setSelectedFiles(e.target.files);
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

      {selectedFiles && selectedFiles.length > 1 && (
        <div
          className="w-full border rounded-md overflow-y-auto overflow-x-hidden"
          style={{ maxHeight: "10rem" }}
        >
          {Array.from(selectedFiles).map((file, index) => (
            <div key={index} className="text-sm py-1 px-2 truncate">
              {file.name}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { useState } from "react";
import { toast } from "sonner";

interface AddMetricsProps {
  initialName?: string;
  onSave: (name: string, description: string) => void;
  onCancel: () => void;
}

const AddMetrics = ({
  initialName = "",
  onSave,
  onCancel,
}: AddMetricsProps) => {
  const [name, setName] = useState(
    initialName.startsWith("/") ? initialName.slice(1) : initialName
  );
  const [description, setDescription] = useState("");

  const handleSave = async () => {
    const trimmedName = name.trim();
    const trimmedDescription = description.trim();
    if (!trimmedName || !trimmedDescription) {
      toast.error(
        <span className="text-destructive">
          Name and description are required.
        </span>
      );
      return;
    }
    const casedName =
      trimmedName.charAt(0).toUpperCase() + trimmedName.slice(1);

    // Call backend to save
    try {
      const res = await fetch("http://localhost:8000/criteria", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: casedName,
          description: trimmedDescription,
        }),
      });
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Failed to save criterion");
      }
      const saved = await res.json();
      toast(`Saved: ${saved.name} as a new metric`);
      setName("");
      onSave(saved.name, saved.description);
    } catch (err: any) {
      toast.error(
        <span className="text-destructive">
          {err.message || "Failed to save criterion"}
        </span>
      );
    }
  };

  return (
    <div className="mx-[-24px] mt-[-16px] mb-[-20px] bg-background rounded-b-lg p-4 flex flex-col gap-4 overflow-auto">
      <h1 className="text-lg font-semibold">Add new criteria</h1>
      <div className="flex flex-col gap-2">
        <Label htmlFor="name" className="text-sm font-medium">
          Name
        </Label>
        <Input
          id="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="bg-background text-sm text-foreground w-full break-words"
          placeholder="Enter criterion name"
        />
      </div>
      <div className="flex flex-col gap-2">
        <Label htmlFor="description" className="text-sm font-medium">
          Description
        </Label>
        <Textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="bg-background text-sm text-foreground h-52 w-full overflow-y-auto resize-none"
          placeholder="Enter criterion description"
        />
      </div>
      <div className="flex justify-end gap-2 mt-2">
        <Button variant="outline" onClick={onCancel}>
          Cancel
        </Button>
        <Button
          type="button"
          onClick={handleSave}
          disabled={!name.trim() || !description.trim()}
        >
          Save
        </Button>
      </div>
    </div>
  );
};

export default AddMetrics;

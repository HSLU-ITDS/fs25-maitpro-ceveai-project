import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
} from "@/components/ui/sidebar";
import { Label } from "@radix-ui/react-dropdown-menu";
import { Textarea } from "./ui/textarea";
import { Button } from "./ui/button";
import { Input } from "@/components/ui/input";

export function AppSidebar() {
  return (
    <Sidebar>
      <SidebarHeader className="pt-5">
        <h1 className="font-extrabold text-4xl p-3">CEVEAI</h1>
      </SidebarHeader>
      <SidebarContent className="px-3">
        <SidebarGroup>
          <p className="text-sm dark:text-gray-400 font-extralight text-black">
            CEVEAI is an intelligent resume assessment platform designed to
            streamline the hiring process and enhance job applications. Using
            advanced AI, it analyzes CVs for structure, relevance, and key
            qualifications, providing instant feedback and actionable
            improvement suggestions.
          </p>
        </SidebarGroup>
        <SidebarGroup>
          <div className="grid w-full max-w-sm items-center gap-1.5">
            <Label htmlFor="cv-upload" className="text-sm">
              Files
            </Label>
            <Input id="cv-upload" type="file" />
          </div>
        </SidebarGroup>

        <SidebarGroup>
          <div className="grid gap-1.5">
            <Label htmlFor="message" className="text-sm">
              Prompt
            </Label>
            <Textarea placeholder="Type your message here." id="message" />
            <Button>Evaluate</Button>
          </div>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter />
    </Sidebar>
  );
}

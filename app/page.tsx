import Card from "@/components/card";
import CardItem from "@/components/card-item";
import ModelBadges from "@/components/model-badges";
import StepsList from "@/components/steps-list";
import React from "react";
import {
  Zap,
  SlidersVertical,
  MessageSquareText,
  Target,
  FileText,
  UserRoundCheck,
  FileStack,
  ListCollapse,
  WandSparkles,
  Server,
} from "lucide-react";

const Landing = () => {
  const supportedModels = [
    "GPT-4o",
    "Claude 3 Opus",
    "Gemini Pro",
    "Llama 3",
    "Mistral Large",
  ];

  const getStartedSteps = [
    {
      title: "Define Job Requirements and Specifications",
      description:
        "Define your job requirements and specifications in the sidebar",
    },
    {
      title: "Upload pool of CVs to be analyzed",
      description: "Upload candidate CVs for analysis",
    },
    {
      title: "Adjust and add metrics to your preference",
      description: "Adjust metrics & weighting as needed",
    },
    {
      title: "Review and compare detailed overall and individual results",
      description: "Evaluate and review the AI-powered results",
    },
  ];

  return (
    <div className="flex flex-row h-full ">
      <div className="flex-8/12 flex flex-col px-6 space-y-6">
        <h1 className="text-5xl font-extrabold text-primary ">
          Smarter <span className="text-muted-foreground">Hiring</span> <br />{" "}
          Starts with <br /> Smarter{" "}
          <span className="text-muted-foreground">Sreening</span>
        </h1>
        <div className=" w-full h-[100px] flex flex-col space-y-5">
          <div
            className="flex
           flex-col space-y-3"
          >
            <div className="flex space-x-4 font-semibold rounded-md bg-muted py-2 px-5 w-fit shadow-xl">
              <WandSparkles className="w-5 h-5" />
              <h1 className="text-sm">AI-Powered CV Assessment & Scoring</h1>
            </div>
            <div className="text-muted-foreground text-sm">
              Analyze CVs for structure, relevance, grammar, and key
              qualifications—while giving you the flexibility to customize or
              add your own evaluation criteria for personalized hiring
              decisions.
            </div>
          </div>
          <Card className="px-4 py-2">
            <div className="flex flex-col space-y-2">
              <div className="flex  space-x-4 font-semibold rounded-md">
                <WandSparkles className="w-5 h-5 text-primary" />
                <h1 className="text-sm text-primary">
                  AI-Powered CV Assessment & Scoring
                </h1>
              </div>
              <p className="text-muted-foreground text-sm">
                CeVeAI leverages advanced language models to deliver accurate
                and insightful resume analysis.
              </p>
              <ModelBadges models={supportedModels} />

              <div className="grid grid-cols-12 gap-3 ">
                <div className="col-span-4 flex items-center gap-2">
                  <Server className="w-8 h-8" />
                  <h1 className="text-sm font-semibold  text-primary">
                    Self-host option available:
                  </h1>
                </div>
                <p className="col-span-8 text-sm text-muted-foreground ">
                  Deploy locally with your own LLMs for complete data privacy
                </p>
              </div>
            </div>
          </Card>
          <h1 className="text-primary text-sm font-semibold">
            Get started with these steps:
          </h1>
          <StepsList steps={getStartedSteps} />
        </div>
      </div>

      <div className="flex-5/12 flex items-center">
        <Card className="px-4 py-6 ">
          <div className="flex flex-col space-y-4">
            <h1 className="font- text-primary font-bold">How CEVEAI Works</h1>
            <div className="w-full h-fit flex flex-col space-y-4">
              <CardItem
                icon={FileText}
                title="CVs & Query Parsing"
                description="Parses and formats key requirements from your job description and CV pool"
                size="large"
              />
              <CardItem
                icon={UserRoundCheck}
                title="Evaluation"
                description="LLMs process the formatted query and evaluate each formatted CV contents"
                size="large"
              />
              <CardItem
                icon={FileStack}
                title="Scoring & Ranking"
                description="Candidates are scored and ranked based on the requirements and configured metrics"
                size="large"
              />
              <CardItem
                icon={ListCollapse}
                title="Detailed Insights"
                description="Get detailed feedback on summary and individual results"
                size="large"
              />
            </div>
          </div>

          <hr className="my-4 border-ring" />

          {/*Why CEVEAI ITEMS*/}
          <div className="flex flex-col space-y-4">
            <div>
              <h1 className="text-primary font-bold">Why CEVEAI?</h1>
            </div>
            <div className="grid grid-row-2 gap-8">
              <div className="row-span-1 h-12 grid grid-cols-2 gap-3">
                <CardItem
                  icon={Zap}
                  title="Faster Screening"
                  description="Quickly analyze resumes"
                />
                <CardItem
                  icon={Target}
                  title="Objectivity"
                  description="Consistently eliminate bias"
                />
              </div>
              <div className="row-span-1 h-12 grid grid-cols-2 gap-3">
                <CardItem
                  icon={SlidersVertical}
                  title="Fully Adaptable"
                  description="Tailored to your needs"
                />
                <CardItem
                  icon={MessageSquareText}
                  title="Deep Insights"
                  description="Beyond keyword matching"
                />
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default Landing;

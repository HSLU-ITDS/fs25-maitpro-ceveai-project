export interface Candidate {
  Name: string;
  Total: string;
  Relevance: string;
  Grammar: string;
  Experience: string;
  Cohesiveness: string;
}

export interface Scores {
  Relevance: string;
  Grammar: string;
  Experience: string;
  Cohesiveness: string;
}

export interface Metric {
  name: string;
  min: number;
  max: number;
  defaultValue: number;
}

export const candidates: Candidate[] = [
  {
    Name: "John Doe",
    Total: "9.0",
    Relevance: "9.0",
    Grammar: "9.0",
    Experience: "9.0",
    Cohesiveness: "9.0",
  },
  {
    Name: "John Doe",
    Total: "9.0",
    Relevance: "9.0",
    Grammar: "9.0",
    Experience: "9.0",
    Cohesiveness: "9.0",
  },
  {
    Name: "John Doe",
    Total: "9.0",
    Relevance: "9.0",
    Grammar: "9.0",
    Experience: "9.0",
    Cohesiveness: "9.0",
  },
  {
    Name: "John Doe",
    Total: "9.0",
    Relevance: "9.0",
    Grammar: "9.0",
    Experience: "9.0",
    Cohesiveness: "9.0",
  },
  {
    Name: "John Doe",
    Total: "9.0",
    Relevance: "22.0",
    Grammar: "9.0",
    Experience: "9.0",
    Cohesiveness: "9.0",
  },
  {
    Name: "John Doe",
    Total: "9.0",
    Relevance: "9.0",
    Grammar: "9.0",
    Experience: "9.0",
    Cohesiveness: "9.0",
  },
  {
    Name: "John Doe",
    Total: "9.0",
    Relevance: "9.0",
    Grammar: "9.0",
    Experience: "9.0",
    Cohesiveness: "9.0",
  },
  {
    Name: "John Doe",
    Total: "9.0",
    Relevance: "9.0",
    Grammar: "9.0",
    Experience: "9.0",
    Cohesiveness: "9.0",
  },
  {
    Name: "John Doe",
    Total: "9.0",
    Relevance: "9.0",
    Grammar: "9.0",
    Experience: "9.0",
    Cohesiveness: "9.0",
  },
  {
    Name: "John Doe",
    Total: "9.0",
    Relevance: "22.0",
    Grammar: "9.0",
    Experience: "9.0",
    Cohesiveness: "9.0",
  },
  {
    Name: "John Doe",
    Total: "9.0",
    Relevance: "22.0",
    Grammar: "9.0",
    Experience: "9.0",
    Cohesiveness: "9.0",
  },
];

export const scores: Scores[] = [
  {
    Relevance: "9.0",
    Grammar: "9.0",
    Experience: "9.0",
    Cohesiveness: "9.0",
  },
];

export const metrics: Metric[] = [
  {
    name: "Relevance",
    min: 0,
    max: 100,
    defaultValue: 0,
  },
  {
    name: "Experience",
    min: 0,
    max: 100,
    defaultValue: 0,
  },
  {
    name: "Conciseness",
    min: 0,
    max: 100,
    defaultValue: 0,
  },
  {
    name: "Engagement",
    min: 0,
    max: 100,
    defaultValue: 0,
  },
  {
    name: "Cohesiveness",
    min: 0,
    max: 100,
    defaultValue: 0,
  },
  {
    name: "Grammar",
    min: 0,
    max: 100,
    defaultValue: 0,
  },
];

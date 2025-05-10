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

export interface Criteria {
  name: string;
  weight: number;
  description: string;
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

export const criteria: Criteria[] = [
  {
    name: "Relevance",
    weight: 0.3,
    description:
      "Evaluate how well the candidate's experience and skills align with the job requirements. Consider the match between their background and the role's key responsibilities and qualifications.",
  },
  {
    name: "Experience",
    weight: 0.25,
    description:
      "Assess the depth and breadth of the candidate's professional experience. Consider the duration, progression, and relevance of their work history to the position.",
  },
  {
    name: "Conciseness",
    weight: 0.15,
    description:
      "Evaluate how effectively the candidate communicates their qualifications without unnecessary details. Consider the clarity and efficiency of their presentation.",
  },
  {
    name: "Engagement",
    weight: 0.1,
    description:
      "Assess how compelling and engaging the candidate's presentation is. Consider the use of action verbs, achievements, and the overall impact of their narrative.",
  },
  {
    name: "Cohesiveness",
    weight: 0.1,
    description:
      "Evaluate how well the different sections of the candidate's profile flow together. Consider the logical progression and consistency of their career story.",
  },
  {
    name: "Grammar",
    weight: 0.1,
    description:
      "Assess the technical quality of the writing. Consider spelling, grammar, punctuation, and overall language proficiency.",
  },
];

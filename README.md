# CEVEAI Project

This is a full-stack application built with [Next.js](https://nextjs.org) for the frontend and [FastAPI](https://fastapi.tiangolo.com/) for the backend.

## Project Structure

```
.
├── app/                 # Next.js frontend application
├── backend/            # FastAPI backend application
│   ├── main.py        # FastAPI application entry point
│   └── fastapienv/    # Python virtual environment
├── components/         # Reusable React components
├── hooks/             # Custom React hooks
└── lib/               # Utility functions and shared code
```

## Prerequisites

Before you begin, ensure you have the following installed:
- [Node.js](https://nodejs.org/) (Latest LTS version)
- [Python 3](https://www.python.org/) (3.8 or higher)
- [npm](https://www.npmjs.com/) (comes with Node.js)
- Docker 
- OpenAI API key

### Environment Setup

#### Backend
Create a `.env.backend` file in the root directory:

```bash
DATABASE_URL=postgresql://postgres:dbpass@host.docker.internal:5432/ceveai
PROVIDER=openai
OPENAI_API_KEY=<your_api_key_here>
```

You can obtain an API key by:
1. Going to [OpenAI's platform](https://platform.openai.com/)
2. Creating an account or signing in
3. Navigating to API keys section
4. Creating a new API key

#### Backend
Create a `.env.frontend` file in the root directory:

```bash
NEXT_PUBLIC_BACKEND_API=https://...
```

## Development Setup

We've provided a script to automate the development environment setup. Simply run:

```bash
./run_dev.sh
```

This script will:
1. Create and activate a Python virtual environment
2. Install all Python dependencies
3. Install Node.js dependencies
4. Start both the backend and frontend development servers

### Manual Setup

If you prefer to set up manually:

#### Backend Setup
```bash
cd backend
python3 -m venv venv
source fastapienv/bin/activate
pip install fastapi uvicorn python-dotenv
uvicorn main:app --reload --port 8000
```

#### Frontend Setup
```bash
npm install
npm run dev
```

## Accessing the Application

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend API: [http://localhost:8000](http://localhost:8000)
- API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

## Learn More

To learn more about the technologies used in this project:

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

## Deployment

The frontend can be deployed on [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme).

For deployment instructions, check out:
- [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying)
- [FastAPI deployment documentation](https://fastapi.tiangolo.com/deployment/)

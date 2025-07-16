# AI Agent Project

A multi-purpose AI agent backend, designed to work seamlessly with a Next.js frontend. This project leverages modern LLMs and tool integrations to provide a flexible, extensible AI assistant.

## Features

-   Modular tool system (math, weather, code execution, and more)
-   LLM-powered conversational agent (Groq, OpenAI, etc.)
-   Extensible with new tools and providers
-   FastAPI backend
-   Ready-to-use with a Next.js frontend

## Requirements

-   Python 3.9+
-   Node.js 18+ (for frontend)
-   [Poetry](https://python-poetry.org/) or `pip` for Python dependencies
-   API keys for:
    -   Groq
    -   OpenWeather
    -   OpenAI

## Getting Started

### 1. Clone the Backend

```bash
git clone https://github.com/diego3008/ai_agent_course.git
cd ai_agent_course
```

### 2. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

Or, if using Poetry:

```bash
poetry install
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory with the following content:

```env
GROQ_API_KEY=your_groq_api_key
OPENWEATHER_API=your_openweather_api_key
OPENAI_API_KEY=your_openai_api_key
```

### 4. Run the Backend

```bash
uvicorn app.main:app --reload
```

---

## Frontend Setup

This project requires a separate frontend, available at [ai_agent_front](https://github.com/diego3008/ai_agent_front).

### 1. Clone the Frontend

```bash
git clone https://github.com/diego3008/ai_agent_front.git
cd ai_agent_front
```

### 2. Install Frontend Dependencies

```bash
npm install
```

Or, if you use Yarn:

```bash
yarn
```

### 3. Run the Frontend

```bash
npm run dev
```

Or:

```bash
yarn dev
```

The frontend will be available at [http://localhost:3000](http://localhost:3000).

---

## Usage

-   Interact with the AI agent via the frontend interface.
-   The backend exposes a FastAPI server for agent interactions and tool execution.

## Project Structure

```
ai_agent_course/
  ├── app/
  │   ├── agent/
  │   ├── api/
  │   ├── schemas/
  │   └── main.py
  ├── requirements.txt
  └── ...
```

## Adding New Tools

To add new tools, define them in `app/agent/tools.py` using the `@tool` decorator. They will be automatically available to the agent.

## License

MIT

---

**Note:**  
You must run both the backend and the frontend for the application to work as intended.

# AI Agent Learning

This is a repository that I made to learn about AI Agents using Google's Agent Development Kit.  

## Prerequisites
1. Install Poetry
2. Copy the .env.example file to .env and fill in the values.
    To fill the values, you can create a free Gemini API key from Google AI Studio.
3. Install the dependencies
```bash
poetry install
```
4. Run the database schema creation script
```bash
poetry run python init-database.py
```

## Run the agent
To run the agent in the development web interface, run the following command:
```bash
poetry run adk web
```

To run the agent in the command line, run the following command:
```bash
poetry run adk run
```
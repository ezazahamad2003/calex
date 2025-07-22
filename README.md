# AI Prospecting Agent

This project is a simple command-line AI agent that helps you find potential prospects (customers) based on your company's information and a search query. It uses the Perplexity AI API to perform deep research and returns a structured JSON list of prospects.

## Features

-   **AI-Powered Prospecting**: Leverages Perplexity AI's `sonar-deep-research` model to find relevant prospects.
-   **Easy to Use**: Simple interactive command-line interface.
-   **Customizable Prompts**: Uses a `prompt_template.txt` file for easy customization of the AI's instructions.
-   **Structured Output**: Returns a clean JSON array of prospects, which can be easily used in other applications.
-   **Save Results**: Prompts to save the generated prospect list to a timestamped JSON file.
-   **Secure API Key Handling**: Uses a `.env` file to keep your API key safe and out of the source code.

## How to Use

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ezazahamad2003/calex.git
    cd calex
    ```

2.  **Install dependencies:**
    This script requires `requests` and `python-dotenv`.
    ```bash
    pip install requests python-dotenv
    ```

3.  **Create a `.env` file:**
    In the `test deepresearch` directory, create a file named `.env` and add your Perplexity API key:
    ```
    PERPLEXITY_API_KEY=your_api_key_here
    ```

4.  **Run the script:**
    ```bash
    python "test deepresearch/main.py"
    ```

5.  **Follow the prompts:**
    -   Enter your company's information.
    -   Enter what kind of prospects you are looking for.

The script will then perform the research and print the results to the console, asking if you'd like to save them to a file.

## Project Structure

-   `test deepresearch/main.py`: The main Python script for the AI prospecting agent.
-   `test deepresearch/prompt_template.txt`: The template used to generate the prompt for the Perplexity AI.
-   `.gitignore`: Ensures that the `.env` file with your API key is not committed to the repository.
-   `README.md`: This file. 
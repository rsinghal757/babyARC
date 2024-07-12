# Tape Transformation Game

This repository contains an interactive game designed to solve abstraction and reasoning tasks. The game presents users with input-output string pairs, and the goal is to determine the transformation logic to predict the output for a given input.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Game Interface](#game-interface)
- [System Prompt](#system-prompt)
- [Development and Testing](#development-and-testing)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/rsinghal757/babyARC.git
    cd babyARC
    ```

2. **Set up a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    Create a `.env` file in the root directory with the following content:
    ```
    OPENAI_ORGANIZATION=your_organization_id
    OPENAI_PROJECT=your_project_id
    OPENAI_API_KEY=your_api_key
    ```

## Usage

1. **Run the game:**
    ```bash
    jupyter notebook
    ```
    Open the `TapeTransformationGame.ipynb` notebook and execute the cells to start the game interface.

2. **Playing the game:**
    The game consists of multiple tasks, each with 4 example input-output pairs and a fifth input for which you need to predict the output. Use the provided color buttons to construct your predicted output tape.

## Game Interface

The game interface is implemented using Jupyter widgets to create an interactive experience. The main components of the interface include:

- **Task Display:**
  Shows the current task number and example input-output pairs.

- **Input and Output Tapes:**
  Displays the input tape for the current task and allows the user to construct the output tape.

- **Color Buttons:**
  Buttons representing different colors that users can click to add to the output tape.

- **Delete Button:**
  Allows users to remove the last added color from the output tape.

- **Check Button:**
  Validates the constructed output tape against the correct output for the current task.

- **Navigation Buttons:**
  Previous and Next buttons to navigate through different tasks.

## System Prompt

The system prompt guides the logic and reasoning process for solving the tasks. It consists of the following steps:

1. **Understand the Problem:**
   Identify the logic or transformation guiding the input-output mapping.

2. **Generate a Program:**
   Write a Python function named `transform` that implements the identified logic. The function should take an input tape as a string and return the transformed output tape as a string.

3. **Evaluate the Program:**
   Test the generated function against the example pairs to ensure correctness.

## Development and Testing

The repository includes a test framework to evaluate the generated programs. The main components include:

- **`test_program_and_get_feedback` Function:**
  Compiles and executes the generated Python code, then evaluates it against example pairs and provides feedback.

- **`decode_task` Function:**
  Converts a task dictionary into a human-readable format for the system prompt.

- **`solve` Function:**
  Iteratively attempts to solve the task by generating reasoning and programs, testing them, and refining based on feedback.

## Contributing

Contributions are welcome! If you have any suggestions, improvements, or bug fixes, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
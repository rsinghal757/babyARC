from dotenv import load_dotenv
import os
import sys
import io
import traceback

from openai import OpenAI

load_dotenv()

# Retrieve the values from environment variables
organization = os.getenv("OPENAI_ORGANIZATION")
project = os.getenv("OPENAI_PROJECT")
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    organization=organization,
    project=project,
    api_key=api_key
)
model="gpt-4o-mini"

with open('prompts/system_prompt.txt', 'r') as file:
    system_prompt = file.read()

def test_program_and_get_feedback(code, test_cases):
    # Redirect stdout and stderr
    old_stdout, old_stderr = sys.stdout, sys.stderr
    redirected_output = io.StringIO()
    redirected_error = io.StringIO()
    sys.stdout, sys.stderr = redirected_output, redirected_error

    try:
        # First, try to compile the code to catch syntax errors
        try:
            compiled_code = compile(code, '<string>', 'exec')
        except SyntaxError as se:
            return False, False, f"Syntax Error: {str(se)}\n\nDetails:\n{traceback.format_exc()}"

        # If compilation succeeds, execute the code
        global_vars = {}
        try:
            exec(compiled_code, global_vars)
        except Exception as e:
            return False, False, f"Runtime Exception: {type(e).__name__}: {str(e)}\n\nDetails:\n{traceback.format_exc()}"

        # Check for any output or errors
        output = redirected_output.getvalue()
        error = redirected_error.getvalue()
        
        if error:
            return False, False, f"Error Output:\n{error}"

        # Run test cases
        test_cases = task.get(list(task.keys())[0])
        test_results = []
        train_cases_passed = True
        fifth_case_passed = False
        for i, (input_value, expected_output) in enumerate(test_cases[:-1]): # Skip the 5th case
            try:
                result = global_vars['transform'](input_value)
                passed = result == expected_output
                test_results.append(f"Test case {i+1}: {'PASS' if passed else 'FAIL'}")
                test_results.append(f"  Input: {input_value}, Expected: {expected_output}, Got: {result}")
                if not passed:
                    train_cases_passed = False
            except Exception as e:
                train_cases_passed = False
                test_results.append(f"Test case {i+1}: ERROR - {type(e).__name__}: {str(e)}")

        # Prepare feedback
        feedback = []
        if output:
            feedback.append(f"Standard Output:\n{output}")
        feedback.append("Test Results:")
        feedback.extend(test_results)
        
        if train_cases_passed:
            fifth_case_result = global_vars['transform'](test_cases[-1][0])
            fifth_case_passed = fifth_case_result == test_cases[-1][1]

        return train_cases_passed, fifth_case_passed, "\n".join(feedback)

    finally:
        # Restore stdout and stderr
        sys.stdout, sys.stderr = old_stdout, old_stderr

def decode_task(task):
    task_pairs = task.get(list(task.keys())[0])
    train_pairs = task_pairs[:-1]
    decoded_task = ""
    for train_pair in train_pairs:
        decoded_task = decoded_task + "Input Tape: " + train_pair[0] + ", Output Tape: " + train_pair[1] + "\n"
    return decoded_task

def solve(task, max_retries=10):
    # Task in natural language
    task_prompt = decode_task(task)

    assistant = client.beta.assistants.create(
        name="Reasoning Task Solver",
        instructions=f"{system_prompt}".format(task_prompt=task_prompt, max_retries=max_retries),
        model=model
    )
    thread = client.beta.threads.create()

    for i in range(max_retries):

        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"Try {i+1}: Step 1 - Articulate your reasoning for solving the task. Plain English.")
        run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=assistant.id)

        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"Try {i+1}: Step 2 - Write the program based on your reasoning. Python only.")
        run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=assistant.id)

        if run.status == "completed":
            print(f"{'-'*8} Try {i+1} completed. Program generated.")
            message = client.beta.threads.messages.list(thread_id=thread.id, limit=1)
            code = message.data[0].content[0].text.value[9:-3]

        train_tests_passed, fifth_test_passed, output = test_program_and_get_feedback(code, task)
        print(f"{'-'*8} Program evaluated.")

        if train_tests_passed:
            if fifth_test_passed:
                print("Task solved successfully!\n")
                return True
            return False

        message = client.beta.threads.messages.create(thread_id=thread.id, role="user", content=output)

    return False

with open('tasks.txt', 'r') as file:
    data = file.read()
tasks_list = data.strip().split('\n\n')
tasks = []

for idx, task in enumerate(tasks_list):
    task_name = f'task_{idx}'
    task_data = []
    for line in task.split('\n'):
        groups = [group.strip() for group in line.split('-')]
        task_data.append(groups)
    tasks.append({task_name: task_data})

score = 0
for i in range(0, len(tasks)):
    print(f"Solving task: {i+1}")
    print(f"{'='*50}")
    task = tasks[i]
    solved = solve(task, max_retries=25)
    score += solved
    print(f"{'='*50}\n")

print(f"Accuracy: Solved {score} out of {len(tasks)} tasks")
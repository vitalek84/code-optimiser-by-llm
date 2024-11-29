import argparse
import os
import subprocess
import time
from typing import Any, Tuple, List, Dict, Optional

from langchain.callbacks.tracers import ConsoleCallbackHandler
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

DEBUG = False


class LLMInterface:
    """A class for interacting with Ollama, OpenAI, Anthropic, or Google Palm models."""
    def __init__(self, model_type: str, prompt_tpl: ChatPromptTemplate, name: Optional[str] = None,
                 temperature: float = 1.0) -> None:
        """
        Initialize the LLM interface.

        Args:
            model_type (str): The model type ('ollama', 'openai', 'anthropic', or 'googlepalm').
            prompt_tpl (ChatPromptTemplate): The prompt template to use.
            name (Optional[str]): The model name.
            temperature (float): Sampling temperature.
        """
        self.model_type = model_type
        if model_type == "ollama":
            self.llm = ChatOllama(model=name, temperature=temperature)
            self.time4sleep = 0
        elif model_type == "openai":
            if "OPENAI_API_KEY" not in os.environ:
                raise ValueError("Please setup OPENAI_API_KEY")
            self.time4sleep = 5  # GPT-4 has rate limits. Be careful not to hit them.
            self.llm = ChatOpenAI(model=name, temperature=temperature)
        elif model_type == "anthropic":
            if "ANTHROPIC_API_KEY" not in os.environ:
                raise ValueError("Please setup ANTHROPIC_API_KEY")
            self.time4sleep = 2 # Adjust as needed based on observed rate limits
            self.llm = ChatAnthropic(model=name, temperature=temperature)
        elif model_type == "googlegenai":
            if "GOOGLE_API_KEY" not in os.environ and "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
                raise ValueError("Please set up either GOOGLE_API_KEY or GOOGLE_APPLICATION_CREDENTIALS environment variable.")
            self.time4sleep = 2  # Adjust as needed
            self.llm = GoogleGenerativeAI(model=name, temperature=temperature)
        else:
            raise ValueError("Unsupported model type. Use 'ollama', 'openai', 'anthropic', or 'googlepalm'.")

        self.chain = prompt_tpl | self.llm


    def __call__(self, **kwargs: dict) -> Any:
        """
        Invoke the LLM model with provided arguments.

        Args:
            **kwargs: Arbitrary keyword arguments for the model.

        Returns:
            str: The response from the model.
        """
        time.sleep(self.time4sleep)
        response = self.chain.invoke(
            kwargs, config={'callbacks': [ConsoleCallbackHandler()] if DEBUG else []}
        )
        if self.model_type != 'googlegenai':
            print(f"Total tokens: {response.usage_metadata['total_tokens']}")
        return response


def get_script_content(script_path: str) -> str:
    """
    Read the content of a Python script file.

    Args:
        script_path (str): Path to the script file.

    Returns:
        str: The content of the script file.
    """
    with open(script_path, 'r') as file:
        return file.read()


def run_program(program_path: str) -> Tuple[str, str, int, bool]:
    """
    Execute a Python script and measure its execution time.

    Args:
        program_path (str): Path to the Python script.

    Returns:
        Tuple[str, str, int, bool]: Output, error message, execution time in microseconds, and error status.
    """
    start_time = time.time()
    result = subprocess.run(['python3', program_path], capture_output=True, text=True)
    end_time = time.time()
    execution_time = int((end_time - start_time) * 1_000_000)  # Convert to microseconds
    error_occurred = result.returncode != 0
    return result.stdout, result.stderr, execution_time, error_occurred


def create_exp_folder(run_folder: Optional[str] = None) -> str:
    """
    Create a new experiment folder with a unique name.

    Args:
        run_folder (Optional[str]): Base folder path for experiments. Defaults to './run'.

    Returns:
        str: Path to the newly created experiment folder.
    """
    if run_folder is None:
        run_folder = "./run"
    if not os.path.exists(run_folder):
        os.makedirs(run_folder)
    exp_folders = [f for f in os.listdir(run_folder) if f.startswith("exp") and f[3:].isdigit() and len(f) == 7]
    if exp_folders:
        exp_numbers = [int(folder[3:]) for folder in exp_folders]
        next_exp_number = max(exp_numbers) + 1
    else:
        next_exp_number = 1
    next_exp_folder = f"exp{next_exp_number:04d}"
    next_exp_path = os.path.join(run_folder, next_exp_folder)
    os.makedirs(next_exp_path)
    return next_exp_path


def save_and_run_optimized_script(script_path: str, exp_folder_path: str, optimized_script: str,
                                  iteration_number: int) -> Tuple[str, str, int, bool]:
    """
    Save an optimized script to a file and execute it.

    Args:
        script_path (str): Path to the original script.
        exp_folder_path (str): Path to the experiment folder.
        optimized_script (str): The optimized script content.
        iteration_number (int): Current iteration number.

    Returns:
        Tuple[str, str, int, bool]: Output, error message, execution time in microseconds, and error status.
    """
    script_name = os.path.splitext(os.path.basename(script_path))[0]
    new_script_path = os.path.join(exp_folder_path, f"{script_name}_epoch_{iteration_number}.py")
    with open(new_script_path, 'w') as file:
        file.write(optimized_script)
    return run_program(new_script_path)


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """Hi. Your role is Senior python3 developer and your task is to help a user to optimise his python script by execution time - reduce
execution time as much as possible. You should use all your knowledge about Python3 and think as deeply as you can. Users will do it iteratively.

User will send you data in this pattern:

            base_code: ```CODE_HERE``` -  the code that the user have from the beginning and tries to optimise.
	        base_extime: ```Integer, Time in microseconds``` -  execution time of base_code
            two_iterations_ago_code: ```CODE_HERE``` -  two iterations ago python code that you wrote
            two_iterations_ago_extime: ```Integer, Time in microseconds``` - execution time of two_iterations_ago_code
            prev_iteration_code ```CODE_HERE``` - previous iteration python code that you wrote
            prev_iteration_extime: ```Integer, Time in microseconds``` - execution time of prev_iteration_code
            prev_iteration_execution_error: ```True|False``` - This variable shows that prev_iteration_code returned an error. It means your prev_iteration_code can’t be launched on the user's PC. 
            prev_iteration_error_description: ```Error description or None``` - if prev_iteration_execution_error = True you have error description. What went wrong on the user's PC.
            reference_result: ```STRUCTURED_TEXT_HERE``` - the script that you try to optimise returns some results and this is the reference result - result that returns base script w/o any optimisations.
            prev_iteration_results: ```STRUCTURED_TEXT_HERE``` - results of script that you wrote on previous iteration. 

            CONDITIONS:
                1. User send you code and execution time, you return user new version of script, user execute it on his side and provide you result as
prev_iteration_code and prev_iteration_extime (execution time). Also users always provide you base_code and base_extime as a reference. At the first iteration prev_iteration_code = base_code and prev_iteration_extime = base_extime
                2. After the first iteration, a user provides you with two versions of the script that you sent to the user (prev_iteration_code,
prev_iteration_extime) and (two_iterations_ago_code, two_iterations_ago_extime) . Please analyse them and keep in mind what approaches you already tried.
                3. Find the best solution for minimising execution time base on p.1 and p.2
                4. Return to a user a new script w/o any explanation and any additional tags. send back just a new version of scrip.
                5. You are able to add any python3 libraries that you think may improve performance.
                6. If you don’t see significant changes in execution time,  try some different approaches.
                7. If you receive prev_iteration_execution_error=True and
prev_iteration_error_description=```error stack trace```. It means your code works incorrectly. In this case you should analyse possible issues and create new version w/o
errors.
                8. You will receive reference_result - results of the initial script and prev_iteration_results - results from your prev
iteration code. Results should be equal. Please note If they don’t equal it means your script works incorrectly even if it has better execution time.
You should analyse and fix the issue.
                9. In every new script that you create you should add dockstring as the fist statement of the script  where you should write your chain of thought. You should write step by step why you think the version that you offer will work better than the previous version. 
                10. If you notice that the previous version worked incorrectly (you see current_iteration_execution_error and error_description) please add to documentation. ```I noticed that the previous version works incorrectly. I analysed the issue and fixed it. Also I understand that I shouldn’t take to account execution time of not working version```
                11. If you notice that the previous version has different results with reference results  please add to documentation. ```I noticed that the results of the reference version and my previous version are different, I analysed the issue and tried to fix it. So results should be the same in current version."""),
        ("human", """base_code: ```{base_code}```,
                     base_extime: {base_extime},
                     two_iterations_ago_code: ```{two_iterations_ago_code}```,
                     two_iterations_ago_extime: {two_iterations_ago_extime}
                     prev_iteration_code: ```{prev_iteration_code}```,
                     prev_iteration_extime: {prev_iteration_extime},
                     prev_iteration_execution_error: {prev_iteration_execution_error},
                     prev_iteration_error_description: {prev_iteration_error_description},
                     reference_results: ```{reference_results}```,
                     prev_iteration_results: ```{prev_iteration_results}```""")
    ]
)


def main() -> None:
    """Main function."""
    parser = argparse.ArgumentParser(description='Optimize Python script execution time.')
    parser.add_argument('--debug', required=False, action='store_true', help='Enable LLM detail output')
    parser.add_argument('--program', required=True, help='Path to the Python script to optimize')
    parser.add_argument('--steps', type=int, default=50, help='Number of optimisation steps you want to try')
    parser.add_argument('--model', required=True, choices=['ollama', 'openai', 'anthropic', 'googlegenai'], help='Select the model to use')
    parser.add_argument('--model_name', required=True, help='Specify the model name for the selected backend')
    global DEBUG
    args = parser.parse_args()
    DEBUG = args.debug
    steps = args.steps
    base_code = get_script_content(args.program)
    iteration_number = 0
    llm_interface = LLMInterface(
        model_type=args.model,
        prompt_tpl=prompt,
        name=args.model_name,
        temperature=1.0
    )
    exp_path = create_exp_folder()
    reference_results, _, base_extime, _ = run_program(args.program)

    print(f"Iteration Initial: Execution Time: {base_extime} microseconds")
    two_iterations_ago_code = ''
    two_iterations_ago_extime = 0
    prev_iteration_code = base_code
    prev_iteration_extime = base_extime
    prev_iteration_execution_error = False
    prev_iteration_error_description = ''
    output = reference_results
    results: List[Dict[str, any]] = []

    while steps > 0:
        llm_response = llm_interface(
            base_code=base_code,
            base_extime=base_extime,
            two_iterations_ago_code=two_iterations_ago_code,
            two_iterations_ago_extime=two_iterations_ago_extime,
            prev_iteration_code=prev_iteration_code,
            prev_iteration_extime=prev_iteration_extime,
            prev_iteration_execution_error=prev_iteration_execution_error,
            prev_iteration_error_description=prev_iteration_error_description,
            reference_results=reference_results,
            prev_iteration_results=output
        )
        if args.model != 'googlegenai':
            script_content = llm_response.content.strip().strip("```").strip("python")
        else:
            script_content = llm_response.strip().strip("```").strip("python")
        output, error, execution_time, execution_error = save_and_run_optimized_script(
            args.program, exp_path, script_content, iteration_number
        )

        print(f"Iteration {iteration_number}: Execution Time: {execution_time} microseconds")
        if execution_error:
            prev_iteration_execution_error = execution_error
            print(f"Error during execution: {error}")
        elif reference_results != output and not execution_error:
            print("Output mismatch error:", error)
        results.append({
            "iteration": iteration_number,
            "execution_time": execution_time,
            "execution_error": execution_error
        })
        iteration_number += 1
        steps -= 1

    filtered_results = [res for res in results if not res['output_issue'] and not res['execution_error']]
    sorted_filtered_results = sorted(filtered_results, key=lambda x: x['execution_time'])
    print(
        f"Last results: execution_time {filtered_results[-1]['execution_time']} "
        f"iteration: {filtered_results[-1]['iteration']}")
    print(
        f"The best results: execution_time {sorted_filtered_results[0]['execution_time']} "
        f"iteration: {sorted_filtered_results[0]['iteration']}")


if __name__ == "__main__":
    main()

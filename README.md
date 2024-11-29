# Python Code Optimizer

This project explores how various Large Language Models (LLMs) can optimize 
Python 3 code by improving performance (reduce execution time). 
The primary script runs code in a subprocess, gathers execution metrics 
(e.g., execution time), and sends these to an LLM for iterative optimization.

## Getting Started

1. **Set up a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements
   ```
3. **Set up API keys for the desired LLMs:**
   ```bash
   export OPENAI_API_KEY=your_openai_api_key
   export ANTHROPIC_API_KEY=your_anthropic_api_key
   export GOOGLE_API_KEY=your_google_ai_studio_api_key
   ```
4. **Install Ollama locally:** Follow the instructions at [Ollama GitHub Repository](https://github.com/ollama/ollama?tab=readme-ov-file#linux).
In experiments, the Qwen2.5 Coder 14B model with extended context was used. 
5. Ensure your script meets the following criteria:

    * It should run successfully via subprocess
    * it shouldn't be a daemon (run endlessly)
    * It should output results to stdout (used as a reference for optimization quality).
> **Note:**  
> You don't need to provide all API keys. Set only the keys for the LLMs you plan to use.

## Running the Optimizer

### Ollama: 

```bash 
python3 main.py --program script_fapi.py --model ollama --model_name qwen2.5-coder-8K-ctx:14b --steps 20
  ```
see below how to create model with  [large context](#Ollama model creation). 

### Launch openai
```bash 
python3 main.py --program script_fapi.py --model openai --model_name gpt-4o --steps 20
```

### Launch googlegenai
```bash
python3 main.py --program script_fapi.py --model googlegenai  --model_name gemini-pro --steps 20
```

## Launch anthropic
```bash
python3 main.py --program script_fapi.py --model anthropic --model_name claude-3-5-sonnet-20241022  --steps 20
```
> Output:  
> Results of optimisation will be placed into ./run/expNum folder. 


## Logic explanation
At each iteration:
1. The script specified via the --program argument is executed in a subprocess.
2. The LLM receives:
   * Metadata about the execution:
     * base_code: The initial code version.
     * base_extime: Execution time (in microseconds) of the base code.
     * two_iterations_ago_code: Code from two iterations prior (if applicable).
     * two_iterations_ago_extime: Execution time of the code from two iterations prior.
     * prev_iteration_code: Code from the previous iteration.
     * prev_iteration_extime: Execution time of the code from the previous iteration.
     * prev_iteration_execution_error: Whether the previous iteration encountered an error.
     * prev_iteration_error_description: Details of the error, if any.
     * reference_results: Output from the base script (used as a reference).
     * prev_iteration_results: Results from the previous iteration.
3. The LLM analyzes this data to:
  * Optimize performance.
  * Fix errors (if present).
  * Suggest a new, improved code version.
  * LLM returns python code and chain of thought like module documentation.

## Prompt
```python
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
```

## Example Scripts
The repository includes examples of inefficient Python scripts to demonstrate optimization:

1. script.py: Reads an Nginx access log and groups data by HTTP request type.
2. script_fapi.py: Launches a FastAPI instance, processes a complex JSON request, and completes execution after one API call.
3. script_ohlcv.py: Fetches OHLCV data for 10 cryptocurrencies from Binance.
4. script_sorting.py: Implements an inefficient sorting algorithm.

In the folder ./run/exp0025 example of script_fapi.py optimisation by claude-3-5-sonnet-20241022

## Code optimiser options: 
* ```--debug``` - enables detailed LLM output.
* ```--program``` - Path to the Python script to optimize
* ```--steps``` - Number of optimization iterations.
* ```--model``` - Specifies the LLM backend (```ollama```, ```openai```, ```anthropic```, ```googlegenai```)
* ```--model_name``` - Specifies the model name for the chosen backend.


## Limitations

1. **Dependency Installation**:  
   New dependencies suggested by the model are not installed automatically. Install them manually if necessary and re-run the optimizer.

2. **Model Context Size**:  
   Context size varies across LLMs. Large scripts may exceed the model's context size, leading to errors or suboptimal results. Ensure that your script's size (multiplied by 3, as three code versions are included in the prompt) fits within the model's context limit:
   - **Ollama Qwen2.5 Coder 14B**: Default context is 2048 tokens (can be extended via a Modelfile).
   - **OpenAI GPT-4o**: 8192 tokens.
   - **Google GenAI (Gemini Pro)**: Very large context (up to 2 million tokens).
   - **Anthropic (Sonnet)**: 200,000 tokens.

3. **Redundancy in `requirements.txt`**:  
   Some dependencies (e.g., `pandas`) may not be directly required but are included as the LLM might utilize them during optimization.

## Ollama model creation:
```bash
ollama create qwen2.5-coder-8K-ctx:14b -f ./Modelfile
```
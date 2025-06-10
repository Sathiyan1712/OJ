from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from submit.forms import submitform
from submit.models import CodeSubmit
from Teachers.models import Problem, ProblemSolved
from django.conf import settings
import os
import uuid
import subprocess
from pathlib import Path
import google.generativeai as genai # Import the Gemini library
from django.conf import settings
# ...
genai.configure(api_key=settings.GEMINI_API_KEY)



# genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY"))

# Create your views here.

# def Result_view(request):
#     if request.user.is_authenticated:
#         if request.user.is_teacher:
#             base_template = "base.html"
#         else:
#             base_template = "base1.html"
#     else:
#         base_template= "base1.html"
#     return render(request, "Result.html", {'base_template':base_template})

@login_required
def submit(request, problem_id = None):
    if request.user.is_authenticated:
                if request.user.profile.user_type=="teacher":
                    base_template = "base.html"
                else:
                    base_template = "base1.html"
    else:
        base_template= "base1.html"
#    ?why?
    problem = None
    if problem_id:
         problem = get_object_or_404(Problem, id = problem_id)

    submission_ = None 
    message = None     
    show_ai_review = False 
    

    if request.method == "POST":
        form = submitform(request.POST)
        if form.is_valid():
            
            submission = form.save(commit = False)
            submission.user = request.user
            submission.problem= problem
            action = request.POST.get("action")
            if action == "run":
                Output = running_code
                print(submission.language)
                print (submission.code)
                output= running_code( submission.language, submission.code, submission.input or "")
                submission.output = output
                
                message = "Output for manual input"
                
                
            elif action == "submit" and problem:
                sample_input = problem.sample_input or ""
                expected_output = problem.expected_output or ""
                show_ai_review = True
                output = running_code(submission.language, submission.code, sample_input)
                submission.input = sample_input
                submission.output = output
                submission.save()
                submission_=submission

                if output.strip() == expected_output.strip():
                    ProblemSolved.objects.get_or_create(user=request.user, problem=problem)
                    submission.is_correct=True
                    message = "Submitted Successfully! Your solution is correct."

                else:
                     submission.is_correct=False
                     message = (
                         " Wrong Answer\n"
                         f"<strong>Expected:</strong>\n<pre>{expected_output}</pre>\n"
                         f"<strong>Your Output:</strong>\n<pre>{output}</pre>"
                     )
                 
                submission.save()
                submission_=submission
                    #message = "Wrong Answer or Output does not match the expected output."
            else:
                 message = "Invalid action or problem not specified for submission."
            if action == "run":
                submission.save()
                submission_ = submission  
                return render(request, "Result.html", {"form":submitform(), "submission_" : submission_, 'base_template':base_template, "message":message, "problem":problem})          
            
            return render(request, "compiler.html", {
                "form": submitform(instance=submission), # Pre-populate form with submission details if needed
                "submission_": submission_,
                'base_template': base_template,
                "message": message,
                "problem": problem,
                "show_ai_review": show_ai_review # Pass the flag
            })
        
    else:
            form = submitform()
    return render(request, "compiler.html", {
        "form": form,
        'base_template': base_template,
        "problem": problem,
        "submission_": submission_, # Will be None on initial load
        "message": message,         # Will be None on initial load
        "show_ai_review": show_ai_review # Will be False on initial load
    })
        

def running_code(language, code, input_data):
    project_path = Path(settings.BASE_DIR)
    directories = ["code","inputs", "outputs"]
    
    for direct in directories:
        dir_path = project_path/direct
        if not dir_path.exists():
             dir_path.mkdir(parents=True, exist_ok= True)

    codes_dir = project_path/"code"
    inputs_dir = project_path/"inputs"
    outputs_dir = project_path/"outputs"

    unique = str(uuid.uuid4())

    code_file_name = f"{unique}.{language}"
    input_file_name = f"{unique}.txt"
    output_file_name =f"{unique}.txt"

    code_file_path = codes_dir/code_file_name
    input_file_path = inputs_dir/input_file_name
    output_file_path = outputs_dir/output_file_name

    with open(code_file_path, "w") as codefile:
        codefile.write(code)

    with open(input_file_path, "w") as inputfile:
        inputfile.write(input_data)
    




    output = ""
    error = ""

    try:
        if language == "cpp":
            # Compile C++ code
            executable_path = codes_dir/unique
            compile_result = subprocess.run(
                ["g++", str(code_file_path), "-o", str(executable_path)],
                capture_output=True,
                text=True
            )
            
            if compile_result.returncode != 0:
                output = f"Compilation Error:\n{compile_result.stderr}"
            else:
                # Run compiled executable
                run_result = subprocess.run(
                    [str(executable_path)],
                    input=input_data,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                output = run_result.stdout
                if run_result.stderr:
                    output += f"\nRuntime Error:\n{run_result.stderr}"

        elif language == "py":
            # Execute Python code
            run_result = subprocess.run(
                ["python", "-u", str(code_file_path)],
                input=input,
                capture_output=True,
                text=True,
                timeout=10
            )
            output = run_result.stdout
            if run_result.stderr:
                output += f"\nRuntime Error:\n{run_result.stderr}"

    except subprocess.TimeoutExpired:
        output = "Time Limit Exceeded (10 seconds)"
    except Exception as e:
        output = f"Unexpected Error: {str(e)}"

    # Write final output to file
    with open(output_file_path, "w") as f:
        f.write(output)

    return output




@login_required
def ai_review_code(request, submission_id):
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
    submission = get_object_or_404(CodeSubmit, pk=submission_id, user=request.user)

    # Fetch the problem details for context
    problem = submission.problem
    problem_statement = problem.description if problem else "No problem statement available."

    # Prepare the prompt for Gemini
    prompt = f"""
    You are an AI code reviewer for an online judge.
    The user submitted the following code to solve a problem.

    **Problem Statement:**
    {problem_statement}

    **Submitted Code ({submission.language}):**
    ```{"python" if submission.language == "py" else "cpp"}
    {submission.code}
    ```

    **Input used for validation:**
    ```
    {submission.input}
    ```

    **Your Code's Output:**
    ```
    {submission.output}
    ```

    **Expected Output (if available):**
    ```
    {problem.expected_output if problem and problem.expected_output else "Not provided for this review."}
    ```

    Please provide a comprehensive review of the submitted code.
    Focus on:
    1.  **Correctness:** Does the code logically solve the problem? Point out any flaws leading to incorrect outputs.
    2.  **Efficiency:** Can the code be made more efficient (time complexity, space complexity)? Suggest improvements.
    3.  **Readability and Style:** Is the code easy to understand? Suggest improvements for variable names, comments, and overall structure.
    4.  **Edge Cases:** Does the code handle potential edge cases correctly?
    5.  **Potential Bugs:** Identify any subtle bugs that might not be caught by simple tests.

    Provide an improved version of the code if possible, clearly indicating the changes and why they are improvements.
    If the code is already perfect, explain why.
    """
    
    ai_response_text = ""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        ai_response_text = response.text
    except Exception as e:
        ai_response_text = f"An error occurred while generating AI review: {e}"

    if request.user.profile.user_type == "teacher":
        base_template = "base.html"
    else:
        base_template = "base1.html"

    return render(request, 'ai_review_result.html', {
        'submission': submission,
        'ai_review': ai_response_text,
        'base_template': base_template,
        'problem': problem
    })



    # with open(output_file_path, "w") as outputfile:
    #     pass

    # if language=="cpp":
    #     executable_path = codes_dir/unique
    #     compile_result = subprocess.run(
    #         ["g++", str(code_file_path), "-o", str(executable_path)]
            
    #     )
    #     if compile_result.returncode==0:
    #         with open(input_file_path, "r") as input_file:
    #             with open(output_file_path, "w") as output_file:
    #                 subprocess.run(
    #                     [str(executable_path)],
    #                     stdin=input_file,
    #                     stdout= output_file,   
    #                 )
    # elif language == "py":
    #     with open(input_file_path, "r") as input_file:
    #         with open(output_file_path, "w") as output_file:
    #              subprocess.run(
    #                 ["python", '-u' ,str(code_file_path)],
    #                 stdin=input_file,
    #                 stdout=output_file,
    #                 stderr=subprocess.STDOUT,
    #             )
                 
    # with open(output_file_path, "r")as output_file:
    #     output= output_file.read()

    # return output
        
from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Problem
from .forms import ProblemForm
from Teachers.models import ProblemSolved
from submit.models import CodeSubmit
from django.conf import settings
import os
import uuid
from pathlib import Path
# Create your views here.
def is_teacher(user):
    return hasattr(user, 'profile') and user.profile.user_type =='teacher'

@login_required
@user_passes_test(is_teacher)
def teacher_home(request):
    return render(request, 'teacher_dashboard.html')

#PROBLEM

@login_required
@user_passes_test(is_teacher)
def problems(request):
    problems = Problem.objects.all()
    solved_ids = set()

    if request.user.is_authenticated:
        solved_ids = set(ProblemSolved.objects.filter(user=request.user).values_list('problem_id', flat=True))

    for prob in problems:
        prob.is_solved = prob.id in solved_ids

    return render(request, "Problems.html", {"problems": problems})


#PROBLEM DETTAIL
@login_required
@user_passes_test(is_teacher)
def problem_detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    return render(request, 'problem_detail.html', {'problem':problem})


#ADD PROBLEM

@login_required
@user_passes_test(is_teacher)
def add_problem(request):
    if request.method == "POST":
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.created_by= (request.user)
            import re
            if problem.example:
                
                problem.example = re.sub(r"(Example\d+:)", r"\n\1", problem.example)
            problem.created_by= (request.user)
            problem.save()

            project_path = Path(settings.BASE_DIR)
            directories = ["sample_input","expected_output"]
            
            for direct in directories:
                dir_path = project_path/direct
                if not dir_path.exists():
                     dir_path.mkdir(parents=True, exist_ok= True)
        
            samp_in_dir = project_path/"sample_input"
            exp_out_dir = project_path/"expected_output"
            
        
            unique = str(uuid.uuid4())
        
            
            sample_input_file_name = f"{unique}.txt"
            expected_output_file_name =f"{unique}.txt"
        
            
            sample_input_file_path = samp_in_dir/sample_input_file_name
            expected_output_file_path = exp_out_dir/expected_output_file_name
            
            if problem.sample_input:
                with open(sample_input_file_path, "w") as sampfile:
                    sampfile.write(problem.sample_input)


            if problem.expected_output:

                with open(expected_output_file_path, "w") as expfile:
                    expfile.write(problem.expected_output)
            

            return redirect('problems')
    else:
        form =ProblemForm()

    return render (request, 'Add_Problem.html', {'form':form})




#REMOVE PROBLEM

@login_required
@user_passes_test(is_teacher)
def remove_problem(request):
    if request.method == "POST":
        problem_iud = request.POST.get('problem_iud')
        proble = get_object_or_404(Problem, id = problem_iud)
        proble.delete()
        return redirect('problems')
    else:
        problems = Problem.objects.all()
        return render (request, 'Remove_Problem.html', {'problems': problems})





#problem submission
@login_required
@user_passes_test(is_teacher)
def Tproblem_submissions(request, pk):
    problem = get_object_or_404(Problem, pk = pk)
    submissions = CodeSubmit.objects.filter(user=request.user, problem=problem).order_by('timestamp')
    return render(request, 'Tproblem_submissions.html', {
        'problem':problem,
        'submissions': submissions,
    })




@login_required
@user_passes_test(is_teacher)
def Tview_code_submission(request, submission_id):
    submission = get_object_or_404(CodeSubmit, pk=submission_id, user=request.user)
    return render(request, 'Tview_code_submission.html', {'submission': submission})
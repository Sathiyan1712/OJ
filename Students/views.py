from django.shortcuts import render, get_object_or_404
from Teachers.models import Problem, ProblemSolved

from submit.views import running_code
from submit.models import CodeSubmit
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import StudentSubmitForm


# Create your views here.

def is_student(user):
    return hasattr(user, 'profile') and user.profile.user_type == 'student'

@login_required
@user_passes_test(is_student)
def student_home(request):
    return render (request,'StudentsDashboard.html')


# @login_required
# @user_passes_test(is_student)
# def Student_Problem(request):
#     problems = Problem.objects.all()
#     return render(request, 'Studproblem.html', {'problems':problems})



@login_required
@user_passes_test(is_student)
def Student_Problem(request):
    problems = Problem.objects.all()
    solved_ids = set()

    if request.user.is_authenticated:
        solved_ids = set(ProblemSolved.objects.filter(user=request.user).values_list('problem_id', flat=True))

    for prob in problems:
        prob.is_solved = prob.id in solved_ids

    return render(request, "Studproblem.html", {"problems": problems})



@login_required
@user_passes_test(is_student)
def ProblemDetail(request, pk):
    problem = get_object_or_404(Problem, pk = pk)
    return render(request, 'Problemdetail.html', {'problem':problem})


#problem submission
@login_required
@user_passes_test(is_student)
def problem_submissions(request, pk):
    problem = get_object_or_404(Problem, pk = pk)
    submissions = CodeSubmit.objects.filter(user=request.user, problem=problem).order_by('timestamp')
    return render(request, 'problem_submissions.html', {
        'problem':problem,
        'submissions': submissions,
    })




@login_required
@user_passes_test(is_student)
def view_code_submission(request, submission_id):
    submission = get_object_or_404(CodeSubmit, pk=submission_id, user=request.user)
    return render(request, 'viewcode.html', {'submission': submission})

# @login_required
# @user_passes_test(is_student)
# def Solve_problem(request, pk):

#     problem = get_object_or_404(Problem, pk = pk)
    
#     if request.method == 'POST':
#         form = StudentSubmitForm(request.POST)
#         if form.is_valid():
#             submission = form.save(commit=False)
#             submission.output = running_code(submission.language, submission.code, submission.input)
#             submission.save()
#             return render(request, 'Result.html', {'submission' : submission})
#     else :
#         form = StudentSubmitForm()

#     return render(request, 'Compiler.html', {'form': form})
    


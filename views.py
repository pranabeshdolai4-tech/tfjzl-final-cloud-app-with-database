from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

# Course details / exam view
def course_details(request, course_id):
    context = {}
    if request.method == 'GET':
        try:
            course = Course.objects.get(pk=course_id)
            context['course'] = course
            return render(request, 'onlinecourse/course_details_bootstrap.html', context)
        except Course.DoesNotExist:
            return render(request, 'onlinecourse/course_details_bootstrap.html', context)


# Task 5: submit function
def submit(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        user = request.user

        # Fetch active enrollment for the user
        enrollment = Enrollment.objects.get(user=user, course=course)

        # Create a new submission instance
        submission = Submission.objects.create(enrollment=enrollment)

        # Collect selected choices from POST payload
        selected_choice_ids = []
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                selected_choice_ids.append(int(value))

        # Retrieve choice objects and attach to submission
        for choice_id in selected_choice_ids:
            choice = Choice.objects.get(pk=choice_id)
            submission.choices.add(choice)

        submission.save()
        return HttpResponseRedirect(reverse('onlinecourse:show_exam_result', args=(course.id, submission.id)))

    return redirect('onlinecourse:course_details', course_id=course_id)


# Task 5: show_exam_result function
def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    # Calculate total exam grade and user score
    total_score = 0
    earned_score = 0

    # Retrieve all submitted choices
    selected_choices = submission.choices.all()
    selected_choice_ids = [choice.id for choice in selected_choices]

    for lesson in course.lesson_set.all():
        for question in lesson.question_set.all():
            total_score += question.grade
            if question.is_get_score(selected_choice_ids):
                earned_score += question.grade

    context['course'] = course
    context['submission'] = submission
    context['total_score'] = total_score
    context['earned_score'] = earned_score
    context['selected_ids'] = selected_choice_ids

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
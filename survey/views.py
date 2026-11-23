from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

from .forms import SurveyResponseForm
from .models import SurveyResponse


def home(request):
    if request.method == 'POST':
        form = SurveyResponseForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your survey response was submitted successfully!')
            return redirect('home')
    else:
        form = SurveyResponseForm()

    return render(request, 'survey/home.html', {'form': form})


@login_required
def results(request):
    responses = SurveyResponse.objects.all().order_by('-submitted_at')

    total_responses = responses.count()

    average_rating = responses.aggregate(
        average=Avg('rating')
    )['average']

    context = {
        'responses': responses,
        'total_responses': total_responses,
        'average_rating': average_rating,
    }

    return render(request, 'survey/results.html', context)
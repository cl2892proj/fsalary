from django.shortcuts import render, get_object_or_404

# Create your views here.

from .models import Review, Hire

def index(request):
    context = {}
    return render(request, 'reviews/base.html', context)


def hiring_detail(request, hire_id):
    hire = get_object_or_404(Hire, id=hire_id)
    review_list = Review.objects.filter(hire_id=hire_id)
    context = {'hire':hire, 'review_list':review_list}
    return render(request, 'reviews/hiring_detail.html', context)
    

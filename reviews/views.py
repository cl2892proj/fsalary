from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Review, Hire
from .forms import ReviewForm
import datetime

def index(request):
    context = {}
    return render(request, 'reviews/base.html', context)


def hiring_detail(request, hire_id):
    hire = get_object_or_404(Hire, id=hire_id)
    review_list = Review.objects.filter(hire_id=hire_id)
    context = {'hire':hire, 'review_list':review_list, 'form':ReviewForm()}
    return render(request, 'reviews/hiring_detail.html', context)
    
def add_review(request, hire_id):
    hire = get_object_or_404(Hire, id=hire_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        comment = form.cleaned_data['comment']
        review = Review()
        review.hire = hire
        review.pub_date = datetime.datetime.now()
        review.user_name = 'user1'
        review.comment = comment
        review.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reviews:hiring_detail', args=(hire.id,)))
    review_list = Review.objects.filter(hire_id=hire_id)
    context = {'hire':hire, 'review_list':review_list, 'form':form}
    return render(request, 'reviews/hiring_detail.html',context)
        




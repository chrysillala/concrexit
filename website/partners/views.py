from django.shortcuts import get_object_or_404, render

from partners.models import Partner, Vacancy, VacancyCategory
from random import random


def index(request):
    partners = Partner.objects.filter(is_active=True, is_main_partner=False)

    context = {
        'main_partner': Partner.objects.get(
            is_active=True,
            is_main_partner=True
        ),
        'partners': sorted(partners, key=lambda x: random()),
    }
    return render(request, 'partners/index.html', context)


def partner(request, slug):
    partner = get_object_or_404(Partner, slug=slug)
    context = {
        'partner': partner,
        'vacancies': Vacancy.objects.filter(partner=partner),
    }
    return render(request, 'partners/partner.html', context)


def vacancies(request):
    context = {
        'vacancies': Vacancy.objects.all(),
        'categories': VacancyCategory.objects.all(),
    }

    return render(request, 'partners/vacancies.html', context)
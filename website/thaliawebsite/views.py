from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import (HttpResponseBadRequest,
                         HttpResponseForbidden, JsonResponse)
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.debug import (sensitive_variables,
                                           sensitive_post_parameters)

from members.models import Member


@login_required
def styleguide(request):
    return render(request, 'singlepages/styleguide.html')


@sensitive_variables()
@sensitive_post_parameters()
@require_POST
@csrf_exempt
def wiki_login(request):
    apikey = request.POST.get('apikey')
    user = request.POST.get('user')
    password = request.POST.get('password')

    if apikey != settings.WIKI_API_KEY:
        return HttpResponseForbidden('{"status":"error","msg":"invalid key"}')
    if user is None or password is None:
        return HttpResponseBadRequest(
            '{"status":"error","msg":"Missing username or password"}',
            content_type='application/json')

    user = authenticate(username=user, password=password)
    if user is not None:
        try:
            memberships = [cmm.committee.wiki_namespace for cmm in
                           user.member.committeemembership_set.exclude(
                               until__lt=timezone.now().date())
                           .select_related('committee')
                           if cmm.committee.wiki_namespace is not None]
        except Member.DoesNotExist:
            memberships = []

        return JsonResponse({'status': 'ok',
                             'name': user.get_full_name(),
                             'mail': user.email,
                             'admin': user.is_superuser,
                             'msg': 'Logged in',
                             'committees': memberships})
    return JsonResponse({'status': 'error',
                         'msg': 'Authentication Failed'},
                        status=403)


@staff_member_required
def crash(request):
    raise Exception("Test exception")

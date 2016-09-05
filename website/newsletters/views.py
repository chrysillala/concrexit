from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, render, redirect
from django.template import Context
from django.template.loader import get_template
from django.utils import translation
from members.models import Member
from newsletters.models import Newsletter
from partners.models import Partner


@login_required
def preview(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    partners = Partner.objects.filter(is_main_partner=True)
    main_partner = partners[0] if len(partners) > 0 else None

    return render(request, 'newsletters/email.html', {
        'newsletter': newsletter,
        'main_partner': main_partner,
        'lang_code': request.LANGUAGE_CODE
    })


@staff_member_required
@permission_required('newsletters.change_event')
def admin_send(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)

    if newsletter.sent:
        return redirect(newsletter)

    if request.POST:
        partners = Partner.objects.filter(is_main_partner=True)
        main_partner = partners[0] if len(partners) > 0 else None

        from_email = settings.NEWSLETTER_FROM_ADDRESS
        html_template = get_template('newsletters/email.html')
        text_template = get_template('newsletters/email.txt')

        for language in settings.LANGUAGES:
            translation.activate(language[0])

            recipients = [member.user.email for member in
                          Member.objects.all().filter(
                              receive_newsletter=True, language=language[0])
                          if member.is_active() is True]

            subject = newsletter.title
            html_message = html_template.render(Context({
                'newsletter': newsletter,
                'main_partner': main_partner,
                'lang_code': language,
                'request': request
            }))
            text_message = text_template.render(Context({
                'newsletter': newsletter,
                'main_partner': main_partner,
                'lang_code': language,
                'request': request
            }))

            msg = EmailMultiAlternatives(subject, text_message,
                                         to=[from_email],
                                         bcc=recipients,
                                         from_email=from_email)
            msg.attach_alternative(html_message, "text/html")
            msg.send()

            translation.deactivate()

        newsletter.sent = True
        newsletter.save()

        return redirect('admin:newsletters_newsletter_changelist')
    else:
        return render(request, 'newsletters/admin/send_confirm.html', {
            'newsletter': newsletter
        })
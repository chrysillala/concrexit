from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from events.models import Registration
from thaliawebsite.templatetags import baseurl


def notify_first_waiting(request, event):
    if (event.max_participants is not None and
        Registration.objects
                    .filter(event=event, date_cancelled=None)
                    .count() > event.max_participants):
        # Prepare email to send to the first person on the waiting list
        first_waiting = (Registration.objects
                         .filter(event=event, date_cancelled=None)
                         .order_by('date')[event.max_participants])
        first_waiting_member = first_waiting.member

        text_template = get_template('events/email.txt')

        with translation.override(first_waiting_member.language):
            subject = _("[THALIA] Notification about your "
                        "registration for '{}'").format(
                event.title)
            text_message = text_template.render({
                'event': event,
                'reg': first_waiting,
                'member': first_waiting_member,
                'base_url': baseurl.baseurl(request)
            })

            EmailMessage(
                subject,
                text_message,
                to=[first_waiting_member.user.email]
            ).send()
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, get_language

from events import emails
from events.exceptions import RegistrationError
from events.models import Registration, RegistrationInformationField


def is_user_registered(event, user):
    if not event.registration_required:
        return None

    return event.registrations.filter(
        member=user.member,
        date_cancelled=None).count() > 0


def event_permissions(user, event):
    perms = {
        "create_registration": False,
        "cancel_registration": False,
        "update_registration": False,
    }
    if user.is_authenticated and user.member.can_attend_events:
        registration = None
        try:
            registration = Registration.objects.get(
                event=event,
                member=user.member
            )
        except Registration.DoesNotExist:
            pass

        perms["create_registration"] = (
            (registration is None or registration.date_cancelled is not None)
            and event.registration_allowed)
        perms["cancel_registration"] = (
            registration is not None and
            registration.date_cancelled is None and
            event.cancellation_allowed)
        perms["update_registration"] = (
            registration is not None and
            registration.date_cancelled is None and event.has_fields() and
            event.registration_allowed)

    return perms


def is_organiser(user, event):
    if user.is_superuser or user.has_perm("events.override_organiser"):
        return True

    if event and user.has_perm('events.change_event'):
        committees = 0
        if event is not None:
            committees = user.member.get_committees().filter(
                pk=event.organiser.pk).count()
        return committees != 0

    return False


def create_registration(user, event):
    if event_permissions(user, event)["create_registration"]:
        registration = None
        try:
            registration = Registration.objects.get(
                event=event,
                member=user.member
            )
        except Registration.DoesNotExist:
            pass

        if registration is None:
            return Registration.objects.create(
                event=event,
                member=user.member
            )
        elif registration.date_cancelled is not None:
            if registration.is_late_cancellation():
                raise RegistrationError(_("You cannot re-register anymore "
                                          "since you've cancelled after the "
                                          "deadline."))
            else:
                registration.date = timezone.now()
                registration.date_cancelled = None
                registration.save()

        return registration
    elif event_permissions(user, event)["cancel_registration"]:
        raise RegistrationError(_("You were already registered."))
    else:
        raise RegistrationError(_("You may not register."))


def cancel_registration(request, user, event):
    registration = None
    try:
        registration = Registration.objects.get(
            event=event,
            member=user.member
        )
    except Registration.DoesNotExist:
        pass

    if event_permissions(user, event)["cancel_registration"] and registration:
        if registration.queue_position == 0:
            emails.notify_first_waiting(request, event)

        # Note that this doesn"t remove the values for the
        # information fields that the user entered upon registering.
        # But this is regarded as a feature, not a bug. Especially
        # since the values will still appear in the backend.
        registration.date_cancelled = timezone.now()
        registration.save()
    else:
        raise RegistrationError(_("You are not registered for this event."))


def update_registration(user, event, field_values):
    registration = None
    try:
        registration = Registration.objects.get(
            event=event,
            member=user.member
        )
    except Registration.DoesNotExist:
        pass

    if not registration:
        raise RegistrationError(_("You are not registered for this event."))

    if not event_permissions(user, event)["update_registration"]:
        return

    for field_id, field_value in field_values:
        field = RegistrationInformationField.objects.get(
            id=field_id.replace("info_field_", ""))

        if (field.type == RegistrationInformationField.INTEGER_FIELD
                and field_value is None):
            field_value = 0
        elif (field.type == RegistrationInformationField.BOOLEAN_FIELD
                and field_value is None):
            field_value = False
        elif (field.type == RegistrationInformationField.TEXT_FIELD
              and field_value is None):
            field_value = ''

        field.set_value_for(registration, field_value)


def registration_fields(user, event):
    registration = None
    try:
        registration = Registration.objects.get(
            event=event,
            member=user.member
        )
    except Registration.DoesNotExist:
        pass

    if event_permissions(user, event)["update_registration"] and registration:
        information_fields = registration.information_fields
        fields = {}

        for information_field in information_fields:
            field = information_field["field"]

            fields["info_field_{}".format(field.id)] = {
                "type": field.type,
                "label": getattr(field, "{}_{}".format(
                    "name",  get_language())),
                "description": getattr(field, "{}_{}".format(
                    "description", get_language())),
                "value": information_field["value"],
                "required": field.required
            }

        return fields
    else:
        raise RegistrationError(_("You are not registered for this event."))
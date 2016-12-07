from django import forms

from activemembers.models import CommitteeMembership
from members.models import Member


class CommitteeMembershipForm(forms.ModelForm):
    member = forms.ModelChoiceField(
        queryset=Member.objects.order_by('user__first_name',
                                         'user__last_name'))

    class Meta:
        model = CommitteeMembership
        exclude = ()

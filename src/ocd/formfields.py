from django.utils.safestring import mark_safe
import floppyforms.__future__ as forms


class HTMLArea(forms.Textarea):
    template_name = 'floppyforms/htmlarea.html'

    def get_context(self, name, value, attrs):
        ctx = super(HTMLArea, self).get_context(name, value, attrs)
        ctx['attrs']['rows'] = 4
        return ctx


class DateTimeLocalInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class OCSplitDateTime(forms.SplitDateTimeWidget):
    def render(self, name, value, attrs=None):
        html = super(OCSplitDateTime, self).render(name, value, attrs=attrs)
        return mark_safe('<span class="oc-dt-split">%s</span>' % html)


class OCSplitDateTimeField(forms.SplitDateTimeField):
    widget = OCSplitDateTime


class OCCheckboxSelectMultiple(forms.SelectMultiple):
    template_name = 'floppyforms/oc_checkbox_select.html'


class GroupCheckboxSelectMultiple(forms.SelectMultiple):
    template_name = 'floppyforms/groups_checkbox_select.html'


class OCIssueRadioButtons(forms.RadioSelect):
    template_name = 'floppyforms/oc_issue_radio_buttons.html'


class OCProposalRadioButtons(forms.RadioSelect):
    template_name = 'floppyforms/oc_proposal_radio_buttons.html'

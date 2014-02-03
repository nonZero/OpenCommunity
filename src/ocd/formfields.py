from django.utils.safestring import mark_safe
import floppyforms as forms


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
        return mark_safe("<span class=\"oc-dt-split\">%s</span>" % html)
        
class OCCheckboxSelectMultiple(forms.SelectMultiple):
    template_name = 'floppyforms/oc_checkbox_select.html'

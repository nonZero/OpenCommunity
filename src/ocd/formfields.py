import floppyforms as forms


class HTMLArea(forms.Textarea):
    template_name = 'floppyforms/htmlarea.html'


class DateTimeLocalInput(forms.DateTimeInput):
    input_type = 'datetime-local'

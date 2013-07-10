from ocd.validation import convert_to_html


def convert_html_fields(model_class, fields):
    converted = 0
    skipped = 0
    for o in model_class.objects.all():
        dirty = False
        for f in fields:
            if getattr(o, f):
                setattr(o, f, convert_to_html(getattr(o, f)))
                dirty = True
        if dirty:
            o.save()
            converted += 1
        else:
            skipped += 1

    return converted, skipped

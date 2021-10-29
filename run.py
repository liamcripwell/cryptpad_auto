import fire

from cryptpad_auto.forms import FormBuilder, FormTemplateBuilder


class Launcher(object):

    def form(self, template_file, data_file, out_file):
        """Build a CryptPad Form from a template and data."""
        builder = FormBuilder(template_file)
        builder.build(data_file)
        builder.to_file(out_file)

    def tempalte(self, form_file, out_file, data_groups=[]):
        """Build a CryptPad Form template from an existing form."""
        builder = FormTemplateBuilder(form_file)
        builder.build(data_groups)
        builder.to_file(out_file)


if __name__ == '__main__':
    fire.Fire(Launcher)
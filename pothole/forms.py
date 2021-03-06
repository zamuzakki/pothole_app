from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column, Button
from .models import Pothole, PotholeRepair

class PotholeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    Row(
                        Column('photo', css_class='col-12 col-sm-6 input-sm'),
                        Column('response_time_needed', css_class='col-12 col-sm-6 input-sm '),
                        css_class='row'
                    ),
                    css_class='col-md-12'
                ),
                css_class='form-row row'
            ),

            Row(
                Column(
                    Row(
                        Column('width', css_class='col-12 col-sm-6 input-sm'),
                        Column('depth', css_class='col-12 col-sm-6 input-sm'),
                        css_class='row'
                    ),
                    css_class='col-md-12'
                ),
                css_class='form-row row'
            ),
            Submit('submit', 'Save')
        )

    def save(self, *args, **kwargs):
        print(self.fields['width'])
        # super(PotholeForm, self).save(*args, **kwargs)

    class Meta:
        model = Pothole
        fields = '__all__'
        # exclude = ('geometry',)

class PotholeSearchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            # Row(
            #     Column('photo', css_class='form-group col-md-6 mb-0'),
            #     Column('response_time_needed', css_class='form-group col-md-6 mb-0'),
            #     css_class='form-row'
            # ),
            #
            # Row(
            #     Column('depth', css_class='form-group col-md-6 mb-0'),
            #     Column('width', css_class='form-group col-md-6 mb-0'),
            #     css_class='form-row'
            # ),
            'width',
            'depth',
            'response_time_needed',
            Submit('submit', 'Show')
        )

    class Meta:
        model = Pothole
        fields = '__all__'
        # exclude = ('geometry',)
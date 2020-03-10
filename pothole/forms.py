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
                Column('photo', css_class='form-group col-md-6 mb-0'),
                Column('response_time_needed', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),

            Row(
                Column('depth', css_class='form-group col-md-6 mb-0'),
                Column('width', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            # 'geometry',
            # Button('submit', 'Add Pothole', css_class='btn btn-primary ajax_submit_pothole', )
            Submit('submit', 'Save')
        )

    def save(self, *args, **kwargs):
        print(self.fields['width'])
        # super(PotholeForm, self).save(*args, **kwargs)

    class Meta:
        model = Pothole
        fields = '__all__'
        # exclude = ('geometry',)
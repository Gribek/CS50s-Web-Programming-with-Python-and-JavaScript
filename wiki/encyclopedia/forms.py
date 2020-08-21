from django import forms

from encyclopedia.util import list_entries


class AddEntryForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title in list_entries():
            self.add_error('title', 'Entry with such title already exist!')
        return cleaned_data

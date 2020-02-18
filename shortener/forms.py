from django import forms


class FullURLForm(forms.Form):
    full_url = forms.URLField(    )
    proposed_shortcut = forms.SlugField(
        max_length=200, 
        required=False, 
        help_text='Shortcut can consist of letters, numbers, underscores or hyphens.', 
        error_messages={'invalid':'You can use only letters, numbers, underscores or hyphens.'}
    )
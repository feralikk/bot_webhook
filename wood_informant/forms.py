from django import forms

from .models import Profile

# class LumberForm(forms.ModelForm):
#     class Meta:
#         model = Lumber
#         fields = (
#             'id', 'post_id', 'title', 'city', 'type', 'wood_type', 'wet', 'length', 'width',
#             'thickness', 'price', 'discription', 'post_date',
#             'parse_date', 'post_views', 'post_url'
#         )
#         widgets = {
#             'city': forms.TextInput,
#             'discription': forms.TextInput,
#         }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'external_id',
            'name',
        )
        widgets = {
            'name': forms.TextInput,
        }

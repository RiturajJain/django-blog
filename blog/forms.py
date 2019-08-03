from django import forms
from .models import Comment

class CommentOnPostForm(forms.ModelForm):

    content = forms.CharField(
                                label = '',
                                widget = forms.Textarea(
                                    attrs = {
                                        'placeholder': "Comment here",
                                        'class': "comment-form",
                                        'rows': 3,
                                        }
                                )
                            )

    class Meta:
        model = Comment
        fields = ['content']

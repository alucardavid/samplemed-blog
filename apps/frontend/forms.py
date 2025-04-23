from django import forms
from django.contrib.auth.models import User
from apps.api.models.article import Article

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password_confirm']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nome de usuário'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Primeiro nome'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Último nome'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password_confirm'):
            self.add_error('password_confirm', 'As senhas não coincidem.')
        return cleaned_data
    

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nome de usuário', 'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha', 'class': 'form-control'})
    )

class ArticleCreateForm(forms.ModelForm):
    keywords = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'palavra1, palavra2, palavra3',
            'class': 'form-control'
        }),
        label='Palavras-chave'
    )

    class Meta:
        model = Article
        fields = ['title', 'subtitle', 'content', 'type', 'status', 'keywords']
        widgets = {
            'title': forms.TextInput(),
            'subtitle': forms.TextInput(),
            'content': forms.Textarea(),
            'type': forms.Select(),
            'status': forms.Select(),
        }
        labels = {
            'title': 'Título',
            'subtitle': 'Subtítulo',
            'content': 'Conteúdo',
            'type': 'Tipo',
            'status': 'Status',
        }
    
    def clean_keywords(self):
        """Converte a string de keywords em uma lista de nomes"""
        keywords = self.cleaned_data.get('keywords', '')
        if keywords:
            keyword_list = [k.strip() for k in keywords.split(',') if k.strip()]
            return keyword_list
        return []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
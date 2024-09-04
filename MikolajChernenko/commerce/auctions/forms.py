# auctions/forms.py

from django import forms
from .models import Listing, Bid, Comment, Category

class ListingForm(forms.ModelForm):
    image = forms.ImageField(required=False)  # Usunięto przecinek na końcu
    starting_bid = forms.DecimalField(label='Starting Bid (€)', max_digits=10, decimal_places=2)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label="Category")

    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image', 'category']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

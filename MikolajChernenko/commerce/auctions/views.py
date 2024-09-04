from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages  
from .models import User, Listing, Bid, Comment, Category
from .forms import ListingForm, BidForm, CommentForm
from django.utils import timezone

def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })

@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.current_price = listing.starting_bid
            listing.created_by = request.user
            listing.save()
            messages.success(request, "Listing created successfully.")
            return redirect("index")
    else:
        form = ListingForm()
    return render(request, "auctions/create_listing.html", {
        "form": form
    })

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    bids = listing.bids.all()
    comments = listing.comments.all()
    in_watchlist = request.user.is_authenticated and request.user.watchlist.filter(pk=listing_id).exists()
    bid_form = BidForm()
    comment_form = CommentForm()

    highest_bid = bids.order_by('-amount').first()
    user_won_auction = request.user.is_authenticated and not listing.is_active and highest_bid and highest_bid.user == request.user

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": bids,
        "comments": comments,
        "in_watchlist": in_watchlist,
        "bid_form": bid_form,
        "comment_form": comment_form,
        "user_won_auction": user_won_auction
    })

@login_required
def add_to_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    request.user.watchlist.add(listing)
    messages.success(request, "Added to watchlist.")
    return redirect("listing", listing_id=listing_id)

@login_required
def remove_from_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    request.user.watchlist.remove(listing)
    messages.success(request, "Removed from watchlist.")
    return redirect("listing", listing_id=listing_id)

@login_required
def watchlist(request):
    listings = request.user.watchlist.all()
    watchlist_count = listings.count()
    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        "watchlist_count": watchlist_count
    })

@login_required
def place_bid(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            if bid.amount < listing.starting_bid:
                messages.error(request, "Bid must be at least as high as the starting bid.")
            elif listing.bids.exists() and bid.amount <= listing.current_price:
                messages.error(request, "Bid must be higher than the current highest bid.")
            else:
                bid.listing = listing
                bid.user = request.user
                bid.timestamp = timezone.now()
                bid.save()
                listing.current_price = bid.amount
                listing.save()
                messages.success(request, "Your bid was placed successfully!")
                return redirect("listing", listing_id=listing_id)
        else:
            messages.error(request, "Invalid bid amount.")
    
    
    return redirect("listing", listing_id=listing_id)

@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.user == listing.created_by and listing.is_active:
        listing.is_active = False
        listing.save()
        messages.success(request, "Auction closed successfully.")
    else:
        messages.error(request, "You are not authorized to close this auction.")
    return redirect("listing", listing_id=listing_id)

@login_required
def add_comment(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.listing = listing
            comment.user = request.user
            comment.save()
            messages.success(request, "Comment added successfully.")
    return redirect("listing", listing_id=listing_id)

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category_listings(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = Listing.objects.filter(category=category, is_active=True)
    return render(request, "auctions/category_listings.html", {
        "category": category,
        "listings": listings
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid username and/or password.")
    return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, "Passwords must match.")
            return render(request, "auctions/register.html")
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            messages.success(request, "Registration successful.")
        except IntegrityError:
            messages.error(request, "Username already taken.")
            return render(request, "auctions/register.html")
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/register.html")

def active_listings(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/active_listings.html", {
        "listings": listings
    })

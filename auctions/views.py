from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django import forms
from .models import *
from .forms import AuctionForm
from django.contrib.auth.decorators import login_required



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def index(request):
    Lists = AuctionListing.objects.all()
    print(Lists)
    return render(request,"auctions/index.html",{
        "Lists" : Lists
    })

#function to display detailed view of each of the auction list
@login_required(login_url='login')

def list(request,Auction_id):

#Auction stores the auction retrieved using id
    Auction = AuctionListing.objects.get(id = Auction_id)
 #Comment is class whose object store auction name and owner who commented on that particular auction -- like this we may have many
    comment = Comments.objects.filter(auction=Auction).order_by('created_at')
#Bid is class that stores all the objects that was bidded on a particular auction by a particular user many-many relation 
    bid = Bids.objects.filter(auction=Auction).order_by('bid_time')


#if method is post that is form is submitted of comment then create the comment in its object
    if request.method == "POST":
        comment_text = request.POST.get("content")
        bid_amt = request.POST.get("bid_amount")
       

        if  bid_amt  and request.user.is_authenticated:
            Bids.objects.create(auction=Auction,user=request.user,bid_amount=bid_amt)

        if comment_text and request.user.is_authenticated:
            Comments.objects.create(auction=Auction,user=request.user,content=comment_text)
            return HttpResponseRedirect(reverse('list' ,args =[Auction_id]))


#else when we go to a particular auction page it should go to listing html detailed content
    return render(request,"auctions/listings.html",{
        "Auction" : Auction,
        "Comments":comment,
        "bids":bid

    })

def toggle_watchlist(request,Auction_id):
    Auction = AuctionListing.objects.get(id =Auction_id)
    
    if request.user in Auction.watchlisted_by.all():
        Auction.watchlisted_by.remove(request.user)
    else:
        Auction.watchlisted_by.add(request.user)
    return HttpResponseRedirect(reverse('list' ,args =[Auction_id]))

def user_watchlist(request):
    watchlist = request.user.watchlist.all()
    category_obj = Category.objects.get(name="Household Items")
    Auction = AuctionListing.objects.filter(category=category_obj)
    print(Auction)
    return render(request,"auctions/watchlist.html",{"watchlist":watchlist})
    
def category(request,category):
    category_obj = Category.objects.get(name=category)
    Auctions = AuctionListing.objects.filter(category=category_obj)
    return render(request,"auctions/category.html",{"Auctions":Auctions})

@login_required(login_url='login')
def create_auction(request):
    if request.method == "POST":
        form = AuctionForm(request.POST)
        if form.is_valid:
            auction = form.save(commit=False)
            auction.owner = request.user
            auction.save()
            return redirect('index')
        else:
            form = AuctionForm()


    return render(request,"auctions/create_auction.html",{"form":AuctionForm})

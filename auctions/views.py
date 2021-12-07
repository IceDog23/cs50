from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, connections
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import activate, templatize
from .forms import NewListing, NewBid, NewComment
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Categories, User, Bid, Comment, Watchlist, Listing  

def index(request):
    #find all listings in database 
    #pass it to the template
    items = Listing.objects.all()

    return render(request, "auctions/index.html", {
        "items":items
    })

#function to create a new listing 
@login_required
def create_listing (request): 
    if request.method == "POST":
        form = NewListing(request.POST)

        if form.is_valid(): 
            new_item = form.save(commit=False)
            new_item.owner = request.user 
            new_item.save()

            return HttpResponseRedirect(reverse("auction:listing", args=(new_item.pk,)))

    else: 
        form = NewListing()

        return render (request, 'auctions/create_listing.html', {
            'form': form
        })
    
    return HttpResponseRedirect(reverse("auction:index"))
    

def listing (request, id): 
    #find a listing in a database 
    item = Listing.objects.get(pk = id)    
    #create a form for new bids
    f_bid = NewBid()    
    #check if owner is same user as sign in
    owner = False
    #check if highest bidder is same user as sign in
    h_bidder = False 
    #list all comments for listing 
    comments = Comment.objects.filter(item=id)

    #render newcomment form 
    f_new_comment = NewComment()

    if request.user.is_authenticated:
        name = User.objects.get (username = request.user.username)

        #look for a item owner 
        if item.owner == name:
            owner = True

        #check if log in user is highest bidder on the item 
        if item.h_bidder == name: 
            h_bidder = True    

    if request.method == 'POST':
        
        if 'close_listing' in request.POST and owner: 
            item.active = False
            item.save()

        data ={             
            'item': item,
            'owner': owner,
            'watchlist': None,
            'f_bid': f_bid,
            'h_bidder': h_bidder,
            'f_new_comment': f_new_comment,
            'comments': comments
        }
        
        return render (request, "auctions/listing.html", data)


    #try to find a item in watchlist 
    try: 
        watchlist = Watchlist.objects.get(user = name, item = item)
        data = {
            'item': item,
            'owner': owner,
            'watchlist': watchlist,
            'f_bid': f_bid,
            'h_bidder': h_bidder,
            'f_new_comment': f_new_comment, 
            'comments': comments
        }
    except: 
        data = {
            'item': item,
            'owner': owner,
            'watchlist': None,
            'f_bid': f_bid,
            'h_bidder': h_bidder,
            'f_new_comment': f_new_comment, 
            'comments': comments
        }
    return render (request, "auctions/listing.html", data)

@login_required
def watchlist (request, user): 
    if request.user.is_authenticated: 
        name = User.objects.get(pk = request.user.id)

    if request.method == "POST": 

        if 'd_watchlist' in request.POST: 
            item_id = request.POST['d_watchlist']
            watchlist = Watchlist.objects.filter(item = item_id, user = name) 
            watchlist.delete()
            return HttpResponseRedirect(reverse("auction:watchlist", args=(user,)))    


        else: 
            item_id = request.POST['item']
            item = Listing.objects.get(pk = item_id)
            watched = True
            new_watchlist = Watchlist(user = name, item= item, watched = watched)
            new_watchlist.save()
            return HttpResponseRedirect(reverse("auction:listing", args=(item_id,)))    

    else:
        #load watchlist from database 
        watchlist = Watchlist.objects.filter(user = name)
        return render (request, "auctions/watchlist.html", {
            'watchlist': watchlist
        })

@login_required
def bid (request, id): 
    if request.method == "POST":
        form = NewBid(request.POST)

        print(form.errors)

        if form.is_valid():   
            name = User.objects.get(pk = request.user.id)
            item = Listing.objects.get(pk = id)
            new_bid = form.save(commit=False)
            new_bid.bidder = name
            new_bid.item = item
            new_bid.save()


            print (new_bid.bid)
            print (item.h_bid)

            if new_bid.bid < item.h_bid or (new_bid.bid < item.price and item.h_bid == 0): 
                messages.error(request, "Sorry your bid is too low. Bid higher")
                return HttpResponseRedirect(reverse('auction:listing', args=(id,)))

            else:
                #change a bidder on listing 
                item.h_bid = new_bid.bid 
                item.h_bidder = new_bid.bidder
                item.save()

            return HttpResponseRedirect(reverse('auction:listing', args=(id,)))

        else: 
            #render error
            messages.error(request, "Sorry something is wrong, try again later.")
            return HttpResponseRedirect(reverse('auction:listing', args=(id,)))

@login_required
def new_comment (request, id): 
    if request.method == 'POST': 
        print('in post')
        form = NewComment(request.POST)
        name = User.objects.get(pk = request.user.id)
        item = Listing.objects.get(pk = id)

        if form.is_valid(): 
            new_comment = form.save (commit=False)
            new_comment.user = name
            new_comment.item = item
            new_comment.save()

            return HttpResponseRedirect(reverse('auction:listing', args=(id,)))
    else: 
        print('here')
        messages.error(request, 'Sorry something went wrong. Try again later.')
        return HttpResponseRedirect(reverse('auction:listing', args=(id,)))

def categories (request): 
    #load all categies from the datagase 
    #have acces to items in each category (might need to change models)
    categories = Categories.objects.all()

    data = {
        'categories': categories
    }    

    return render (request, "auctions/categories.html", data)

def category (request, title): 
    category = Categories.objects.get(category = title)
    items = Listing.objects.filter(category = category.id, active = True)

    data = {
        'title': title,
        'items': items
    }

    return render (request, 'auctions/category.html', data)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auction:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auction:index"))


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
        return HttpResponseRedirect(reverse("auction:index"))
    else:
        return render(request, "auctions/register.html")

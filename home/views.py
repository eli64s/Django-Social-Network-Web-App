from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from home.forms import HomeForm
from home.models import Post, Friend 
from django.contrib.auth.decorators import login_required

# The Home App's Views
class HomeView(TemplateView):
    '''
    Homepage class-based view
    '''
    template_name = 'home/home.html'

    
    def get(self, request):
        '''
        Function that gets the user posts on the home page's timeline / newsfeed
        '''
        form = HomeForm()
        posts = Post.objects.all().order_by('-created') # Orders the home page posts by most recently created
        users = User.objects.exclude(id = request.user.id) # Does not show logged in user on 'Add Friends'
        friend, created = Friend.objects.get_or_create(current_user = request.user)
        friends = friend.users.all()

        context = {'form': form, 'posts': posts, 'users': users, 'friends': friends}
        return render(request, self.template_name, context)

    
    def post(self, request):
        '''
        Function to post a message on timeline / newsfeed
        '''
        form = HomeForm(request.POST) # request.post fills form with data received from post request
        if form.is_valid():
            post = form.save(commit = False)
            post.user = request.user 
            post.save()

            text = form.cleaned_data['post']
            form = HomeForm() # Reset to an empty form after submited 
            return redirect('home:home')

        context = {'form': form, 'text': text}
        return render(request, self.template_name, context)


def change_friends(request, operation, pk):
    '''
    Function to add / remove users from your friends list
    '''
    friend = User.objects.get(pk = pk) # Gives us the user
    
    # Add Friend
    if operation == 'add':
        Friend.make_friend(request.user, friend)
    # Remove Friend
    elif operation == 'remove':
         Friend.lose_friend(request.user, friend)

    return redirect('home:home')
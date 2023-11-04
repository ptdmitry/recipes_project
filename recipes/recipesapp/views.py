from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from fuzzywuzzy import process

from .models import Recipe, Category
from .forms import RecipeForm, ProfileForm
from . import utils


def home(request):
    # Retrieve 5 random recipes from the database
    recipes = Recipe.objects.order_by('?')[:5]
    print(recipes)

    # Define any additional data you want to pass to the template
    # For example, you might want to include other information or featured recipes.

    context = {
        'recipies': recipes,
        # Add other context data here if needed
    }

    # Render the home page using the 'home.html' template
    return render(request, 'recipesapp/home.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            login(request, user)
            return redirect('home')
        else:
            # Log validation errors for debugging
            for field, errors in form.errors.items():
                print(f"Validation errors for field {field}: {errors}")
    else:
        form = UserCreationForm()
    return render(request, 'recipesapp/registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the homepage or any other desired page
    return render(request, 'recipesapp/login.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'recipesapp/edit_profile.html', {'form': form})


def recipies(request):
    # Retrieve 5 random recipes to display on the home page
    # random_recipes = Recipe.objects.order_by('?')[:5]
    return render(request, 'recipesapp/home.html')


def get_recipe(request, recipe_id):
    # Retrieve the recipe based on the provided recipe_id or return a 404 page if not found
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    # Define any additional data you want to pass to the template
    # For example, you might want to include related data like comments, ratings, or author information.

    context = {
        'recipe': recipe,
        'steps': utils.make_cooking_steps_article(recipe.cooking_steps),
        # Add other context data here if needed
    }

    # Render the recipe detail page using the 'recipe_detail.html' template
    return render(request, 'recipesapp/recipe_detail.html', context)


@login_required
def add_recipe(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        # If the request is a POST request, it means the form has been submitted
        form = RecipeForm(request.POST, request.FILES)  # Create a form instance with the POST data
        if form.is_valid():
            # If the form is valid, save the recipe
            new_recipe = form.save(commit=False)  # Create a new recipe instance, but don't save it to the database yet
            new_recipe.author = request.user  # Set the author to the currently logged-in user
            new_recipe.save()  # Save the recipe to the database

            # Add categories (if you have a multiple select field for categories)
            categories = request.POST.getlist('categories')
            new_recipe.categories.set(Category.objects.filter(pk__in=categories))

            return redirect('home')  # Redirect to the homepage or a different page after successful submission
    else:
        # If the request is a GET request, display the form
        form = RecipeForm()  # Create a new empty form instance

    return render(request, 'recipesapp/add_recipe.html', {'form': form, 'categories': categories})


def find_best_matching_recipe(request, recipe_name):
    # Get all recipe names from the database
    all_recipe_names = Recipe.objects.values_list('name', flat=True)

    # Find the best match
    best_match = process.extractOne(recipe_name, all_recipe_names)

    if best_match[1] >= 50:
        return best_match[0]

    return None


def get_recipe_by_name(request, recipe_name):
    best_matching_recipe = find_best_matching_recipe(request, recipe_name)

    if best_matching_recipe:
        recipe = Recipe.objects.filter(name=best_matching_recipe).first()
        # Redirect to the detailed recipe page with the best-matching recipe name
        return redirect('recipe', recipe_id=recipe.id)

    # Handle the case where no match is found
    return render(request, 'recipesapp/no_recipe_found.html')


@login_required  # This decorator ensures that only logged-in users can access the view
def edit_recipe(request, recipe_id):
    # Get the recipe by its ID or return a 404 error if it doesn't exist
    recipe = get_object_or_404(Recipe, id=recipe_id)
    categories = Category.objects.all()

    # Check if the logged-in user is the author of the recipe
    if request.user == recipe.author:
        if request.method == 'POST':
            form = RecipeForm(request.POST, instance=recipe)
            if form.is_valid():
                form.save()
                return redirect('recipe_detail', recipe.id)  # Redirect to the recipe detail page
        else:
            form = RecipeForm(instance=recipe)
        return render(request,
                      'recipesapp/edit_recipe.html',
                      {'form': form, 'recipe': recipe, 'categories': categories}
                      )
    else:
        # Handle the case where the logged-in user is not the author of the recipe
        return redirect('home')


def get_recipes(request, user=None):
    if user:
        # Get recipes from the specified user
        user_obj = User.objects.filter(username=user).first()
        if user_obj:
            recipes = Recipe.objects.filter(author=user_obj)
        else:
            recipes = []
    else:
        # Get all recipes
        recipes = Recipe.objects.all()

    context = {
        'recipes': recipes
    }

    return render(request, 'recipesapp/recipe_list.html', context)


def search_recipes(request):
    query = request.GET.get('q', '')  # Get the search query from the URL parameter 'q'
    results = get_recipe_by_name(query)  # Perform fuzzy search

    return render(request, 'recipesapp/search_results.html', {'results': results, 'query': query})

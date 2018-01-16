def get_rating(request):
    rating = request.session['rating'] if 'rating' in request.session else 0
    return {
        'current_rating': rating
    }


def get_name(request):
    if 'gender' in request.session:
        name = 'Melisa' if request.session['gender'] else 'Roberto'
    else:
        name = 'Roberto'
    return {
        'name': name
    }

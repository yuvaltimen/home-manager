from django.shortcuts import render

shopping = [
    {
        "name": "Cottage cheese",
        "author": "Adi",
        "created": "Aug. 12, 2024"
    },
    {
        "name": "Yogurt",
        "author": "Adi",
        "created": "Aug. 12, 2024"
    },
    {
        "name": "Matza",
        "author": "Yuval",
        "created": "Aug. 13, 2024"
    }
]


def home(req):
    ctx = {
        'title': 'Shopping List',
        'shopping_items': shopping
    }
    return render(req, 'shopping_list/home.html', ctx)


def about(req):
    return render(req, 'shopping_list/about.html')





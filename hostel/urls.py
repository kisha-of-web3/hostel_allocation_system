from django.urls import path
from . import views

urlpatterns = [
    # List all hostels
    path('', views.hostels_list, name='hostels_list'),
    path('hostels/', views.hostels_list, name='hostels_list'),

    # Hostel detail page
    path('hostels/<int:hostel_id>/', views.hostel_detail, name='hostel_detail'),

    # Step 1 — Select hostel
    path('apply/select/', views.select_hostel, name='select_hostel'),

    # Step 2 — Application form (must include hostel_id)
    path('apply/<int:hostel_id>/', views.apply_hostel_form, name='apply_hostel_form'),

    # Staff routes
    path('applications/', views.allocations_pending, name='allocations_pending'),
    path('allocate/<int:app_pk>/<int:room_pk>/', views.allocate, name='allocate'),
]

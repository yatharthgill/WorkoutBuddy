from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse
from django.conf import settings
import logging

FASTAPI_BASE_URL = settings.FASTAPI_BASE_URL

# Use module logger; Django logging config controls output in production
logger = logging.getLogger(__name__)


# ===================== DIET PREFERENCE =====================

def diet_preference_view(request):
    allergies_list = ['Nuts', 'Gluten', 'Dairy', 'Soy', 'Eggs', 'Shellfish', 'None']

    token = request.session.get('token')
    if not token:
        return redirect('login')


    try:
        headers = {'Authorization': f'Bearer {token}'}
        resp = requests.get(f'{FASTAPI_BASE_URL}/api/diet/diet-plan/', headers=headers, timeout=5)
        if resp.status_code == 200:
            user_data = resp.json().get('data', {})
            user_id = user_data.get('user_id')
            if user_id:
                request.session['user_id'] = user_id
    except Exception:
        logger.exception("Failed to fetch user_id from FastAPI")



    if request.method == 'POST':
        try:
            diet_type = request.POST.get('diet_type')
            activity_level = request.POST.get('activity_level')
            fitness_goal = request.POST.get('fitness_goal')
            experience_level = request.POST.get('experience_level')
            medical_conditions = request.POST.get('medical_conditions', '')
            preferred_workout_style = request.POST.get('preferred_workout_style')
            preferred_training_days_per_week = request.POST.get('preferred_training_days_per_week')
            

           

            allergies = request.POST.getlist('allergies') or []
            other_allergy = request.POST.get('other_allergy', '').strip()
            if other_allergy:
                allergies.append(other_allergy)

            payload = {
                # "user_id": user_id,
                "diet_type": diet_type,
                "activity_level": activity_level,
                "fitness_goal": fitness_goal,
                "experience_level": experience_level,
                "medical_conditions": [m.strip() for m in medical_conditions.split(',') if m.strip()],
                "allergies": allergies,
                "other_allergy": other_allergy,
                "preferred_workout_style": preferred_workout_style,
                "preferred_training_days_per_week": preferred_training_days_per_week,
            }

            headers = {'Authorization': f'Bearer {token}'}
            response = requests.post(
                f"{FASTAPI_BASE_URL}/api/diet/generate-diet-plan/",
                json=payload,
                headers=headers,
                timeout=10
            )

            logger.debug("FastAPI generate-diet-plan status=%s", response.status_code)
            logger.debug("FastAPI generate-diet-plan response=%s", response.text)

            if response.status_code in [200, 201]:
                return redirect('dietPlan:diet_result')
            else:
                logger.error("FastAPI returned error while generating diet plan: %s", response.text)

        except Exception:
            logger.exception("Form processing failed in diet_preference_view")

    return render(request, 'diet-form.html', {
        'allergies_list': allergies_list
    })


# ===================== DIET RESULT =====================

def diet_result_view(request):
    token = request.session.get('token')
    if not token:
        return redirect('login')

    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f"{FASTAPI_BASE_URL}/api/diet/diet-plan/", headers=headers)
        logger.debug("FastAPI diet-plan status=%s", response.status_code)

        # Redirect if diet plan is not found or API call fails
        if response.status_code == 404:
            logger.info("Diet plan not found for user; redirecting to preference form")
            return redirect('dietPlan:dietPreference')

        if response.status_code != 200:
            logger.error("Unexpected error fetching diet plan: %s", response.text)
            return redirect('dietPlan:dietPreference')

        data = response.json().get("data", {})
        plan = data.get("ai_generated_plan", {})
        logger.debug("Diet plan data retrieved: exists=%s", bool(plan))

    except Exception:
        logger.exception("Exception occurred while fetching diet plan")
        return redirect('dietPlan:dietPreference')

    return render(request, 'diet-result.html', {
        'diet_plan': plan
    })

    
    
# ===================== CHECK RESULT =====================

def check_diet_plan_view(request):
    token = request.session.get("token")
    

    if not token:
        return JsonResponse({"exists": False}, status=401)

    try:
        response = requests.get(
            f"{FASTAPI_BASE_URL}/api/diet/diet-plan/",
            headers={"Authorization": f"Bearer {token}"},
            timeout=3
        )

        if response.status_code == 200:
            data = response.json()
            logger.debug("check_diet_plan_view response data: exists=%s", bool(data.get("ai_generated_plan")))
            exists = bool(data.get("ai_generated_plan"))
            return JsonResponse({"exists": exists})
        else:
            logger.warning("check_diet_plan_view unexpected status: %s", response.status_code)
            return JsonResponse({"exists": False})
    except Exception:
        logger.exception("Error checking diet plan existence")
        return JsonResponse({"exists": False}, status=500)




# ===================== MEAL LOG =====================

def meal_log_view(request):
    token = request.session.get('token')
    if not token:
        return redirect('login')

    meal_types = ['breakfast', 'lunch', 'dinner']

    if request.method == 'POST':
        date = request.POST.get('date')
        meal_data = {'date': date, 'breakfast': [], 'lunch': [], 'dinner': []}

        for meal_type in meal_types:
            items = []
            for key in request.POST:
                if key.startswith(f"{meal_type}["):
                    idx = key[len(meal_type) + 1:].split(']')[0]
                    field = key.split('[')[2].rstrip(']')
                    if idx.isdigit():
                        idx = int(idx)
                        while len(items) <= idx:
                            items.append({})
                        items[idx][field] = request.POST[key]

            for item in items:
                item_data = {
                    "item_name": item.get("item_name"),
                    "quantity": float(item.get("quantity")) if item.get("quantity") else None,
                    "weight_in_grams": float(item.get("weight_in_grams")) if item.get("weight_in_grams") else None
                }
                if item_data["item_name"]:
                    meal_data[meal_type].append(item_data)

        meal_data = {k: v for k, v in meal_data.items() if v or k == "date"}

        try:
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.post(f"{FASTAPI_BASE_URL}/api/progress/meal-log/", json=meal_data, headers=headers)

            logger.debug("Meal log POST status=%s", response.status_code)
            logger.debug("Meal log response=%s", response.text)

            if response.status_code in [200, 201]:
                return render(request, 'meal-log.html', {
                    'meal_types': meal_types,
                    'message': 'Meal log submitted successfully!'
                })
            else:
                logger.error("Failed to log meal: status=%s response=%s", response.status_code, response.text)
                return render(request, 'meal-log.html', {
                    'meal_types': meal_types,
                    'message': 'Failed to log meal.'
                })

        except Exception:
            logger.exception("Meal log submission failed")
            return render(request, 'meal-log.html', {
                'meal_types': meal_types,
                'message': 'Error submitting meal log.'
            })

    # If GET request
    return render(request, 'meal-log.html', {
        'meal_types': meal_types
    })
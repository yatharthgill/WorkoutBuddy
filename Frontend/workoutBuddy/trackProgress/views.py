import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from dateutil.parser import parse as parse_date
import requests


FASTAPI_BASE_URL = settings.FASTAPI_BASE_URL


@csrf_exempt
def workout_log(request):
    token = request.session.get("token")
    if not token:
        return redirect("login")

    headers = {"Authorization": f"Bearer {token}"}
    context = {}

    if request.method == "POST":
        date = request.POST.get("selected_date")
        plan_id = request.POST.get("plan_id")
        status = request.POST.get("status", "completed")
        exercises_data = []

        for key in request.POST:
            if key.startswith("exercise_"):
                _, date_key, exercise_name = key.split("_", 2)
                completed = request.POST.get(key) == "on"
                sets = request.POST.get(f"sets_{exercise_name}", 0)
                reps = request.POST.get(f"reps_{exercise_name}", "")
                duration = request.POST.get(f"duration_{exercise_name}", "")

                exercises_data.append({
                    "name": exercise_name,
                    "sets": int(sets),
                    "reps": reps,
                    "duration_per_set": duration,
                    "completed": completed
                })

        payload = {
            "plan_id": plan_id,
            "date": date,
            "status": status,
            "created_at": timezone.now().isoformat(),
            "exercises": exercises_data
        }

        try:
            response = requests.post(f'{FASTAPI_BASE_URL}/api/workout/complete/', json=payload, headers=headers)
            response_data = response.json()

            if response_data.get("status") == 201:
                context["success_message"] = response_data["message"]
            else:
                context["error_message"] = f"Failed to submit log: {response_data.get('message', 'Unknown error')}"
        except Exception as e:
            context["error_message"] = f"Error while submitting workout log: {e}"

        # Continue to GET the latest workout plan even after POST
        # so that the user stays on the same page
        # instead of redirecting

    try:
        response = requests.get(f'{FASTAPI_BASE_URL}/api/workout/plans/user', headers=headers)
        response_data = response.json()
        workout_plan = response_data.get("data", [None])[0]

        if workout_plan and "_id" in workout_plan:
            workout_plan["id"] = workout_plan.pop("_id")

        context["workout_plan"] = workout_plan
    except Exception as e:
        pass

    return render(request, "workout_log.html", context)


def diet_progress_view(request):
    token = request.session.get("token")
    # user_id = request.session.get("user_id")
  
    if not token:
        messages.error(request, "You must be logged in to view your diet progress.")
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(
            f"{FASTAPI_BASE_URL}/api/progress/diet/chart/progress",
            headers=headers
        )
        res_data = response.json()
        
        if res_data["status"] != 200:
            messages.error(request, res_data.get("message", "Could not fetch progress data."))
            return redirect("dietPlan:meal_log")

        data = res_data["data"]
        return render(request, "chart.html", {
            "period": data["period"],
            "weight": data["weight"],
            "consistency": data["consistency_percentage"],
            "adherence": data["adherence_percentage"],
            "daily_data": data["daily_chart_data"]
        })

    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect("dietPlan:meal_log")





def workout_progress_view(request):
    token = request.session.get("token")
    if not token:
        messages.error(request, "You must be logged in to view workout progress.")
        return redirect("login")

    try:
        response = requests.get(
            f"{FASTAPI_BASE_URL}/api/workout/progress/report",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
      

        if not data.get("success"):
            raise ValueError("API call failed")

        summary = data.get("data", {}).get("summary", {})

        daily_logs = summary.get("dailyLog", [])

        # Safely prepare chart data
        workout_dates = [log.get("date") for log in daily_logs if log.get("date")]
        calorie_per_day = [log.get("calorie_burnout", 0) for log in daily_logs]

        muscle_distribution = summary.get("muscle_distribution", {})
        muscle_labels = list(muscle_distribution.keys())
        muscle_values = list(muscle_distribution.values())

        context = {
            "start_date": summary.get("start_date"),
            "end_date": summary.get("end_date"),
            "completed_days": summary.get("completed_days", 0),
            "total_days": summary.get("total_days", 0),
            "consistency": summary.get("consistency", 0),
            "average_rpe": summary.get("average_rpe", 0),
            "total_sets": summary.get("total_sets", 0),
            "total_reps": summary.get("total_reps", 0),
            "calories_burned": summary.get("sum_of_all_calorie_burnout", 0),
            "weight": summary.get("weight", 0),
            "tips": summary.get("tips", []),
            # Chart data, passed as safe JSON strings
            "workout_dates": json.dumps(workout_dates),
            "calorie_per_day": json.dumps(calorie_per_day),
            "muscle_labels": json.dumps(muscle_labels),
            "muscle_values": json.dumps(muscle_values),
        }

        return render(request, "workout_Chart.html", context)

    except Exception as e:
        print("ERROR:", str(e))
        messages.error(request, f"Failed to fetch workout progress: {str(e)}")
        return render(request, "workout_Chart.html", {"error": str(e)})




def diet_progress_date_range_view(request): 
    token = request.session.get("token")
    if not token:
        messages.error(request, "Please log in to continue.")
        return redirect("login")

    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        print("Sending date range:", start_date, end_date)

        headers = {
            "Authorization": f"Bearer {token}"
        }
        params = {
            "start_date": start_date,
            "end_date": end_date
        }

        try:
            response = requests.get(
                f"{FASTAPI_BASE_URL}/api/progress/Diet/generate",
                headers=headers,
                params=params,
                timeout=10
            )
            res_json = response.json()
            # print("API Response:", res_json)
            # print("Status Code:", response.status_code)

            if response.status_code != 200 or "data" not in res_json or "summary" not in res_json["data"]:
                messages.error(request, "Can't generate the data on these dates.")
                return render(request, "dates.html", {
                    "start_date": start_date,
                    "end_date": end_date
                })

            data = res_json.get("data", {})
            summary = data.get("summary", {})
            report = summary.get("dietProgressReport", {})

            if not data:
                messages.error(request, "No data available between these dates.")
                return render(request, "dates.html", {
                    "start_date": start_date,
                    "end_date": end_date
                })

            # ✅ ADD THIS HERE
            daily_logs = report.get("estimatedCalorieBreakdown", {}).get("dailyLog", [])
            processed_daily_data = [
                {"date": log["date"], "total": log["calories"]["total"]}
                for log in daily_logs
            ]

            return render(request, "chart.html", {
                "start_date": start_date,
                "end_date": end_date,
                "period": report.get("userProfile", {}).get("period"),
                "weight": report.get("userProfile", {}).get("weight"),
                "consistency": report.get("mealLoggingConsistency", {}).get("consistencyPercentage"),
                "adherence": report.get("adherenceAnalysis", {}).get("adherencePercentage"),
                "daily_data": json.dumps(processed_daily_data)  # ✅ Pass JSON here
            })

        except Exception as e:
            messages.error(request, f"Error fetching chart data: {str(e)}")
            return render(request, "dates.html", {
                "start_date": start_date,
                "end_date": end_date
            })

    return render(request, "dates.html")



def workout_progress_date_range_view(request): 
    token = request.session.get("token")
    if not token:
        messages.error(request, "Please log in to continue.")
        return redirect("login")

    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        print("Sending date range for workout:", start_date, end_date)

        headers = {
            "Authorization": f"Bearer {token}"
        }
        params = {
            "start_date": start_date,
            "end_date": end_date
        }

        try:
            response = requests.get(
                f"{FASTAPI_BASE_URL}/api/progress/Workout/generate",  # Make sure this route exists in your FastAPI backend
                headers=headers,
                params=params,
                timeout=10
            )
            res_json = response.json()

            if response.status_code != 200 or not res_json.get("success"):
                messages.error(request, res_json.get("message"))
                return render(request, "workout_dates.html", {
                    "start_date": start_date,
                    "end_date": end_date
                })

            summary = res_json.get("data", {}).get("summary", {})

            daily_logs = summary.get("dailyLog", [])

            workout_dates = [log.get("date") for log in daily_logs if log.get("date")]
            calorie_per_day = [log.get("calorie_burnout", 0) for log in daily_logs]

            muscle_distribution = summary.get("muscle_distribution", {})
            muscle_labels = list(muscle_distribution.keys())
            muscle_values = list(muscle_distribution.values())

            context = {
                "start_date": start_date,
                "end_date": end_date,
                "completed_days": summary.get("completed_days", 0),
                "total_days": summary.get("total_days", 0),
                "consistency": summary.get("consistency", 0),
                "average_rpe": summary.get("average_rpe", 0),
                "total_sets": summary.get("total_sets", 0),
                "total_reps": summary.get("total_reps", 0),
                "calories_burned": summary.get("sum_of_all_calorie_burnout", 0),
                "weight": summary.get("weight", 0),
                "tips": summary.get("tips", []),
                "workout_dates": json.dumps(workout_dates),
                "calorie_per_day": json.dumps(calorie_per_day),
                "muscle_labels": json.dumps(muscle_labels),
                "muscle_values": json.dumps(muscle_values),
            }

            return render(request, "workout_Chart.html", context)

        except Exception as e:
            messages.error(request, f"Error fetching workout chart data: {str(e)}")
            return render(request, "workout_dates.html", {
                "start_date": start_date,
                "end_date": end_date
            })

    return render(request, "workout_dates.html")
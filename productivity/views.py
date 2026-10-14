import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from . import model_service as ms


def _clean(values):
    return {f: float(values.get(f, 0) or 0) for f in ms.FEATURES}


def dashboard(request):
    data = {
        "summary": ms.summary(),
        "employees": ms.employees(),
        "fields": [{"name": n, "label": l, "step": s} for n, l, s in ms.FIELDS],
    }
    return render(request, "productivity/dashboard.html", {"data": data})


def predict_form(request):
    fields = [{"name": n, "label": l, "step": s} for n, l, s in ms.FIELDS]

    if request.method == "POST":
        values = _clean(request.POST)
        result = ms.predict(values)
        inputs = [{"label": l, "value": values[n]} for n, l, _ in ms.FIELDS]
        bars = [{"name": k, "pct": round(v * 100, 1)} for k, v in result["probabilities"].items()]
        return render(request, "productivity/result.html",
                      {"result": result, "inputs": inputs, "bars": bars})

    initial = ms.medians()
    emp_id = request.GET.get("employee_id")
    if emp_id:
        match = [e for e in ms.employees() if str(e.get("Employee_ID")) == emp_id.strip()]
        if match:
            initial = {f: match[0][f] for f in ms.FEATURES}
    for f in fields:
        f["value"] = initial.get(f["name"], 0)
    return render(request, "productivity/employee_form.html", {"fields": fields})


@require_POST
def api_predict(request):
    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse(ms.predict(_clean(payload)))


def api_summary(request):
    return JsonResponse(ms.summary())


def api_employee(request, employee_id):
    for e in ms.employees():
        if str(e.get("Employee_ID")) == employee_id:
            return JsonResponse({"employee": e, "prediction": ms.predict(_clean(e))})
    return JsonResponse({"error": "Employee not found"}, status=404)

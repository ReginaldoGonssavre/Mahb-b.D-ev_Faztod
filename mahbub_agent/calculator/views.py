from django.http import JsonResponse
import numpy as np

def add_vectors(request):
    vector_a = request.GET.getlist('a', type=float)
    vector_b = request.GET.getlist('b', type=float)
    result = np.add(vector_a, vector_b).tolist()
    return JsonResponse({'result': result})
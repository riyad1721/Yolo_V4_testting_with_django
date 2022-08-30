from django.shortcuts import render
from django.http.response import StreamingHttpResponse,JsonResponse
from base.camera import VideoPTZ,ObjectDetect


# Create your views here.
# Create your views here.
def index(request):
    return render(request, 'index.html')
def dashboard(request):
    context = {
                'test' : 'This is my test dashboard'
                }
    return render(request, 'dashboard.html', context)

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
# def genData(camera):
#     while True:
#         data=list(camera.get_data())
#         return data
def video_feed(request):
	return StreamingHttpResponse(gen(VideoPTZ()),
					content_type='multipart/x-mixed-replace; boundary=frame')
def object_feed(request):
	return StreamingHttpResponse(gen(ObjectDetect()),
					content_type='multipart/x-mixed-replace; boundary=frame')
# def detect_result(request):
#     return StreamingHttpResponse(gen(ObjectDetect()),
# 					content_type='multipart/x-mixed-replace; boundary=frame')

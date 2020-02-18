from django.core.mail import send_mail

from backend.celery import app
from video_encoding.tasks import convert_all_videos

from contest.models import Video


@app.task(queue='father')
def convert_videos():
    videos_to_convert = Video.objects.filter(status="En Proceso")
    app_label = videos_to_convert.first()._meta.app_label
    model_name = videos_to_convert.first()._meta.model_name
    for video in videos_to_convert:
        convert_video.delay(app_label, model_name, video.id)
        video.status = "converting"
        video.save()


@app.task(queue='son')
def convert_video(video_id, app_label, model_name):
    convert_all_videos(app_label, model_name, video_id)


@app.task(queue='check')
def convert_video():
    videos_in_converting_process = Video.objects.filter(status="converting")
    for video in videos_in_converting_process:
        if video.format_set.complete().all().exists():
            video.status = "Convertido"
            video.save()
            send_mail('SmartTools - Video Cargado para conscurso',
                      'El video que subiste para el concurso ' + video.contest.name +
                      ' ha sido cargado con exito. Puedes ingresar a verlo en ' + video.contest.url,
                      'c.cordobac@uniandes.edu.co',
                      [video.email],
                      fail_silently=False)

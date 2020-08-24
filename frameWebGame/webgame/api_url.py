from django.urls import path
from webgame import api



urlpatterns = [
    #新场景
    path('new-changjing/',api.newChangjing),
    path('upload-bg/',api.upload_img),
    #场景
    path('get-changjing/',api.getChangjing),
    #流程
    path('add-step/',api.addStep),
    path('get-step/',api.getStep),
    path('save-step-setting/',api.saveStepSetting),
    #角色
    path('set-actor/',api.setActor),
    path('delete-action/',api.deleteAction)
]
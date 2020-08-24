from rest_framework.response import Response
from rest_framework.decorators import api_view
from webgame.models import Changjing,Step,People,People_action
from PIL import Image
from io import BytesIO
from io import BytesIO
import os
import base64

imgUrl = "http://127.0.0.1:9000/upload/"
hostUrl = "http://127.0.0.1:9000/"

@api_view(['GET',"DELETE"])
def getChangjing(request):
  if request.method == "DELETE":
    changjing_id = request.POST['changjing_id']

    changjing = Changjing.objects.get(id=changjing_id)
    changjing.delete()
    return Response('ok')
  all_changjing = Changjing.objects.all()
  all_changjing_data = []

  for changjing in all_changjing:
    changjing_item = {
      "name":changjing.name,
      "bgimg":imgUrl+str(changjing.bgimg),
      "id":changjing.id,
      "label":changjing.name
    }
    all_changjing_data.append(changjing_item)
  return Response(all_changjing_data)



@api_view(['POST'])
def newChangjing(request):
  name = request.POST['name']
  new_changjing = Changjing(name=name)
  new_changjing.save()

  all_changjing = Changjing.objects.all()
  all_changjing_data = []

  for changjing in all_changjing:
    changjing_item = {
      "name":changjing.name,
      "bgimg":imgUrl+str(changjing.bgimg),
      "id":changjing.id,
      "label":changjing.name
    }
    all_changjing_data.append(changjing_item)
  return Response(all_changjing_data)

@api_view(['POST'])
def upload_img(request):
  cj_id = request.POST['cj_id']
  new_bg = request.FILES['file']


  changjing = Changjing.objects.get(id=cj_id)
  changjing.bgimg = new_bg
  changjing.save()

  return Response({"msg":"ok","bgimg":imgUrl+str(changjing.bgimg)})


@api_view(['GET','DELETE'])
def getStep(request):
  if request.method == "DELETE":
    step_id = request.POST['step_id']

    step = Step.objects.get(id=step_id)
    step.delete()
    return Response('ok')
  cj_id = request.GET['id']

  changjing = Changjing.objects.get(id=cj_id)

  all_step = changjing.step_changjing.all()
  all_step_data = []

  for step in all_step:
    step_item = {
      "name":step.name,
      "id":step.id,
      "people1":{
        "nickName":"",
        "name":"",
        "bodyimg":""
      },
      "people2":{
        "nickName":"",
        "name":"",
        "bodyimg":""
      },
      "text":"",
      "playType":"enter"
    }
    if step.people1:
      step_item['people1']["nickName"] = step.people1.belong.nickName
      step_item['people1']["name"] = step.people1.name
      step_item['people1']["bodyimg"] = step.people1.bodyimg
    if step.people2:
      step_item['people2']["nickName"] = step.people2.belong.nickName
      step_item['people2']["name"] = step.people2.name
      step_item['people2']["bodyimg"] = step.people2.bodyimg
    if step.text:
      step_item['text'] = step.text
    all_step_data.append(step_item)

  return Response(all_step_data)


@api_view(['POST'])
def addStep(request):
  print(request.POST)
  changjing_id = request.POST['changjing_id']
  name = request.POST['name']

  changjing = Changjing.objects.get(id=changjing_id)
  new_step =  Step(name=name,belong=changjing)
  new_step.save()
  return Response('ok')

#保存流程设置
@api_view(['POST'])
def saveStepSetting(request):
  step_id = request.POST['step_id']
  step = Step.objects.get(id=step_id)
  left_action = request.POST['left_action']
  leftAction = People_action.objects.filter(id=left_action)
  right_action = request.POST['right_action']
  rightAction = People_action.objects.filter(id=right_action)
  text = request.POST['text']

  if leftAction:
    step.people1 = leftAction[0]
  else:
    step.people1 = None
  if rightAction:
    step.people2 = rightAction[0]
  else:
    step.people2 = None
  step.text = text
  step.save()
  return Response('ok')


#角色
@api_view(['POST','GET','DELETE','PUT'])
def setActor(request):
  if request.method=="PUT":
    actor_id = request.POST['actor_id']
    actor = People.objects.get(id=actor_id)
    action_img = request.POST['action_img']
    action_name = request.POST['action_name']
    # print('本地图片')
    image_data = base64.b64decode(action_img.split(',')[1])
    image_name = actor.nickName +'-'+ action_name + '.png'
    # print(image_name)
    image_url = os.path.join('upload', image_name).replace('\\', '/')
    with open(image_url, 'wb') as f:
        f.write(image_data)

    bodyimg = hostUrl+image_url
    print(bodyimg,action_name)

    new_action = People_action(name=action_name,bodyimg=bodyimg,belong=actor)
    new_action.save()
    return Response('ok')
  if request.method=="DELETE":
    artor_id = request.POST['artor_id']

    artor = People.objects.get(id=artor_id)
    artor.delete()
    return Response('ok')
  if request.method=='POST':
    new_actor = request.POST['new_actor']

    new_people = People(nickName=new_actor)
    new_people.save()
    return Response('ok')
  if request.method=="GET":
    all_actor = People.objects.all()
    all_actor_data = []
    for actor in all_actor:
      actor_item = {
        "nickName":actor.nickName,
        "coverimg":"",
        "id":actor.id,
        "action":[]
      }
      all_action = actor.action_people.all()
      for action in all_action:
        action_item = {
          "id":action.id,
          "name":action.name,
          "bodyimg":action.bodyimg
        }
        actor_item["action"].append(action_item)
      all_actor_data.append(actor_item)
    return Response(all_actor_data)


@api_view(['DELETE'])
def deleteAction(request):
  action_id=request.POST['action_id']
  action = People_action.objects.get(id=action_id)
  action.delete()
  return Response('ok')
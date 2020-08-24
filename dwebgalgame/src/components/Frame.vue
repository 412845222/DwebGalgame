<template>
  <div>
    <div id="frame" :style="'background:url('+Changjing.bgimg+')'">
      <!-- 人物 -->
      <div v-if="StepInfo.people1 || StepInfo.people2" id="people">
        <div v-if="StepInfo.people1.bodyimg" id="people-left" :class="'people '+StepInfo.playType">
          <img :src="StepInfo.people1.bodyimg" alt="" />
        </div>
        <div v-if="StepInfo.people2.bodyimg" id="people-right" :class="'people '+StepInfo.playType">
          <img :src="StepInfo.people2.bodyimg" alt="" />
        </div>
      </div>
      <!-- 对话 -->
      <div v-if="StepInfo.text" id="msg" :class="'dweb msgtext '+StepInfo.playType">
        <!-- 人物名称 -->
        <div id="people-name">
          <div v-if="StepInfo.people1.nickName" >
            <span id="name-left">{{ StepInfo.people1.nickName }} :</span>
          </div>
          <div v-if="StepInfo.people2.nickName">
            <span id="name-right">: {{ StepInfo.people2.nickName }}</span>
          </div>
          <div class="clear"></div>
        </div>
        <!-- 人物对话 -->
        <div  id="msg-content">
          <div class="dweb">
            <p>{{ StepInfo.text }}</p>
          </div>
          
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props:{
    Changjing:Object,
    StepInfo:Object
  },
  watch:{
    
  },
  data() {
    return {
      
    }
  },
};
</script>

<style scoped>
#frame {
  overflow: hidden;
  width: 1200px;
  height: 675px;
  background: url("../assets/testData/test-frameBg.png");
}
#people-left {
  /* border: 1px solid #000; */
  width: 500px;
  height: 675px;
  overflow: hidden;
  position: absolute;
  margin-left: 100px;
}
#people-right {
  /* border: 1px solid #000; */
  width: 500px;
  height: 675px;
  overflow: hidden;
  position: absolute;
  margin-left: 600px;
}
.people img {
  width: 100%;
}
.people {
  transform: translate3d(0px, 0px, 0px);
  transition: opacity 500ms ease-in-out;
  opacity:1;
  filter: alpha(opacity=1);
}
.msgtext {
  transform: translate3d(0px, 0px, 0px);
  transition: opacity 500ms ease-in-out;
  opacity:1;
  filter: alpha(opacity=1);
}
.enter {
  opacity:0;
  filter: alpha(opacity=0);
  transition: opacity 500ms ease-in-out;
}


#msg {
  position: absolute;
  width: 1200px;
  height: 200px;
  margin-top: 475px;
}

#people-name {
  font-size: 30px;
  width: 100%;
  margin-top: 20px;
}
#name-left {
  float: left;
  margin-left: 100px;
}
#name-right {
  float: right;
  margin-right: 100px;
}
#msg-content {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}
#msg-content .dweb{
  box-sizing: border-box;
  width: 90%;
  text-align: center;
  font-size: 20px;
  padding: 10px 50px;
  font-weight: 700;
}
</style>

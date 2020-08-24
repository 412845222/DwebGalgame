<template>
  <div>
    <el-row :gutter="10">
      <el-col :span="6">
        <div class="dweb" style="display:flex">
          <el-input v-model="new_actor" placeholder="新建角色名称"></el-input>
          <el-button @click="saveNewActor()" type="success">保存新建</el-button>
        </div>
      </el-col>

      <el-col :span="10">
        <el-row :gutter="10" id="actor-list">
          <el-col v-for="item in all_actor" :key="item.id" :span="12">
            <div class="dweb">
              {{ item.nickName }}
              <el-divider></el-divider>
              <el-button @click="chooseArctor(item)" type="success"
                >进入管理</el-button
              >
              <el-button @click="deleteArtor(item.id)" type="danger"
                >删除</el-button
              >
            </div>
          </el-col>
        </el-row>
      </el-col>

      <el-col v-if="choosed_actor.id" id="actor-admin" :span="8">
        <div class="dweb">
          <span>角色名: {{ choosed_actor.nickName }}</span>
          <el-divider></el-divider>
          <div class="dweb" style="display:flex">
            <el-input
              v-model="new_actor_action"
              placeholder="新建动作名称"
            ></el-input>
            <el-button @click="saveNewAction()" size="mini" type="success">
              保存新建
            </el-button>
            <el-button @click="clickUploadBtn" size="mini" type="warning">
              上传图片
            </el-button>
          </div>
        </div>
        <div class="body dweb">
          <el-row :gutter="10">
            
            <el-col id="preview-img" :span="16">
              <div class="dweb">
                <img src="" alt="" />
                <el-image v-if="new_actor_action_src.length>0" :src="new_actor_action_src" :fit="'cover'"></el-image>
                <el-image v-else :src="choosed_action.bodyimg" :fit="'cover'"></el-image>
              </div>
            </el-col>
            <el-col :span="8"> 
              <el-row>
                <el-col v-for="item in choosed_actor.action" :key="item.id">
                  <div class="dweb" style="text-align:center">
                      {{ item.name }}
                      <el-divider></el-divider>
                      <el-button @click="chooseAction(item)" type="success" size="mini">查看</el-button>
                      <el-button @click="deleteAction(item.id)" type="danger" size="mini">删除</el-button>
                  </div>
                </el-col>
              </el-row>
            </el-col>
            <input
              id="upload-action"
              @change="imgInput($event)"
              type="file"
              style="display:none"
            />
          </el-row>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from "axios";
import Qs from "qs";
export default {
  data() {
    return {
      new_actor: "",
      all_actor: [],
      //管理
      choosed_actor: {},
      choosed_action:{},
      new_actor_action: "",
      new_actor_action_src: "",
      new_actor_action_file:{},

    };
  },
  mounted() {
    this.getAllActor();
  },
  methods: {
    chooseAction(action){
      this.choosed_action = action
    },
    deleteAction(id){
      axios({
        method:'delete',
        headers:{
          "Content-Type":"application/x-www-form-urlencoded"
        },
        url: "http://127.0.0.1:9000/api/delete-action/",
        data: Qs.stringify({
          action_id:id
        })
      }).then((res)=>{
        if (res.data=='ok') {
          this.getAllActor();
        }
      })
    },
    //保存新动作
    saveNewAction(){
      axios({
        method: "put",
        url: "http://127.0.0.1:9000/api/set-actor/",
        data: Qs.stringify({
          actor_id: this.choosed_actor.id,
          action_img:this.new_actor_action_src,
          action_name:this.new_actor_action
        }),
      }).then((res)=>{
        console.log(res)
        if (res.data=='ok') {
          this.getAllActor();
          this.new_actor_action_src = ""
          this.new_actor_action = ""
        }
      })
    },
    //选择角色
    chooseArctor(actor) {
      this.choosed_actor = actor;
      this.new_actor_action_src = ""
      this.choosed_action = {}
    },
    saveNewActor() {
      axios({
        method: "post",
        url: "http://127.0.0.1:9000/api/set-actor/",
        data: Qs.stringify({
          new_actor: this.new_actor,
        }),
      }).then((res) => {
        console.log(res);
        if (res.data == "ok") {
          this.getAllActor();
        }
      });
    },
    //获取全部角色
    getAllActor() {
      axios({
        method: "get",
        url: "http://127.0.0.1:9000/api/set-actor/",
      }).then((res) => {
        this.all_actor = res.data;
        this.all_actor.forEach((obj)=>{
          if (obj.id == this.choosed_actor.id) {
            this.choosed_actor = obj
          }
        })
      });
    },
    deleteArtor(id) {
      axios({
        method: "delete",
        url: "http://127.0.0.1:9000/api/set-actor/",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        data: Qs.stringify({
          artor_id: id,
        }),
      }).then((res) => {
        if (res.data == "ok") {
          this.getAllActor();
        }
      });
    },
    //图片选择
    imgInput(e) {
      let files = e.target.files;
      console.log(files);
      let img = files[0];
      this.new_actor_action_file = img
      let imgData = new FileReader();
      imgData.readAsDataURL(img);
      var self = this
      imgData.onload = function() {
        self.new_actor_action_src = imgData.result;
      };
    },
    clickUploadBtn() {
      let inputDom = document.getElementById("upload-action");
      inputDom.click();
    },
  },
};
</script>

<style scoped>
.dweb {
  color: #fff;
}
#actor-list .dweb {
  color: #fff;
  min-height: 60px;
  margin-top: 5px;
  text-align: center;
  padding: 10px 10px;
}
#actor-admin .dweb {
  padding: 10px 10px;
}
#actor-admin .dweb span {
  font-size: 30px;
  font-weight: 700;
}
#preview-img {
  /* width: 300px; */
}
</style>

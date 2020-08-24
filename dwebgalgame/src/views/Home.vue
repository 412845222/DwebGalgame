<template>
  <div id="create">
    <el-row :gutter="5">
      <el-col :span="2">
        <div class="dweb">
          <el-input
            v-model="new_changjing"
            placeholder="请新场景名称"
          ></el-input>
          <el-button size="mini" @click="addNewChangjing" type="success"
            >添加场景</el-button
          >
        </div>
        <div class="body dweb" style="padding:0 0 10px 0">
          <el-row>
            <el-col v-for="item in changjing_tree" :key="item.id" :span="24" style="margin-top:10px;text-align:center">
              <el-button-group v-if="item.id == choosed_changjing.id">
                <el-button
                  icon="el-icon-video-camera"
                  type="warning"
                  size="mini"
                >{{ item.name }}</el-button>
                <el-button
                  @click="deleteChangjing(item.id)"
                  type="danger"
                  icon="el-icon-delete"
                  size="mini"
                  circle
                ></el-button>
              </el-button-group>
              <el-button-group v-else>
                <el-button
                  @click="chooseChangjing(item)"
                  icon="el-icon-video-camera"
                  type="primary"
                  size="mini"
                >{{ item.name }}</el-button>
                <el-button
                  @click="deleteChangjing(item.id)"
                  type="danger"
                  icon="el-icon-delete"
                  size="mini"
                  circle
                ></el-button>
              </el-button-group>
            </el-col>
          </el-row>
        </div>
      </el-col>
      <el-col :span="6">
        
        <SetpSetting
          @getAllStep="getAllStep"
          @changeFrameStep="changeFrameStep"
          @reloadSetpData="reloadSetpData"
          @closeSetChangjing="closeSetChangjing"
          @reloadAllStep="getAllStep"
          :Changjing="choosed_changjing"
          :StepList="step_list"
          :Actors="all_actor"
        ></SetpSetting>
      </el-col>
      <el-col :span="16">
        <div id="center-dom" class="dweb" style="padding:20px 0">
          <div id="wutai">
            <Frame
              :Changjing="choosed_changjing"
              :StepInfo="choosed_step"
            ></Frame>
          </div>
        </div>
      </el-col>
    </el-row>

    <div v-if="setBox_view" id="set-changjing" class="dweb">
      <div class="dweb" style="padding:20px 20px">
        <h2>{{ choosed_changjing.name }} 背景设置</h2>
        <el-divider></el-divider>
        <el-upload
          :action="'http://127.0.0.1:9000/api/upload-bg/'"
          list-type="picture-card"
          :data="{ cj_id: this.choosed_changjing.id }"
          :on-success="uploadChangjingBg"
        >
          <i class="el-icon-plus"></i>
        </el-upload>
        <el-dialog :visible.sync="dialogVisible">
          <img width="100%" :src="dialogImageUrl" alt="" />
        </el-dialog>

        <el-button
          @click="closeSetChangjing"
          type="warning"
          style="margin-top:20px"
          >关闭</el-button
        >
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Qs from "qs";
import Frame from "../components/Frame.vue";
import SetpSetting from "../components/SetpSetting.vue";
export default {
  data() {
    return {
      changjing_tree: [],
      //场景管理
      maxId: 0,
      new_changjing: "",
      setBox_view: false,
      choosed_changjing: {},

      dialogImageUrl: "",
      dialogVisible: false,

      //场景 流程
      step_list: [],
      choosed_step: {},

      //角色管理
      all_actor: [],
    };
  },
  components: {
    Frame,
    SetpSetting,
  },
  watch: {
    people(value) {
      console.log(value);
    },
  },
  mounted() {
    this.getAllChangjing();
    this.getAllActor();
  },
  methods: {
    //获取全部角色
    getAllActor() {
      axios({
        method: "get",
        url: "http://127.0.0.1:9000/api/set-actor/",
      }).then((res) => {
        // console.log(res.data);
        this.all_actor = res.data;
      });
    },
    //获取场景流程
    getAllStep(id) {
      axios({
        url: "http://127.0.0.1:9000/api/get-step/",
        method: "get",
        params: {
          id,
        },
      }).then((res) => {
        // console.log(res.data);
        this.step_list = res.data;
        this.step_list.forEach((obj)=>{
          if (obj.id == this.choosed_step.id) {
            this.changeFrameStep(obj)
          }
        })
      });
    },
    reloadSetpData(){
      this.getAllChangjing();
      this.getAllActor();
      this.getAllStep(this.choosed_changjing.id)
    },
    //场景流程 切换 画面
    changeFrameStep(step) {
      // console.log(step);
      this.choosed_step = step;
    },
    //设置场景
    uploadChangjingBg(res) {
      console.log(res);
      if (res.msg == "ok") {
        this.choosed_changjing.bgimg = res.bgimg;
        this.getAllChangjing();
      }
    },
    chooseChangjing(node) {
      // console.log(node)
      this.choosed_changjing = node;
      this.setBox_view = true;
      this.getAllStep(node.id);
      this.choosed_step = {}
    },
    closeSetChangjing() {
      this.setBox_view = false;
    },
    //新场景
    addNewChangjing() {
      let checkTree = this.loopCheckData(this.changjing_tree);
      if (checkTree == false) {
        this.new_changjing = "";
        return;
      }

      if (this.new_changjing.length > 0) {
        //存储新场景
        axios({
          method: "post",
          url: "http://127.0.0.1:9000/api/new-changjing/",
          data: Qs.stringify({
            name: this.new_changjing,
          }),
        }).then((res) => {
          this.changjing_tree = res.data;
        });
      }
    },

    //递归查询新id
    loopCheckData(tree) {
      let checkTree = true;
      //检查新栏目数据
      tree.forEach((obj) => {
        if (obj.id > this.maxId) {
          this.maxId = obj.id;
        }
        if (obj.label == this.new_changjing) {
          alert("命名重复");
          checkTree = false;
          return;
        }
        if (obj.children) {
          if (obj.children.length > 0) {
            this.loopCheckData(obj.children);
          }
        }
      });

      return checkTree;
    },
    //获取保存场景
    getAllChangjing() {
      axios({
        method: "get",
        url: "http://127.0.0.1:9000/api/get-changjing/",
      }).then((res) => {
        this.changjing_tree = res.data;
      });
    },

    //测试表情切换
    changeLeftFace() {
      if (this.people.left.face == "sad") {
        this.people.left.face = "enter";
        let self = this;
        this.faceenter = setInterval(function() {
          self.people.left.face = "bkl";
          self.people.left.img = "/people/yukie/yukie_bkl.png";
          clearInterval(self.faceenter);
        }, 500);
      }
      if (this.people.left.face == "bkl") {
        this.people.left.face = "enter";
        let self = this;
        this.faceenter = setInterval(function() {
          self.people.left.face = "sad";
          self.people.left.img = "/people/yukie/yukie_sad.png";
          clearInterval(self.faceenter);
        }, 500);
      }
    },
    deleteChangjing(id){
      axios({
        method:'delete',
        headers:{
          "Content-Type":"application/x-www-form-urlencoded"
        },
        url: "http://127.0.0.1:9000/api/get-changjing/",
        data: Qs.stringify({
          changjing_id:id
        })
      }).then((res)=>{
        if (res.data=="ok") {
          this.getAllChangjing()
          this.choosed_changjing = {}
          this.choosed_step = {}
        }
      })
    }
  },
};
</script>

<style>
#create .dweb {
  /* min-height: 800px; */
  color: #fff;
}
#center-dom {
  display: flex;
  justify-content: center;
  align-items: center;
}
#wutai {
  width: 1200px;
  height: 675px;
  background: #00000060;
}
#set-changjing {
  position: absolute;
  left: 40%;
  top: 10%;
  padding: 20px 20px;
}
#set-changjing .dweb {
  width: 100%;
  height: 100%;
}
</style>

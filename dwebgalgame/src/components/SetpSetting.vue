<template>
  <div>
    <div class="dweb">
      <el-button @click="startPlayFrame" type="success" circle>
        <i class="iconfont icon-bofang"></i>
      </el-button>
      <el-button @click="nextPlayFrame" type="warning" circle>
        <i class="iconfont icon-kuaijin"></i>
      </el-button>
      <el-button @click="stopPlayFrame" type="danger" circle>
        <i class="iconfont icon-iconstop"></i>
      </el-button>
    </div>
    <div v-if="Changjing.id" class="body dweb" style="padding:5px 10px">
      <el-button @click="new_step_view = true" type="primary">
        新建流程
      </el-button>
    </div>
    <div class="body dweb" style="padding:10px 0">
      <el-row :gutter="10">
        <el-col
          v-for="(item, index) in StepList"
          :key="index"
          class="step-item"
          :span="24"
        >
          <el-button-group>
            <el-button
              @click="chooseStepSetting(item)"
              type="info"
              icon="el-icon-s-tools"
              size="mini"
              circle
            ></el-button>
            <el-button
              @click="chooseStepChangeFrame(item, 'preview')"
              type="success"
              size="mini"
              icon="el-icon-thumb"
              >{{ item.name }}</el-button
            >
            <el-button
              v-if="item.people1.name"
              type="primary"
              size="mini"
              icon="el-icon-user"
              >人物-左</el-button
            >
            <el-button
              v-if="item.people2.name"
              type="primary"
              size="mini"
              icon="el-icon-user"
              >人物-右</el-button
            >
            <el-button
              v-if="item.text"
              type="primary"
              icon="el-icon-document"
              size="mini"
            >
              对话
            </el-button>
            <el-button
              type="danger"
              @click="deleteStep(item.id)"
              icon="el-icon-delete"
              circle
              size="mini"
            >
            </el-button>
          </el-button-group>
        </el-col>
      </el-row>
    </div>
    <!-- 新流程 -->
    <div v-if="new_step_view" id="new-step" class="dweb">
      <div class="dweb" style="padding:20px 20px">
        <el-input
          v-model="new_step_name"
          placeholder="新流程名称"
          style="margin-bottom:10px"
        ></el-input>
        <el-button @click="saveNewStep" type="success">保存</el-button>
        <el-button @click="new_step_view = false" type="warning"
          >取消</el-button
        >
      </div>
    </div>

    <!-- 配置流程 -->
    <div
      v-if="setting_step_view"
      id="setting-step"
      class="dweb"
      style="width:300px;padding:20px 20px"
    >
      <div class="dweb" style="padding:20px 20px">
        <h3>{{ Changjing.name }}场景 -- {{ choosed_step.name }}</h3>
        <el-divider></el-divider>
        <el-form :model="choosed_step" class="demo-form-inline">
          <el-form-item label="人物-左">
            <el-select
              v-model="choosed_step.left.actor"
              placeholder="选择人物形象"
            >
              <el-option label="无" value="'none'"></el-option>
              <el-option
                v-for="item in Actors"
                :key="item.id"
                :label="item.nickName"
                :value="item.id"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="人物-左 -- 表情">
            <div v-for="item in Actors" :key="item.id" style="float:left">
              <div v-if="choosed_step.left.actor == item.id">
                <div v-for="action in item.action" :key="action.id">
                  <el-button
                    v-if="action.id == choosed_step.left.action"
                    type="warning"
                    size="mini"
                    >{{ action.name }}</el-button
                  >
                  <el-button
                    v-else
                    @click="choosed_step.left.action = action.id"
                    type="success"
                    size="mini"
                    >{{ action.name }}</el-button
                  >
                </div>
              </div>
            </div>
          </el-form-item>
          <el-form-item label="人物-右">
            <el-select
              v-model="choosed_step.right.actor"
              placeholder="选择人物形象"
            >
              <el-option label="无" value="'none'"></el-option>
              <el-option
                v-for="item in Actors"
                :key="item.id"
                :label="item.nickName"
                :value="item.id"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="人物-右 -- 表情">
            <div v-for="item in Actors" :key="item.id" style="float:left">
              <div v-if="choosed_step.right.actor == item.id">
                <div v-for="action in item.action" :key="action.id">
                  <el-button
                    v-if="action.id == choosed_step.right.action"
                    type="warning"
                    size="mini"
                    >{{ action.name }}</el-button
                  >
                  <el-button
                    v-else
                    @click="choosed_step.right.action = action.id"
                    type="success"
                    size="mini"
                    >{{ action.name }}</el-button
                  >
                </div>
              </div>
            </div>
          </el-form-item>
          <el-form-item label="文本信息">
            <el-input
              type="textarea"
              placeholder="请输入内容"
              v-model="choosed_step.text"
              maxlength="60"
            >
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button @click="saveStepSetting()" type="success"
              >保存</el-button
            >
            <el-button @click="closeSettingStepBox()" type="warning"
              >取消</el-button
            >
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Qs from "qs";
import swal from "sweetalert";
export default {
  props: {
    StepList: Array,
    Changjing: Object,
    Actors: Array,
  },
  data() {
    return {
      //新流程
      new_step_name: "",
      new_step_view: false,
      //设置流程
      choosed_step: {},
      setting_step_view: false,

      //播放流程
      now_step: 0,
      step_list: [],
    };
  },
  mounted() {
    console.log(this.StepList);
  },
  methods: {
    //选择流程
    chooseStepChangeFrame(step, showType) {
      // console.log(step)
      if (showType == "preview") {
        console.log("预览step");
        step.playType = "";
      }
      this.$emit("changeFrameStep", step);
    },
    //设置流程
    chooseStepSetting(step) {
      // console.log('123')
      this.setting_step_view = true;
      this.choosed_step = {
        id: step.id,
        name: step.name,
        left: {
          actor: 0,
          action: 0,
        },
        right: {
          actor: 0,
          action: 0,
        },
        text: "",
      };
      console.log(step);
    },
    saveStepSetting() {
      console.log(this.choosed_step);
      axios({
        url: "http://127.0.0.1:9000/api/save-step-setting/",
        method: "post",
        data: Qs.stringify({
          step_id: this.choosed_step.id,
          left_action: this.choosed_step.left.action,
          right_action: this.choosed_step.right.action,
          text: this.choosed_step.text,
        }),
      }).then((res) => {
        console.log(res.data);

        this.$emit("reloadSetpData");
        this.closeSettingStepBox();
      });
    },
    closeSettingStepBox() {
      this.choosed_step = {};
      this.setting_step_view = false;
    },
    //保存新流程
    saveNewStep() {
      axios({
        url: "http://127.0.0.1:9000/api/add-step/",
        method: "post",
        data: Qs.stringify({
          changjing_id: this.Changjing.id,
          name: this.new_step_name,
        }),
      }).then((res) => {
        console.log(res);
        if (res.data == "ok") {
          this.$emit("getAllStep", this.Changjing.id);
          this.new_step_view = false;
          this.new_step_name = "";
        }
      });
    },
    deleteStep(id) {
      axios({
        url: "http://127.0.0.1:9000/api/get-step/",
        method: "delete",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        data: Qs.stringify({
          step_id: id,
        }),
      }).then((res) => {
        console.log(res.data);
        if (res.data == "ok") {
          this.$emit("getAllStep", this.Changjing.id);
        }
      });
    },
    async reloadAllStep(id) {
      let data = false;
      await axios({
        url: "http://127.0.0.1:9000/api/get-step/",
        method: "get",
        params: {
          id,
        },
      }).then((res) => {
        // console.log(res.data);
        this.step_list = res.data;
        data = true;
      });
      return data;
    },
    startPlayFrame() {
      console.log("开始播放");
      //全部重新获取流程
      this.reloadAllStep(this.Changjing.id).then((res) => {
        if (res) {
          console.log(this.step_list);
          this.$emit("closeSetChangjing");
          //进入场景 第一step
          this.chooseStepChangeFrame(this.step_list[0], "play");
          var self = this;
          let startFrame = setInterval(function() {
            self.step_list[0].playType = "";
            clearInterval(startFrame);
          }, 1000);
        }
      });
    },
    //下一步
    nextPlayFrame() {
      console.log("切换下一流程");
      //清空上一个step 数据
      this.step_list[this.now_step].playType = "enter";
      this.now_step += 1;
      if (this.now_step >= this.step_list.length) {
        swal({
          title: "没有了",
          text: "是否转回第一个流程？",
          icon: "warning",
          buttons: true,
        }).then((willRealod) => {
          if (willRealod) {
            this.now_step = 0;
            //等待界面重置
            let waitReload = setInterval(() => {
              //更新当前播放位置
              this.$emit("closeSetChangjing");
              //进入场景 下一个step
              console.log(this.step_list[this.now_step]);
              this.chooseStepChangeFrame(this.step_list[this.now_step], "play");
              // console.log(this.step_list[0]);
              var self = this;
              let nextFrame = setInterval(function() {
                self.step_list[self.now_step].playType = "";
                clearInterval(nextFrame);
              }, 500);
              clearInterval(waitReload);
            }, 500); 
          } else {
            this.step_list = [];
            this.now_step = 0;
            this.chooseStepChangeFrame({}, "play");
            return;
          }
        });
      } else {
        //等待界面重置
        let waitReload = setInterval(() => {
          //更新当前播放位置
          this.$emit("closeSetChangjing");
          //进入场景 下一个step
          console.log(this.step_list[this.now_step]);
          this.chooseStepChangeFrame(this.step_list[this.now_step], "play");
          // console.log(this.step_list[0]);
          var self = this;
          let nextFrame = setInterval(function() {
            self.step_list[self.now_step].playType = "";
            clearInterval(nextFrame);
          }, 500);
          clearInterval(waitReload);
        }, 500);
      }
    },
    //停止播放模式
    stopPlayFrame() {
      this.step_list = [];
      this.now_step = 0;
      this.chooseStepChangeFrame({}, "play");
    },
    //定时测试
    testTimeLoop() {
      console.log("开始播放");
      this.$emit("closeSetChangjing");
      console.log(this.StepList);

      let allStep = this.StepList;
      //开始循环播放
      let step_index = 0;
      var self = this;
      let framePlayer = setInterval(function() {
        if (step_index < allStep.length) {
          self.chooseStepChangeFrame(allStep[step_index]);
          step_index += 1;
        } else {
          step_index = 0;
          clearInterval(framePlayer);
        }
      }, 1000);
    },
  },
};
</script>

<style scoped>
.step-item {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}
#new-step {
  position: absolute;
  left: 30%;
  top: 20%;
  z-index: 1001;
  padding: 20px 20px;
}
#new-step .dweb {
  width: 100%;
  height: 100%;
  background: #00000090;
}
#setting-step {
  position: absolute;
  left: 30%;
  top: 20%;
  z-index: 1001;
}
#setting-step .dweb {
  width: 100%;
  height: 100%;
  background: #00000090;
}
</style>

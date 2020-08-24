<template>
  <div id="app">
    <div id="top-menu" class="dweb">
      <el-container>
        <el-header>
          <el-menu
            :default-active="'/'"
            class="el-menu-demo"
            :background-color="'#00000000'"
            mode="horizontal"
            router
          >
            <el-menu-item index="/">开始</el-menu-item>
            <el-menu-item index="/actor-store">角色仓库</el-menu-item>
          </el-menu>
        </el-header>
      </el-container>
    </div>
    <div id="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {};
</script>
<style></style>

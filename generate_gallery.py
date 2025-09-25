name: 生成并部署PDF画廊

# 触发条件：当推送到main分支且pdfs或photos目录有变化时
on:
  push:
    branches: [ main ]
    paths:
      - 'pdfs/**'           # 监听pdfs目录变化
      - 'photos/**'         # 监听photos目录变化
      - 'generate_gallery.py'  # 监听生成脚本变化
      - '.github/workflows/generate-gallery.yml'  # 监听工作流文件变化

# 权限设置：解决403权限问题
permissions:
  contents: write        # 允许读写仓库内容
  pages: write           # 允许操作GitHub Pages
  id-token: write        # 允许生成ID令牌

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest  # 使用最新的Ubuntu系统
    
    steps:
      # 步骤1：检出仓库代码
      - name: 检出代码
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # 获取完整历史记录

      # 步骤2：设置Python环境
      - name: 设置Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'  # 指定Python版本
          cache: 'pip'            # 缓存pip依赖，加速构建

      # 步骤3：安装依赖库
      - name: 安装依赖
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      # 步骤4：运行脚本生成画廊
      - name: 生成PDF画廊
        run: python generate_gallery.py

      # 步骤5：部署到GitHub Pages
      - name: 部署到GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}  # 使用内置令牌授权
          publish_dir: ./gallery                     # 部署gallery目录下的内容
          publish_branch: gh-pages                   # 部署到gh-pages分支
          force_orphan: true                         # 强制创建独立分支，减少历史体积
          commit_message: "自动部署: 更新PDF画廊 (${{ github.sha }})"  # 自定义提交信息
          
      # 步骤6：显示部署成功信息
      - name: 部署成功提示
        if: success()
        run: echo "PDF画廊已成功部署到GitHub Pages！"
    
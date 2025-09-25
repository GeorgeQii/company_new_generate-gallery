import os
import glob
from PIL import Image
import shutil

# 配置
PDF_DIR = "pdfs"
PHOTO_DIR = "photos"
GALLERY_DIR = "gallery"
THUMBNAIL_DIR = os.path.join(GALLERY_DIR, "thumbnails")
PDF_DEST_DIR = os.path.join(GALLERY_DIR, "pdfs")

def create_directories():
    """创建必要的目录"""
    os.makedirs(GALLERY_DIR, exist_ok=True)
    os.makedirs(THUMBNAIL_DIR, exist_ok=True)
    os.makedirs(PDF_DEST_DIR, exist_ok=True)

def process_photos():
    """处理照片，生成缩略图"""
    photo_files = glob.glob(os.path.join(PHOTO_DIR, "*.[JjPpGg]*"))  # 匹配常见图片格式
    photo_data = []
    
    for photo_path in photo_files:
        # 获取文件名（不含扩展名）
        photo_name = os.path.splitext(os.path.basename(photo_path))[0]
        
        # 查找对应的PDF文件（假设PDF文件名与照片名相同）
        pdf_path = os.path.join(PDF_DIR, f"{photo_name}.pdf")
        if not os.path.exists(pdf_path):
            print(f"警告: 未找到 {photo_name} 对应的PDF文件")
            continue
        
        # 生成缩略图
        thumbnail_path = os.path.join(THUMBNAIL_DIR, f"{photo_name}.jpg")
        try:
            with Image.open(photo_path) as img:
                # 保持比例缩放，最大宽度/高度为300
                img.thumbnail((300, 300))
                img.convert('RGB').save(thumbnail_path, "JPEG")
        except Exception as e:
            print(f"处理图片 {photo_path} 时出错: {e}")
            continue
        
        # 复制PDF到目标目录
        dest_pdf_path = os.path.join(PDF_DEST_DIR, f"{photo_name}.pdf")
        shutil.copy2(pdf_path, dest_pdf_path)
        
        # 收集数据用于生成HTML
        photo_data.append({
            "name": photo_name,
            "thumbnail": os.path.relpath(thumbnail_path, GALLERY_DIR),
            "pdf": os.path.relpath(dest_pdf_path, GALLERY_DIR)
        })
    
    return photo_data

def generate_html(photo_data):
    """生成与北京愉佚科技风格一致的HTML页面"""
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta name="baidu-site-verification" content="codeva-GoGsXK3SLW">
    <title>北京愉佚科技 - PDF文件画廊</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
    <meta name="description" content="北京愉佚科技PDF文件展示，点击图片查看详细PDF内容">
    <meta name="keywords" content="北京愉佚科技, PDF查看, 技术文档, 资料下载">
    <!-- 引入Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- 引入Font Awesome -->
    <link href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css" rel="stylesheet">
    <link href="image/logo.png" rel="icon" type="image/png">
    <script>
        // Tailwind配置
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        primary: '#165DFF',
                        secondary: '#36BFFA',
                        dark: '#1D2939',
                        light: '#F9FAFB',
                        accent: '#0284C7'
                    },
                    fontFamily: {
                        sans: ['Inter', 'system-ui', 'sans-serif'],
                    },
                }
            }
        }
    </script>
    <style type="text/tailwindcss">
        @layer utilities {
            .content-auto {
                content-visibility: auto;
            }
            .text-shadow {
                text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .hover-lift {
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .hover-lift:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            }
            .gradient-overlay {
                background: linear-gradient(180deg, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.7) 100%);
            }
        }
    </style>
</head>
<body class="bg-light text-dark antialiased">
    <!-- 顶部通知栏 -->
    <div class="bg-primary text-white text-center py-2 text-sm z-50 relative">
        <p>专业技术服务 · 创新解决方案 · 高效实施支持</p>
    </div>

    <!-- Wrapper -->
    <div id="wrapper" class="min-h-screen flex flex-col">

        <!-- Header -->
        <header id="header" class="sticky top-0 z-40 bg-white/95 backdrop-blur-sm shadow-sm transition-all duration-300">
            <div class="container mx-auto px-4 py-3 flex items-center justify-between">
                <a href="index.html" class="flex items-center space-x-2">
                    <img src="image/logo.png" alt="北京愉佚科技logo" class="h-10 w-auto rounded">
                    <div>
                        <strong class="text-xl font-bold text-primary">北京愉佚科技发展有限公司</strong>
                        <span class="block text-sm text-gray-600">技术服务与创新</span>
                    </div>
                </a>
                
                <!-- 桌面导航 -->
                <nav class="hidden md:flex items-center space-x-8">
                    <a href="index.html" class="font-medium text-gray-700 hover:text-primary transition-colors">首页</a>
                    <a href="about.html" class="font-medium text-gray-700 hover:text-primary transition-colors">公司简介</a>
                    <a href="services.html" class="font-medium text-gray-700 hover:text-primary transition-colors">服务项目</a>
                    <a href="https://space.bilibili.com/3546822953928942?spm_id_from=333.33.0.0" target="_blank" class="font-medium text-gray-700 hover:text-primary transition-colors">新闻动态</a>
                    <a href="careers.html" class="font-medium text-gray-700 hover:text-primary transition-colors">招聘信息</a>
                    <a href="contact.html" class="font-medium text-gray-700 hover:text-primary transition-colors">联系方式</a>
                    <a href="pdf-gallery.html" class="font-medium text-primary hover:text-accent transition-colors">PDF画廊</a>
                    <a href="index_en.html" class="ml-4 px-3 py-1 text-sm border border-primary text-primary rounded hover:bg-primary hover:text-white transition-colors">EN</a>
                </nav>
                
                <!-- 移动端菜单按钮 -->
                <div class="flex items-center md:hidden">
                    <a href="index_en.html" class="mr-4 px-3 py-1 text-sm border border-primary text-primary rounded hover:bg-primary hover:text-white transition-colors">EN</a>
                    <button id="menu-toggle" class="text-gray-700 focus:outline-none">
                        <i class="fa fa-bars text-xl"></i>
                    </button>
                </div>
            </div>
            
            <!-- 移动端菜单 -->
            <div id="mobile-menu" class="md:hidden hidden bg-white border-t z-50 absolute w-full left-0">
                <div class="container mx-auto px-4 py-2 flex flex-col space-y-3">
                    <a href="index.html" class="py-2 font-medium text-gray-700 hover:text-primary transition-colors">首页</a>
                    <a href="about.html" class="py-2 font-medium text-gray-700 hover:text-primary transition-colors">公司简介</a>
                    <a href="services.html" class="py-2 font-medium text-gray-700 hover:text-primary transition-colors">服务项目</a>
                    <a href="https://space.bilibili.com/3546822953928942?spm_id_from=333.33.0.0" target="_blank" class="py-2 font-medium text-gray-700 hover:text-primary transition-colors">新闻动态</a>
                    <a href="careers.html" class="py-2 font-medium text-gray-700 hover:text-primary transition-colors">招聘信息</a>
                    <a href="contact.html" class="py-2 font-medium text-gray-700 hover:text-primary transition-colors">联系方式</a>
                    <a href="pdf-gallery.html" class="py-2 font-medium text-primary hover:text-accent transition-colors">PDF画廊</a>
                </div>
            </div>
        </header>

        <!-- Banner -->
        <section id="banner" class="relative h-[60vh] min-h-[400px] flex items-center justify-center overflow-hidden z-10">
            <div class="absolute inset-0 z-0">
                <img src="https://picsum.photos/id/180/1920/1080" alt="PDF文档展示背景" class="w-full h-full object-cover">
                <div class="absolute inset-0 bg-dark/50"></div>
            </div>
            <div class="container mx-auto px-4 z-20 text-center relative">
                <h1 class="text-[clamp(2rem,5vw,3.5rem)] font-bold text-white mb-6 leading-tight text-shadow animate-fade-in">
                    PDF文件画廊
                </h1>
                <p class="text-[clamp(1rem,2vw,1.25rem)] text-gray-100 mb-8 max-w-3xl mx-auto">
                    展示北京愉佚科技各类技术文档与资料，点击图片即可在线查看完整PDF内容
                </p>
                <div class="flex flex-col sm:flex-row justify-center gap-4">
                    <a href="#pdf-gallery" class="px-8 py-3 bg-primary text-white rounded-lg font-medium hover:bg-primary/90 transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-1 relative z-30">
                        查看PDF列表
                    </a>
                    <a href="contact.html" class="px-8 py-3 bg-white/10 backdrop-blur-sm text-white border border-white/30 rounded-lg font-medium hover:bg-white/20 transition-all relative z-30">
                        咨询技术支持
                    </a>
                </div>
            </div>
            <div class="absolute bottom-8 left-0 right-0 flex justify-center animate-bounce z-20">
                <a href="#pdf-gallery" class="text-white/80 hover:text-white">
                    <i class="fa fa-angle-down text-3xl"></i>
                </a>
            </div>
        </section>

        <!-- Main -->
        <div id="main" class="flex-grow relative z-20 bg-light">

            <!-- PDF画廊展示区 -->
            <section id="pdf-gallery" class="py-16 bg-gray-50 relative z-20">
                <div class="container mx-auto px-4">
                    <div class="text-center mb-16 relative z-30">
                        <h2 class="text-[clamp(1.5rem,3vw,2.5rem)] font-bold text-dark mb-4">文档列表</h2>
                        <p class="text-gray-600 max-w-2xl mx-auto">点击下方图片查看对应PDF文档，支持在线浏览与下载</p>
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">'''
    
    # 循环插入PDF与照片卡片
    for item in photo_data:
        html += f'''
                        <article class="tile bg-white rounded-xl overflow-hidden shadow-md hover-lift relative z-30 cursor-pointer" onclick="openPdf('{item["pdf"]}')">
                            <span class="image h-48 overflow-hidden">
                                <img src="{item["thumbnail"]}" alt="{item["name"]}封面" class="w-full h-full object-cover transition-transform duration-500 hover:scale-110">
                            </span>
                            <header class="major p-6">
                                <h3 class="link text-xl font-bold text-dark hover:text-primary transition-colors">{item["name"]}</h3>
                                <p class="text-gray-600 flex items-center mt-2">
                                    <i class="fa fa-file-pdf-o text-red-500 mr-2"></i>
                                    点击查看PDF
                                </p>
                            </header>
                        </article>'''
    
    # 关闭网格布局，继续补充页面剩余部分
    html += '''
                    </div>
                </div>
            </section>

            <!-- 联系区域 -->
            <section id="two" class="py-20 bg-gradient-to-r from-primary to-accent text-white relative z-20">
                <div class="container mx-auto px-4 text-center relative z-30">
                    <header class="major mb-10">
                        <h2 class="text-[clamp(1.5rem,3vw,2.5rem)] font-bold">联系我们</h2>
                    </header>
                    <p class="text-white/90 text-lg max-w-2xl mx-auto mb-8">
                        沟通零距离，服务无止境。北京愉佚科技，您身边的技术专家，随时恭候您的垂询。
                    </p>
                    <ul class="actions justify-center">
                        <li><a href="contact.html" class="px-8 py-3 bg-white text-primary rounded-lg font-medium hover:bg-gray-100 transition-all shadow-lg relative z-40">
                            查看联系方式
                        </a></li>
                    </ul>
                </div>
            </section>

        </div>

        <!-- Footer -->
        <footer id="footer" class="bg-dark text-white pt-16 pb-8 relative z-20">
            <div class="container mx-auto px-4">
                <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
                    <div>
                        <h3 class="text-xl font-bold mb-4">北京愉佚科技</h3>
                        <p class="text-gray-400 mb-4">
                            致力于科技推广和应用服务业，提供全面的技术支持和服务。
                        </p>
                        <div class="flex space-x-4">
                            <a href="#" class="text-gray-400 hover:text-white transition-colors">
                                <i class="fa fa-weixin text-xl"></i>
                            </a>
                            <a href="#" class="text-gray-400 hover:text-white transition-colors">
                                <i class="fa fa-weibo text-xl"></i>
                            </a>
                            <a href="#" class="text-gray-400 hover:text-white transition-colors">
                                <i class="fa fa-linkedin text-xl"></i>
                            </a>
                        </div>
                    </div>
                    
                    <div>
                        <h3 class="text-lg font-bold mb-4">快速链接</h3>
                        <ul class="space-y-2">
                            <li><a href="index.html" class="text-gray-400 hover:text-white transition-colors">首页</a></li>
                            <li><a href="about.html" class="text-gray-400 hover:text-white transition-colors">公司简介</a></li>
                            <li><a href="services.html" class="text-gray-400 hover:text-white transition-colors">服务项目</a></li>
                            <li><a href="careers.html" class="text-gray-400 hover:text-white transition-colors">招聘信息</a></li>
                            <li><a href="contact.html" class="text-gray-400 hover:text-white transition-colors">联系方式</a></li>
                            <li><a href="pdf-gallery.html" class="text-gray-400 hover:text-white transition-colors">PDF画廊</a></li>
                        </ul>
                    </div>
                    
                    <div>
                        <h3 class="text-lg font-bold mb-4">联系我们</h3>
                        <ul class="space-y-2">
                            <li class="flex items-start">
                                <i class="fa fa-map-marker mt-1 mr-3 text-gray-400"></i>
                                <span class="text-gray-400">北京市朝阳区科技园区88号</span>
                            </li>
                            <li class="flex items-center">
                                <i class="fa fa-phone mr-3 text-gray-400"></i>
                                <span class="text-gray-400">010-82721226</span>
                            </li>
                            <li class="flex items-center">
                                <i class="fa fa-envelope mr-3 text-gray-400"></i>
                                <span class="text-gray-400">contact@pleasantteches.com</span>
                            </li>
                        </ul>
                    </div>
                    
                    <div>
                        <h3 class="text-lg font-bold mb-4">订阅资讯</h3>
                        <p class="text-gray-400 mb-4">订阅我们的新闻资讯，了解最新动态</p>
                        <form class="flex relative z-30">
                            <input type="email" placeholder="您的邮箱地址" class="px-4 py-2 rounded-l-lg w-full focus:outline-none text-dark shadow-sm">
                            <button type="submit" class="bg-primary hover:bg-primary/90 px-4 py-2 rounded-r-lg transition-colors shadow-sm">
                                <i class="fa fa-paper-plane"></i>
                            </button>
                        </form>
                    </div>
                </div>
                
                <div class="border-t border-gray-800 pt-8 text-center text-gray-500 text-sm">
                    <ul class="copyright">
                        <li>© 北京愉佚科技发展有限公司 2025</li>
                        <li class="mt-1">© PleasantTech Ventures Co., Ltd. 2025</li>
                    </ul>
                </div>
            </div>
        </footer>

    </div>

    <!-- PDF查看器模态框 -->
    <div id="pdfModal" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 hidden">
        <div class="bg-white rounded-lg w-full max-w-4xl max-h-[90vh] flex flex-col">
            <div class="p-4 border-b flex justify-between items-center">
                <h2 id="pdfTitle" class="text-xl font-bold">PDF查看器</h2>
                <button onclick="closePdf()" class="text-gray-500 hover:text-gray-700">
                    <i class="fa fa-times text-xl"></i>
                </button>
            </div>
            <div class="flex-1 overflow-auto p-4">
                <embed id="pdfEmbed" src="" type="application/pdf" width="100%" height="600px">
            </div>
        </div>
    </div>

    <!-- Scripts -->
    <script>
        // 移动端菜单切换
        document.getElementById('menu-toggle').addEventListener('click', function() {
            const mobileMenu = document.getElementById('mobile-menu');
            mobileMenu.classList.toggle('hidden');
        });

        // 滚动时改变导航栏样式
        window.addEventListener('scroll', function() {
            const header = document.getElementById('header');
            if (window.scrollY > 50) {
                header.classList.add('py-2', 'shadow');
                header.classList.remove('py-3');
            } else {
                header.classList.add('py-3');
                header.classList.remove('py-2', 'shadow');
            }
        });

        // 平滑滚动
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const targetId = this.getAttribute('href');
                if (targetId === '#') return;
                
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 80,
                        behavior: 'smooth'
                    });
                    
                    // 关闭移动菜单（如果打开）
                    document.getElementById('mobile-menu').classList.add('hidden');
                }
            });
        });

        // 添加淡入动画
        document.addEventListener('DOMContentLoaded', function() {
            const fadeElements = document.querySelectorAll('.animate-fade-in');
            fadeElements.forEach(el => {
                el.style.opacity = '0';
                el.style.transform = 'translateY(20px)';
                el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                
                setTimeout(() => {
                    el.style.opacity = '1';
                    el.style.transform = 'translateY(0)';
                }, 300);
            });
        });

        // PDF查看器功能
        function openPdf(pdfPath) {
            const modal = document.getElementById('pdfModal');
            const embed = document.getElementById('pdfEmbed');
            const title = document.getElementById('pdfTitle');
            
            // 提取文件名作为标题
            const fileName = pdfPath.split('/').pop().replace('.pdf', '');
            
            embed.src = pdfPath;
            title.textContent = fileName;
            modal.classList.remove('hidden');
            document.body.style.overflow = 'hidden'; // 防止背景滚动
        }
        
        // 关闭PDF查看器
        function closePdf() {
            const modal = document.getElementById('pdfModal');
            modal.classList.add('hidden');
            document.body.style.overflow = ''; // 恢复滚动
        }
        
        // 点击模态框外部关闭
        document.getElementById('pdfModal').addEventListener('click', function(e) {
            if (e.target === this) {
                closePdf();
            }
        });
        
        // 按ESC键关闭
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && !document.getElementById('pdfModal').classList.contains('hidden')) {
                closePdf();
            }
        });
    </script>
</body>
</html>'''
    
    # 保存HTML文件
    with open(os.path.join(GALLERY_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

def main():
    print("开始生成PDF和照片画廊...")
    create_directories()
    photo_data = process_photos()
    if not photo_data:
        print("警告: 没有找到可处理的照片和PDF文件")
    generate_html(photo_data)
    print(f"画廊生成完成，共处理 {len(photo_data)} 个项目")

if __name__ == "__main__":
    main()
    
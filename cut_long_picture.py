import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
from typing import List, Tuple

class ImageSlicerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🖼️ 长图切割工具")

        # 获取屏幕尺寸
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # 设置初始窗口大小为屏幕的80%
        initial_width = int(screen_width * 0.8)
        initial_height = int(screen_height * 0.8)

        # 计算居中位置
        x = (screen_width - initial_width) // 2
        y = (screen_height - initial_height) // 2

        self.root.geometry(f"{initial_width}x{initial_height}+{x}+{y}")
        self.root.minsize(800, 600)  # 设置最小窗口大小

        # 初始化变量
        self.original_image = None
        self.display_image = None
        self.photo = None
        self.cut_lines = []  # 存储切割线的y坐标
        self.scale_factor = 1.0  # 显示缩放比例
        self.canvas_width = 800
        self.canvas_height = 600

        # 配置样式
        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        """配置UI样式"""
        style = ttk.Style()

        # 设置主题
        style.theme_use('clam')

        # 配置按钮样式
        style.configure('Action.TButton',
                       padding=(10, 5),
                       font=('Arial', 10, 'bold'))

        # 配置标签样式
        style.configure('Info.TLabel',
                       font=('Arial', 9),
                       foreground='#666666')

        # 配置框架样式
        style.configure('Card.TFrame',
                       relief='solid',
                       borderwidth=1)

    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 控制面板
        control_frame = ttk.Frame(main_frame, style='Card.TFrame')
        control_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))

        # 按钮区域
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side=tk.LEFT, padx=10, pady=10)

        ttk.Button(button_frame, text="📁 选择图片", command=self.load_image, style='Action.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="🗑️ 清除切割线", command=self.clear_lines, style='Action.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="✂️ 切割并保存", command=self.slice_and_save, style='Action.TButton').pack(side=tk.LEFT, padx=(0, 10))

        # 信息标签
        info_frame = ttk.Frame(control_frame)
        info_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.info_label = ttk.Label(info_frame, text="请选择一张图片开始", style='Info.TLabel')
        self.info_label.pack()

        # 图片显示区域
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        # 创建画布和滚动条
        self.canvas = tk.Canvas(canvas_frame, bg='white', width=self.canvas_width, height=self.canvas_height)

        # 垂直滚动条
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=v_scrollbar.set)

        # 水平滚动条
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.configure(xscrollcommand=h_scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 绑定鼠标事件
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)

        # 绑定滚轮事件
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Button-4>", self.on_mousewheel)  # Linux
        self.canvas.bind("<Button-5>", self.on_mousewheel)  # Linux

        # 让画布能够获得焦点以接收键盘事件
        self.canvas.focus_set()

        # 切割线列表显示
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

        ttk.Label(list_frame, text="切割线位置:").pack(anchor=tk.W)

        # 列表框显示切割线
        self.lines_listbox = tk.Listbox(list_frame, width=15, height=10)
        self.lines_listbox.pack(fill=tk.Y, expand=True, pady=(5, 0))

        # 删除选中切割线按钮
        ttk.Button(list_frame, text="删除选中", command=self.delete_selected_line).pack(pady=(5, 0))

    def load_image(self):
        """加载图片"""
        file_path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[
                ("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
                ("所有文件", "*.*")
            ]
        )

        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.image_path = file_path

                # 根据图片宽度调整窗口大小
                self.adjust_window_to_image_width()

                self.display_image_on_canvas()
                self.clear_lines()
                self.info_label.config(text=f"已加载: {os.path.basename(file_path)} ({self.original_image.width}x{self.original_image.height})")
            except Exception as e:
                messagebox.showerror("错误", f"无法加载图片: {str(e)}")

    def adjust_window_to_image_width(self):
        """根据图片宽度调整窗口大小，高度固定"""
        if not self.original_image:
            return

        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # 获取图片尺寸
        img_width, img_height = self.original_image.size

        # 为UI控件预留空间
        ui_padding_width = 20 + 250 + 50  # 左右边距 + 切割线列表 + 额外空间
        ui_padding_height = 80 + 40  # 控制面板 + 上下边距

        # 计算窗口宽度：完全贴合图片宽度
        window_width = min(img_width + ui_padding_width, int(screen_width * 0.95))

        # 固定窗口高度为屏幕高度的80%
        window_height = int(screen_height * 0.8)

        # 确保窗口不小于最小尺寸
        window_width = max(window_width, 1000)
        window_height = max(window_height, 700)

        # 计算居中位置
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # 调整窗口大小和位置
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 更新画布尺寸变量
        self.canvas_width = window_width - ui_padding_width
        self.canvas_height = window_height - ui_padding_height

    def display_image_on_canvas(self):
        """在画布上显示图片"""
        if not self.original_image:
            return

        # 计算缩放比例以适应画布
        img_width, img_height = self.original_image.size

        # 计算缩放比例，保持宽度适应画布
        self.scale_factor = min(self.canvas_width / img_width, 1.0)

        # 缩放图片用于显示
        display_width = int(img_width * self.scale_factor)
        display_height = int(img_height * self.scale_factor)

        self.display_image = self.original_image.resize((display_width, display_height), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.display_image)

        # 清除画布并显示图片
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # 设置滚动区域
        self.canvas.configure(scrollregion=(0, 0, display_width, display_height))

    def on_canvas_click(self, event):
        """处理画布点击事件"""
        if not self.original_image:
            return

        # 获取画布坐标
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)

        # 检查点击是否在图片范围内
        if (0 <= canvas_x <= self.display_image.width and
            0 <= canvas_y <= self.display_image.height):

            # 转换为原图坐标
            original_y = int(canvas_y / self.scale_factor)

            # 添加切割线（避免重复）
            if original_y not in self.cut_lines:
                self.cut_lines.append(original_y)
                self.cut_lines.sort()
                self.update_cut_lines_display()
                self.draw_cut_lines()

    def on_mouse_move(self, event):
        """鼠标移动事件，显示预览线"""
        if not self.original_image:
            return

        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)

        # 清除之前的预览线
        self.canvas.delete("preview_line")

        # 检查鼠标是否在图片范围内
        if (0 <= canvas_x <= self.display_image.width and
            0 <= canvas_y <= self.display_image.height):

            # 绘制预览线
            self.canvas.create_line(
                0, canvas_y, self.display_image.width, canvas_y,
                fill="blue", width=1, dash=(5, 5), tags="preview_line"
            )

    def on_mousewheel(self, event):
        """处理鼠标滚轮事件"""
        if not self.original_image:
            return

        # 获取滚动方向
        if event.delta:
            # Windows/macOS
            delta = -1 * (event.delta / 120)
        else:
            # Linux
            if event.num == 4:
                delta = -1
            elif event.num == 5:
                delta = 1
            else:
                return

        # 垂直滚动
        self.canvas.yview_scroll(int(delta), "units")

    def draw_cut_lines(self):
        """绘制所有切割线"""
        # 清除现有切割线
        self.canvas.delete("cut_line")

        for original_y in self.cut_lines:
            # 转换为显示坐标
            display_y = original_y * self.scale_factor

            # 绘制切割线
            self.canvas.create_line(
                0, display_y, self.display_image.width, display_y,
                fill="red", width=2, tags="cut_line"
            )

            # 添加标签显示y坐标
            self.canvas.create_text(
                10, display_y - 10, text=f"y={original_y}",
                fill="red", anchor=tk.W, tags="cut_line"
            )

    def update_cut_lines_display(self):
        """更新切割线列表显示"""
        self.lines_listbox.delete(0, tk.END)
        for i, y in enumerate(self.cut_lines):
            self.lines_listbox.insert(tk.END, f"线{i+1}: y={y}")

    def delete_selected_line(self):
        """删除选中的切割线"""
        selection = self.lines_listbox.curselection()
        if selection:
            index = selection[0]
            del self.cut_lines[index]
            self.update_cut_lines_display()
            self.draw_cut_lines()

    def clear_lines(self):
        """清除所有切割线"""
        self.cut_lines.clear()
        self.update_cut_lines_display()
        if hasattr(self, 'canvas'):
            self.canvas.delete("cut_line")

    def slice_and_save(self):
        """切割图片并保存"""
        if not self.original_image or not self.cut_lines:
            messagebox.showwarning("警告", "请先加载图片并设置切割线")
            return

        # 选择保存目录
        save_dir = filedialog.askdirectory(title="选择保存目录")
        if not save_dir:
            return

        try:
            # 获取原始文件名（不含扩展名）
            base_name = os.path.splitext(os.path.basename(self.image_path))[0]

            # 添加图片顶部和底部作为切割点
            cut_points = [0] + self.cut_lines + [self.original_image.height]
            cut_points = sorted(list(set(cut_points)))  # 去重并排序

            # 调试信息
            print(f"原图尺寸: {self.original_image.width}x{self.original_image.height}")
            print(f"切割点: {cut_points}")

            # 切割图片
            sliced_count = 0
            slice_info = []

            for i in range(len(cut_points) - 1):
                top = cut_points[i]
                bottom = cut_points[i + 1]

                # 跳过高度为0的切片
                if bottom - top <= 0:
                    continue

                # 切割图片 - 使用PIL的crop方法 (left, top, right, bottom)
                crop_box = (0, top, self.original_image.width, bottom)
                slice_img = self.original_image.crop(crop_box)

                # 调试信息
                print(f"切片 {sliced_count + 1}: 裁剪区域 {crop_box}, 结果尺寸: {slice_img.width}x{slice_img.height}")

                # 保存切片
                slice_filename = f"{base_name}_slice_{sliced_count + 1:02d}.png"
                slice_path = os.path.join(save_dir, slice_filename)
                slice_img.save(slice_path, "PNG")

                slice_info.append(f"切片{sliced_count + 1}: y={top}-{bottom}, 高度={bottom-top}px")
                sliced_count += 1

            # 显示详细信息
            info_text = f"图片切割完成！\n共生成 {sliced_count} 个切片\n保存位置: {save_dir}\n\n切片详情:\n" + "\n".join(slice_info)
            messagebox.showinfo("成功", info_text)

        except Exception as e:
            import traceback
            error_msg = f"切割图片时出错: {str(e)}\n\n详细错误:\n{traceback.format_exc()}"
            messagebox.showerror("错误", error_msg)
            print(error_msg)

def main():
    root = tk.Tk()
    app = ImageSlicerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

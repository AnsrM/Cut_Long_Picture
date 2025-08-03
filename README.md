# Long Image Slicer Tool

A graphical user interface tool for slicing long images into multiple parts by clicking to set cutting lines with the mouse.

## Features

- 🖼️ Support for multiple image formats (JPG, PNG, BMP, GIF, TIFF, etc.)
- 🖱️ Mouse click to set cutting line positions
- 👀 Real-time cutting line preview (blue dashed preview, red solid cutting lines)
- 📝 Cutting line list management (view, delete)
- 💾 Automatic saving of sliced images
- 🔄 Support for image scaling and scrolling view
- 📐 **Window width fits image**: Horizontal display width perfectly fits image width, vertical height is fixed
- 🖱️ **Mouse wheel support**: Vertical scrolling for long images, Shift+wheel for horizontal scrolling
- 🎨 **Beautiful UI design**: Modern interface, icon buttons, card-style layout

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Run the program:
   ```bash
   python cut_long_picture.py
   ```

2. Click the "📁 Select Image" button to choose a long image to slice

3. Click on the image to set cutting line positions:
   - Mouse movement shows blue dashed line preview
   - Clicking adds red cutting lines
   - Cutting line positions are displayed in the right panel
   - Use mouse wheel to scroll vertically through long images
   - Hold Shift+wheel for horizontal scrolling

4. Manage cutting lines:
   - Select cutting lines in the right panel and click "❌ Delete Selected" to remove
   - Click "🗑️ Clear Cutting Lines" to remove all cutting lines

5. Click "✂️ Slice and Save" button:
   - Choose save directory
   - The program will automatically slice the image according to cutting lines and save

## Output Files

Sliced images will be named in the following format:
- `original_filename_slice_01.png`
- `original_filename_slice_02.png`
- ...

## Interface Description

- **Control Panel**: Contains buttons for selecting images, clearing cutting lines, slicing and saving
- **Image Display Area**: Shows the image, supports scrolling view, clickable to set cutting lines
- **Cutting Lines List**: Displays all cutting line positions, supports selection and deletion

## Notes

- Cutting lines are automatically sorted by y-coordinate
- Duplicate cutting line positions are automatically deduplicated
- Saved images are in PNG format to ensure quality
- Supports scrolling view for extra-long images
- Window width automatically adjusts according to image width (fits image width), height is fixed at 80% of screen height
- Mouse wheel operations: Normal wheel for vertical scrolling, Shift+wheel for horizontal scrolling
- Interface uses modern design, supports high DPI displays


# 长图切割工具

一个带有图形用户界面的长图切割工具，可以通过鼠标点击设置切割线，将长图切割成多个部分。

## 功能特点

- 🖼️ 支持多种图片格式（JPG, PNG, BMP, GIF, TIFF等）
- 🖱️ 鼠标点击设置切割线位置
- 👀 实时预览切割线效果（蓝色虚线预览，红色实线切割线）
- 📝 切割线列表管理（查看、删除）
- 💾 自动保存切割后的图片
- 🔄 支持图片缩放显示和滚动查看
- 📐 **窗口宽度贴合图片**：横向展示宽度完全贴合图片宽度，纵向固定高度
- 🖱️ **滚轮支持**：垂直滚动查看长图，Shift+滚轮水平滚动
- 🎨 **美观的UI设计**：现代化界面，图标按钮，卡片式布局

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

1. 运行程序：
   ```bash
   python cut_long_picture.py
   ```

2. 点击"选择图片"按钮，选择要切割的长图

3. 在图片上用鼠标点击设置切割线位置：
   - 鼠标移动时会显示蓝色虚线预览
   - 点击后会添加红色切割线
   - 切割线位置会显示在右侧列表中
   - 使用滚轮垂直滚动查看长图
   - 按住Shift+滚轮进行水平滚动

4. 管理切割线：
   - 在右侧列表中选择切割线，点击"删除选中"可删除
   - 点击"清除切割线"可删除所有切割线

5. 点击"切割并保存"按钮：
   - 选择保存目录
   - 程序会自动将图片按切割线分割并保存

## 输出文件

切割后的图片会以以下格式命名：
- `原文件名_slice_01.png`
- `原文件名_slice_02.png`
- ...

## 界面说明

- **控制面板**：包含选择图片、清除切割线、切割并保存等按钮
- **图片显示区域**：显示图片，支持滚动查看，可点击设置切割线
- **切割线列表**：显示所有切割线的位置，支持选择删除

## 注意事项

- 切割线会自动按y坐标排序
- 重复位置的切割线会被自动去重
- 保存的图片格式为PNG，保证质量
- 支持超长图片的滚动查看
- 窗口宽度会根据图片宽度自动调整（贴合图片宽度），高度固定为屏幕的80%
- 滚轮操作：普通滚轮垂直滚动，Shift+滚轮水平滚动
- 界面采用现代化设计，支持高DPI显示

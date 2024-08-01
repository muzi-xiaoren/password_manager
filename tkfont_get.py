import os
import glob

# 获取 Windows 字体目录下的字体
def get_all_fonts():
    # Windows 字体目录
    font_dir ="C:/Windows/Fonts"

    # 支持的字体扩展名
    font_extensions = ["*.ttf", "*.ttc", "*.otf", "*.fon"]

    all_fonts = []
    for extension in font_extensions:
        all_fonts.extend(glob.glob(os.path.join(font_dir, extension)))

    return all_fonts

# 获取所有字体路径
fonts = get_all_fonts()

# 打印所有字体路径
for font in fonts:
    print(font)

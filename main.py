from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont

YELLOW = "#FFE4B5"
FONT = ('Arial', 16, 'bold')


class WatermarkingApp:
    def __init__(self, app):
        app.title('Image Watermarking App')
        app.config(padx=50, pady=50, bg=YELLOW)
        self.image_path = None

        self.upload_label = Label(app, text='📷 Current Image:', bg=YELLOW, fg="#333333", font=FONT)
        self.upload_label.grid(row=0, column=0, pady=20, padx=20)

        self.path_label = Label(app, text="None", bg=YELLOW, fg="#333333", font=FONT)
        self.path_label.grid(row=0, column=1, pady=20, padx=20)

        self.upload_button = Button(app, text='Upload Image', bg=YELLOW, fg='#333333',
                                    font=FONT, command=self.select_image,highlightbackground=YELLOW)
        self.upload_button.grid(row=1, column=0, pady=20, padx=20, columnspan=2)

        self.text_label = Label(app, text='💬 Watermark Text:', bg=YELLOW, fg="#333333", font=FONT)
        self.text_label.grid(row=2, column=0, pady=20, padx=20)

        self.text_entry = Entry(app, width=30, bg=YELLOW, fg='#333333', font=FONT,
                                highlightbackground=YELLOW)
        self.text_entry.grid(row=2, column=1, pady=20, padx=20)
        self.text_entry.insert(END, string='Kaemon Ng')

        # 顏色選擇
        self.color_label = Label(app, text='🎨 Text Color:', bg=YELLOW, fg="#333333", font=FONT)
        self.color_label.grid(row=3, column=0, pady=20, padx=20)

        self.color_var = StringVar(value="White")
        self.color_frame = Frame(app, bg=YELLOW)
        self.color_frame.grid(row=3, column=1, pady=20, padx=20, sticky='w')

        Radiobutton(self.color_frame, text="⚪ White", variable=self.color_var, value="White",
                    bg=YELLOW, fg='#333333', font=('Arial', 14), selectcolor=YELLOW,
                    activebackground=YELLOW, activeforeground='#333333',
                    cursor='hand2').pack(side=LEFT, padx=10)
        Radiobutton(self.color_frame, text="⚫ Black", variable=self.color_var, value="Black",
                    bg=YELLOW, fg='#333333', font=('Arial', 14), selectcolor=YELLOW,
                    activebackground=YELLOW, activeforeground='#333333',
                    cursor='hand2').pack(side=LEFT, padx=10)

        # 位置選擇 - 用 OptionMenu 替代 Combobox
        self.position_label = Label(app, text='📍 Position:', bg=YELLOW, fg="#333333", font=FONT)
        self.position_label.grid(row=4, column=0, pady=20, padx=20)

        self.position_var = StringVar(value="Bottom Right")
        position_options = ["Top Left", "Top Right", "Bottom Left", "Bottom Right"]

        self.position_menu = OptionMenu(app, self.position_var, *position_options)
        self.position_menu.config(
            bg='white',
            fg='#333333',
            font=('Arial', 14),
            activebackground='#E0E0E0',
            activeforeground='#333333',
            highlightthickness=0,
            relief='solid',
            bd=2,
            width=25,
            cursor='hand2'
        )
        # 配置下拉選單樣式
        self.position_menu['menu'].config(
            bg='white',
            fg='#333333',
            font=('Arial', 14),
            activebackground='#4CAF50',
            activeforeground='white'
        )
        self.position_menu.grid(row=4, column=1, pady=20, padx=20, sticky='w')

        self.watermark_button = Button(app, text='✨ Add Watermark & Save',
                                       bg=YELLOW, fg='#333333',
                                       font=FONT, command=self.add_watermark,  highlightbackground=YELLOW)
        self.watermark_button.grid(row=5, column=0, columnspan=2, pady=30, padx=20)

        self.status_label = Label(app, text='', bg=YELLOW, fg="#333333",
                                  font=('Arial', 12), wraplength=500)
        self.status_label.grid(row=6, column=0, columnspan=2, pady=20, padx=20)

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Choose your image",
            filetypes=(("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*"))
        )
        if file_path:
            self.image_path = file_path
            file_name = file_path.split('/')[-1]
            self.path_label.config(text=f"{file_name}")
            self.status_label.config(text='✅ Image loaded successfully!', fg='green')

    def get_position(self, width, height, text_width, text_height, position):
        """根據選擇返回文字位置"""
        margin = 60

        positions = {
            "Top Left": (margin, margin),
            "Top Right": (width - text_width - margin, margin),
            "Bottom Left": (margin, height - text_height - margin),
            "Bottom Right": (width - text_width - margin, height - text_height - margin)
        }

        return positions.get(position, (width - text_width - margin, height - text_height - margin))

    def add_watermark(self):
        watermark_text = self.text_entry.get()

        if not self.image_path:
            self.status_label.config(text='❌ Please choose an image first!', fg='red')
            return

        if not watermark_text:
            self.status_label.config(text='❌ Watermark text cannot be empty!', fg='red')
            return

        try:
            # 打開原圖
            image = Image.open(self.image_path).convert("RGBA")
            width, height = image.size

            # 創建透明層
            txt_layer = Image.new('RGBA', image.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(txt_layer)

            # 載入字體
            try:
                font_size = int(height / 25)
                font = ImageFont.truetype("font/ShinyCrystal-Yq3z4.ttf", font_size)
                print("Custom font loaded successfully!")
            except Exception as e:
                print(f"Font loading error: {e}")
                font = ImageFont.load_default()
                font_size = 30

            # 計算文字尺寸
            bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # 獲取位置
            position = self.position_var.get()
            x, y = self.get_position(width, height, text_width, text_height, position)

            # 獲取顏色
            color_choice = self.color_var.get()
            if color_choice == "White":
                text_color = (255, 255, 255, 255)
            else:  # Black
                text_color = (0, 0, 0, 255)

            # 繪製文字
            draw.text((x, y), watermark_text, font=font, fill=text_color)

            # 合併圖層
            watermarked = Image.alpha_composite(image, txt_layer)

            # 保存文件
            save_path = filedialog.asksaveasfilename(
                title="Save watermarked Image",
                defaultextension=".png",
                filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*"))
            )

            if save_path:
                if save_path.lower().endswith(('.jpg', '.jpeg')):
                    watermarked = watermarked.convert('RGB')
                watermarked.save(save_path, quality=95)

                self.status_label.config(
                    text=f"✅ Success! Saved to: {save_path.split('/')[-1]}",
                    fg="green"
                )
            else:
                self.status_label.config(text="⚠️ Save cancelled", fg="orange")

        except Exception as e:
            self.status_label.config(text=f"❌ Error: {str(e)[:50]}...", fg="red")
            print(f"Detailed Error: {e}")


if __name__ == '__main__':
    window = Tk()
    WatermarkingApp(window)
    window.mainloop()
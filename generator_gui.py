import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import os
from PIL import Image, ImageTk

def generate_booth(num_layouts, num_booths, booth_width, booth_height, padding, save_path):
    grid_size = 100

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    def create_layout():
        _, ax = plt.subplots(figsize=(12, 12))
        colors = ['#FFDD44', '#44BBFF', '#AA44FF', '#D2691E', '#4682B4', '#98FB98', '#FF6347', '#40E0D0']
        placed_booths = []

        def is_overlapping(new_booth):
            for existing_booth in placed_booths:
                if not (new_booth[0] + new_booth[2] <= existing_booth[0] or
                        new_booth[0] >= existing_booth[0] + existing_booth[2] or
                        new_booth[1] + new_booth[3] <= existing_booth[1] or
                        new_booth[1] >= existing_booth[1] + existing_booth[3]):
                    return True
            return False

        grid_positions = [(x, y) for x in range(0, grid_size - booth_width, booth_width + padding)
                          for y in range(0, grid_size - booth_height, booth_height + padding)]
        random.shuffle(grid_positions)

        booth_count = 0

        while booth_count < num_booths and grid_positions:
            start_x, start_y = grid_positions.pop()
            max_group_size = min(4, num_booths - booth_count)
            if max_group_size < 2:
                break
            group_size = random.randint(2, max_group_size)
            rows = 1
            cols = group_size
            if start_x + cols * (booth_width + padding) > grid_size or start_y + rows * (booth_height + padding) > grid_size:
                continue
            color = random.choice(colors)
            new_booth = (start_x, start_y, cols * (booth_width + padding), rows * (booth_height + padding))
            if not is_overlapping(new_booth):
                placed_booths.append(new_booth)
                for col in range(cols):
                    x = start_x + col * (booth_width + padding)
                    y = start_y
                    rect = patches.Rectangle((x, y), booth_width, booth_height, linewidth=1, edgecolor='black', facecolor=color, alpha=0.6)
                    ax.add_patch(rect)
                booth_count += group_size

        return booth_count >= num_booths, ax

    layout_num = 0
    while layout_num < num_layouts:
        valid = False
        for _ in range(100):
            valid, ax = create_layout()
            if valid:
                break
        if valid:
            ax.set_xlim(0, grid_size)
            ax.set_ylim(0, grid_size + 10)
            ax.axis('off')
            plt.savefig(os.path.join(save_path, f'data{layout_num}_{num_booths}.png'))
            plt.close()
            layout_num += 1
        else:
            print(f"레이아웃 생성 실패 {layout_num + 1}")

def select_save_path():
    selected_path = filedialog.askdirectory()
    if selected_path:
        entry_save_path.delete(0, tk.END)
        entry_save_path.insert(0, selected_path)

def run_generator():
    num_layouts = int(entry_num_layouts.get())
    num_booths = int(entry_num_booths.get())
    booth_width = int(entry_booth_width.get())
    booth_height = int(entry_booth_height.get())
    padding = int(entry_padding.get())
    save_path = entry_save_path.get()
    generate_booth(num_layouts, num_booths, booth_width, booth_height, padding, save_path)

root = tk.Tk()
root.title("부스 시뮬레이터")

# Add favicon
favicon_path = "C:/Users/User/Documents/rawdata/resources/turkey.ico"
root.iconbitmap(favicon_path)
# favicon = ImageTk.PhotoImage(Image.open(favicon_path))
# root.iconphoto(False, favicon)
# root.iconbitmap(False, favicon)

label_font = ('Malgun Gothic', 12)

ttk.Label(root, text="생성할 이미지 수:", font=label_font).grid(row=0, column=0, padx=10, pady=5, sticky='E')
entry_num_layouts = ttk.Entry(root)
entry_num_layouts.grid(row=0, column=1, padx=10, pady=5, sticky='EW')

ttk.Label(root, text="부스 수:", font=label_font).grid(row=1, column=0, padx=10, pady=5, sticky='E')
entry_num_booths = ttk.Entry(root)
entry_num_booths.grid(row=1, column=1, padx=10, pady=5, sticky='EW')

ttk.Label(root, text="각 부스의 가로 크기:", font=label_font).grid(row=2, column=0, padx=10, pady=5, sticky='E')
entry_booth_width = ttk.Entry(root)
entry_booth_width.grid(row=2, column=1, padx=10, pady=5, sticky='EW')

ttk.Label(root, text="각 부스의 세로 크기:", font=label_font).grid(row=3, column=0, padx=10, pady=5, sticky='E')
entry_booth_height = ttk.Entry(root)
entry_booth_height.grid(row=3, column=1, padx=10, pady=5, sticky='EW')

ttk.Label(root, text="부스 간 간격:", font=label_font).grid(row=4, column=0, padx=10, pady=5, sticky='E')
entry_padding = ttk.Entry(root)
entry_padding.grid(row=4, column=1, padx=10, pady=5, sticky='EW')

ttk.Label(root, text="이미지 저장 경로:", font=label_font).grid(row=5, column=0, padx=10, pady=5, sticky='E')
frame_save_path = ttk.Frame(root)
frame_save_path.grid(row=5, column=1, padx=10, pady=5, sticky='EW')
entry_save_path = ttk.Entry(frame_save_path)
entry_save_path.grid(row=0, column=0, sticky='EW')
btn_browse = ttk.Button(frame_save_path, text="찾아보기...", command=select_save_path)
btn_browse.grid(row=0, column=1, padx=5)

btn_generate = ttk.Button(root, text="생성하기", command=run_generator)
btn_generate.grid(row=6, columnspan=2, pady=10)

root.columnconfigure(1, weight=1)
frame_save_path.columnconfigure(0, weight=1)

root.mainloop()

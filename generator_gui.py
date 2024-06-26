import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import os
from threading import Thread
import matplotlib

matplotlib.use('Agg')

def generate_booth(num_layouts, num_booths, min_booth_width, max_booth_width, min_booth_height, max_booth_height, padding, save_path):
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

        def generate_random_booth_size():
            width = random.randint(min_booth_width, max_booth_width)
            height = random.randint(min_booth_height, max_booth_height)
            return width, height

        def get_group_position(group):
            if group == 'left':
                return 0, grid_size // 3
            elif group == 'center':
                return grid_size // 3, 2 * grid_size // 3
            elif group == 'right':
                return 2 * grid_size // 3, grid_size

        booth_count = 0
        groups = ['left', 'center', 'right']

        while booth_count < num_booths:
            random.shuffle(groups)
            for group in groups:
                start_x_min, start_x_max = get_group_position(group)
                if booth_count >= num_booths:
                    break
                width, height = generate_random_booth_size()
                grid_positions = [(x, y) for x in range(start_x_min, start_x_max - width, width + padding)
                                  for y in range(0, grid_size - height, height + padding)]
                random.shuffle(grid_positions)

                while grid_positions:
                    start_x, start_y = grid_positions.pop()
                    new_booth = (start_x, start_y, width, height)
                    if not is_overlapping(new_booth):
                        placed_booths.append(new_booth)
                        color = random.choice(colors)
                        rect = patches.Rectangle((start_x, start_y), width, height, linewidth=1, edgecolor='black', facecolor=color, alpha=0.6)
                        ax.add_patch(rect)
                        booth_count += 1
                        break

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
    min_booth_width = int(entry_min_booth_width.get())
    max_booth_width = int(entry_max_booth_width.get())
    min_booth_height = int(entry_min_booth_height.get())
    max_booth_height = int(entry_max_booth_height.get())
    padding = int(entry_padding.get())
    save_path = entry_save_path.get()
    btn_generate.config(state=tk.DISABLED, text="생성 중...")
    def task():
        generate_booth(num_layouts, num_booths, min_booth_width, max_booth_width, min_booth_height, max_booth_height, padding, save_path)
        root.after(0, lambda: btn_generate.config(state=tk.NORMAL, text="생성하기"))
    Thread(target=task).start()

root = tk.Tk()
root.title("부스 시뮬레이터")

label_font = ('Malgun Gothic', 12)

ttk.Label(root, text="생성할 이미지 수:", font=label_font).grid(row=0, column=0, padx=10, pady=5, sticky='E')
entry_num_layouts = ttk.Entry(root)
entry_num_layouts.grid(row=0, column=1, padx=10, pady=5, sticky='EW')

ttk.Label(root, text="부스 수:", font=label_font).grid(row=1, column=0, padx=10, pady=5, sticky='E')
entry_num_booths = ttk.Entry(root)
entry_num_booths.grid(row=1, column=1, padx=10, pady=5, sticky='EW')

ttk.Label(root, text="최소 부스 가로 크기:", font=label_font).grid(row=2, column=0, padx=10, pady=5, sticky='E')
entry_min_booth_width = ttk.Entry(root)
entry_min_booth_width.grid(row=2, column=1, padx=10, pady=5, sticky='EW')

ttk.Label(root, text="최대 부스 가로 크기:", font=label_font).grid(row=3, column=0, padx=10, pady=5, sticky='E')
entry_max_booth_width = ttk.Entry(root)
entry_max_booth_width.grid(row=3, column=1, padx=10, pady=5, sticky='EW')

ttk.Label(root, text="최소 부스 세로 크기:", font=label_font).grid(row=4, column=0, padx=10, pady=5, sticky='E')
entry_min_booth_height = ttk.Entry(root)
entry_min_booth_height.grid(row=4, column=1, padx=10, pady=5, sticky='EW')

ttk.Label(root, text="최대 부스 세로 크기:", font=label_font).grid(row=5, column=0, padx=10, pady=5, sticky='E')
entry_max_booth_height = ttk.Entry(root)
entry_max_booth_height.grid(row=5, column=1, padx=10, pady=5, sticky='EW')

ttk.Label(root, text="부스 간 간격:", font=label_font).grid(row=6, column=0, padx=10, pady=5, sticky='E')
entry_padding = ttk.Entry(root)
entry_padding.grid(row=6, column=1, padx=10, pady=5, sticky='EW')

ttk.Label(root, text="이미지 저장 경로:", font=label_font).grid(row=7, column=0, padx=10, pady=5, sticky='E')
frame_save_path = ttk.Frame(root)
frame_save_path.grid(row=7, column=1, padx=10, pady=5, sticky='EW')
entry_save_path = ttk.Entry(frame_save_path)
entry_save_path.grid(row=0, column=0, sticky='EW')
btn_browse = ttk.Button(frame_save_path, text="찾아보기...", command=select_save_path)
btn_browse.grid(row=0, column=1, padx=5)

btn_generate = ttk.Button(root, text="생성하기", command=run_generator)
btn_generate.grid(row=8, columnspan=2, pady=10)

root.columnconfigure(1, weight=1)
frame_save_path.columnconfigure(0, weight=1)

root.mainloop()

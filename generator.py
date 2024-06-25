'''
부스 이미지 generator.py
'''

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

# num_layouts를 통해서 이미지를 몇 개 생성할 것인지 지정(data{n} 형태로 생성되며, 같은 이름이 있으면 덮어써짐)
# num_booths를 조절해서 생성되는 부스의 수를 조절할 수 있음.
def generate_booth(num_layouts=25, num_booths=15):
    # booth_width와 booth_height로 부스의 크기 조절(각 부스에 다른 크기를 적용하는 것은 불가)
    booth_width = 7
    booth_height = 7
    
    # padding으로 부스 사이의 간격 조절
    padding = 3
    
    grid_size = 100
    
    for layout_num in range(1, num_layouts + 1):
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

        for _ in range(num_booths):
            attempts = 0
            max_attempts = 1000
            while attempts < max_attempts:
                rows = random.randint(1, 2)
                cols = random.randint(1, 4)
                if not grid_positions:
                    break
                start_x, start_y = grid_positions.pop()
                if start_x + cols * (booth_width + padding) > grid_size or start_y + rows * (booth_height + padding) > grid_size:
                    continue
                color = random.choice(colors)

                new_booth = (start_x, start_y, cols * (booth_width + padding), rows * (booth_height + padding))
                if not is_overlapping(new_booth):
                    placed_booths.append(new_booth)
                    for row in range(rows):
                        for col in range(cols):
                            x = start_x + col * (booth_width + padding)
                            y = start_y + row * (booth_height + padding)
                            rect = patches.Rectangle((x, y), booth_width, booth_height, linewidth=1, edgecolor='black', facecolor=color, alpha=0.6)
                            ax.add_patch(rect)
                    break

                attempts += 1

        ax.set_xlim(0, grid_size)
        ax.set_ylim(0, grid_size)
        ax.axis('off')
        plt.savefig(f'data{225 + layout_num}.png')
        plt.close()

generate_booth()
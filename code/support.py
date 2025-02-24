from settings import * 
from os import walk
from os.path import join

def import_image(*path, alpha = True, format = 'png'):
	full_path = join(*path) + f'.{format}'
	return pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()

def import_folder(*path):
    frames = []
    folder_path = os.path.join(*path)
    for folder_path, subfolders, image_names in os.walk(folder_path):
        for image_name in sorted(image_names, key=lambda name: int(name.split('.')[0]) if name.split('.')[0].isdigit() else float('inf')):
            full_path = os.path.join(folder_path, image_name)
            try:
                image_surf = pygame.image.load(full_path).convert_alpha()
                frames.append(image_surf)
            except pygame.error:
                pass
    return frames

def import_folder_dict(*path):
	frame_dict = {}
	for folder_path, _, image_names in walk(join(*path)):
		for image_name in image_names:
			full_path = join(folder_path, image_name)
			surface = pygame.image.load(full_path).convert_alpha()
			frame_dict[image_name.split('.')[0]] = surface
	return frame_dict

def import_sub_folders(*path):
    frame_dict = {}
    for _, sub_folders, __ in walk(join(*path)): 
        if sub_folders:
            for sub_folder in sub_folders:
                frame_dict[sub_folder] = import_folder(*path, sub_folder)
    return frame_dict
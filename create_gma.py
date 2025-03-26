import os, shutil
from PIL import Image


def create_gma(gmadexe, bsp, thumb, map_name, tags, nav=False):
    print('creating gma')

    def create_folder(folder):
        try:
            os.makedirs(folder, exist_ok=True)
            print(f"Folder '{folder}' created successfully.")
        except Exception as e:
            print(f"Error creating folder: {e}")

    def ossystem(command):
        print(f"{'-'*80}\nRunning command: {command}\n{'-'*80}")
        os.system(command)

    def resize_and_save_image_png(input_path, output_path, size=(512, 512)):
        try:
            img = Image.open(input_path)
            img = img.resize(size, Image.ANTIALIAS)
            # Save the image as PNG with no metadata
            img.save(output_path, format='PNG', optimize=True, quality=95)
            print(f"Image converted and saved at '{output_path}'")
        except Exception as e:
            print(f"Error: {e}")

    def delete_folder(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f"Folder '{folder_path}' and its contents deleted successfully.")
        except Exception as e:
            print(f"Error deleting folder: {e}")

    def resize_and_save_image_jpeg(input_path, output_path, size=(512, 512)):
        try:
            img = Image.open(input_path)
            img = img.resize(size, Image.ANTIALIAS)
            # Convert to RGB mode if image has transparency
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            # Save the image as JPEG with no metadata
            img.save(output_path, format='JPEG', optimize=True, quality=95)
            print(f"Image resized and saved at '{output_path}'")
        except Exception as e:
            print(f"Error: {e}")

    folder = os.popen(r'echo %TEMP%').read().replace('\n', '')
    folder = f'{folder}\\{map_name}'

    delete_folder(folder)

    folderworkshop = f'{folder}\\workshop'
    foldermapname = f'{folder}\\workshop\\{map_name}'
    foldermaps = f'{folder}\\workshop\\{map_name}\\maps'
    folderthumb = f'{folder}\\workshop\\{map_name}\\maps\\thumb'

    create_folder(folderthumb)

    ossystem(f'copy "{bsp}" "{foldermaps}\\{map_name}.bsp"')

    resize_and_save_image_png(thumb, f'{folderthumb}\\{map_name}.png')
    resize_and_save_image_jpeg(f'{folderthumb}\\{map_name}.png', f'{folderworkshop}\\{map_name}.jpeg')

    #ossystem(f'copy "{folderthumb}\\{map_name}.png" {folderworkshop}')

    with open(f'{foldermapname}\\addon.json', 'a') as f:
        f.write('{\n')
        f.write(f'"title" : "{map_name}",\n')
        f.write(f'"type" : "map",\n')
        f.write(f'"tags" : ["{tags[0]}", "{tags[1]}"],\n')
        f.write(f'"ignore" : []\n')
        f.write('}')

    command = [gmadexe, 'create', '-folder', f'"{foldermapname}"', '-out', f'"{foldermapname}.gma"']

    command = ' '.join(command)
    ossystem(command)

    return f'{foldermapname}.gma', f'{folderworkshop}\\{map_name}.jpeg'

from config import gmadexe, bsp, thumb, nav, map_name, tags

create_gma(gmadexe, bsp, thumb, map_name, tags, nav)

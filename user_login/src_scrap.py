import os
import glob

all_paths = []


def get_all_files_to_scrap(directory_path):
    global all_paths
    all_paths = []
    all_directories = scrap_src('/home/madmachines/pyprojects/CLAT/lms_videos/E_Lecture_and_assessment')
    all_directories += [directory_path]
    return get_html_xml_files_in_dir(all_directories)


def scrap_src(directory_path):
    remaining_dir_list = list_of_remaining_dir(directory_path)
    if len(remaining_dir_list) > 0:
        for child_dir in remaining_dir_list:
            global all_paths
            all_paths += [directory_path + '/' + child_dir]
            all_dir_in_a_dir(directory_path + '/' + child_dir)
    return all_paths


def all_dir_in_a_dir(directory_path):
    remaining_dir_list = list_of_remaining_dir(directory_path)
    if len(remaining_dir_list) > 0:
        for child_dir in remaining_dir_list:
            global all_paths
            all_paths += [directory_path + '/' + child_dir]
            scrap_src(directory_path + '/' + child_dir)
    else:
        pass


def list_of_remaining_dir(directory_path):
    return [name for name in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, name))]


def get_html_xml_files_in_dir(path_list):
    list_of_files = []
    for file_path in path_list:
        list_of_files += glob.glob1(file_path, '*.html')
        list_of_files += glob.glob1(file_path, '*.xml')
    return list_of_files
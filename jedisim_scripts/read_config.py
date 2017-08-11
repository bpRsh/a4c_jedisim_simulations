#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#


def config_dict(config_path):
    """Create a dictionary of variables from input file."""
    # imports
    import re

    # parse config file and make a dictionary
    with open(config_path, 'r') as f:
        config = {}
        string_regex = re.compile('"(.*?)"')
        value_regex = re.compile('[^ |\t]*')

        for line in f:
            if not line.startswith("#"):
                temp = []
                temp = line.split("=")
                if temp[1].startswith("\""):
                    config[temp[0]] = string_regex.findall(temp[1])[0]
                else:
                    config[temp[0]] = value_regex.findall(temp[1])[0]
    return config

# create config dictionary
config_path = 'physics_settings/bulge.conf'
# config_path = 'physics_settings/config1_original.conf'
config = config_dict(config_path)

# print config dictionary
for key, value in config.items():
    print (key, value)

print("\n")
print('{} {} {}'.format('len(config) = ', len(config), ''))
print(config['90_output_file'])
print(config['color_infile'])

# ==============================================================================
# make the filenames from the config parameters
# ==============================================================================
print("\n")
print(config['HST_image'])  # HST.fits
prefix = config['output_folder'] + config['prefix']  #


keys = ['HST_image',            'HST_convolved_image',
        'LSST_convolved_image', 'LSST_convolved_noise_image',
        'catalog_file',         'dislist_file',
        'distortedlist_file',   'convolvedlist_file']


for i in range(len(keys)):
    key = keys[i]
    config[key] = prefix + config[key]

print(config['HST_image'])  # out1/trial0_HST.fits

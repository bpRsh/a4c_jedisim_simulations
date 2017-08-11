# config file for jedimaster.py and associated programs
# a1.jedicolor    a2.jedicatalog
# b1.jedicolor    b2.jeditransform b3.jedidistort b4.jedipaste
# b5.jediconvolve b6.jedipaste     b7.jedirescale
# c1.jediaverage  c2.jedinoise     c3.jedinoise_10
#---------------------jedicolor------------------------------
# jedicolor will create simdatabase/f8_bulge_disk/f8_bulge_disk0.fits
# using input text files, i.e. scales bulge_f814w and disk_f818w galaxies
# jedicatalog will read MAG,MAG0,PIXSCALE,RADIUS from these files and
# will create three catalogs: out1/trial0_catalog.txt,convolved,distortedlist
color_infile="physics_settings/color.txt"
color_outfolder="simdatabase/bulge_disk_f8"
# jedicatalog will read these physics settings.
#---------------------physics settings-----------------------
nx=12288        		# x pixels            (arg for jedidistort)
ny=12288        		# y pixels            (arg for jedidistort)
pix_scale=0.03  		# arseconds per pixel (arg for jedidistort)
lens_z=0.3			    # lens redshift       (arg for jedidistort)
single_redshift=0		# 0 = not-fixed, 1=fixed
fixed_redshift=1.5		# the single source galaxy redshift to use
final_pix_scale=0.2		# LSST pixscale (arcsecords per pixel)
exp_time=6000			# exposure time in seconds
noise_mean=10			# mean for poisson noise
x_border=301    		# must be large enough so that no image can overflow_
y_border=301    		# must be large enough so that no image can overflow
x_trim=480			    # larger than x_border to ensure no edge effects
y_trim=480			    # larger than y_border to ensure no edge effects
num_galaxies=12420		# number of galaxies to simulate 138,000 default
min_mag=22      		# minimum magnitude galaxy to simulate (inclusive)
max_mag=28      		# maximum magnitude galaxy to simulate (inclusive)
power=0.33      		# power for the power law galaxy distribution
#--------------------psf and lenses--------------------------
# lens.txt has a single line with 5 parameters
# 6144 6144 1 1000.000000 4.000000
#  x    y  type p1       p2
#  x - x center of lens (in pixels)
#  y - y center of lens (in pixels)
#  type - type of mass profile
#         1. Singular isothermal sphere
#         2. Navarro-Frenk-White profile
#	       3. NFW constant distortion profile for grid simulations
#  p1 - first profile parameter
#         1. sigma_v [km/s]
#         2. M200 parameter [10^14 solar masses]
#		  3. Distance to center in px. M200 fixed at 20 default, which can be modified in case 3
#  p2 - second profile parameter
#         1. not applicable, can take any numerical
#         2. c parameter [unitless]
#         3. c parameter [unitless]
lenses_file="physics_settings/lens.txt"	  # arg for jedidistort
psf_file="physics_settings/psf.txt"       # psf for
90_psf_file="physics_settings/psf.txt"    # psf for
#--------------------output settings--------------------------
output_folder="out1/"  # jedicatalog etc.
prefix="trial0_"       # jedicatalog etc.
sign="!"               # jedicolor
HST_image="HST.fits"
HST_convolved_image="HST_convolved.fits"
LSST_convolved_image="LSST_convolved.fits"
LSST_convolved_noise_image="LSST_convolved_noise.fits"
output_file="physics_settings/out.txt"
90_output_file="physics_settings/90_out.txt"
#-----------database folders----------------------------------
# There are 10 radius database files 20.dat to 29.dat.
# which contains min and max radius to be used by jedicatalog.
# e.g. the file simdatabase/radius_db/20.dat has two lines: 36.72 3.51
# This must contain files "n.txt" for n= min_mag to max_mag
radius_db_folder="simdatabase/radius_db/"
# There are 15+2 redshift database files 19.dat to 33.dat with +- 99.dat.
# which contains min and max redshift to be used by jedicatalog.
# e.g. the file simdatabase/red_db/19.dat has two lines: 0.301000 0.138000
red_db_folder="simdatabase/red_db/"
#-----------catalog files for jedicatalog -----------------------------
# jedicatalog will write:
# name,x,y,angle,redshift,pixscale,old_mag,old_rad,new_mag,new_rad,stamp_name,dis_name
# in the out1/trial0_catalog.txt
# jedicatalog also creates out1/trial0_convolvedlist.txt
# which has 6 lines like: out1/convolved/convolved_band_0.fits
# jedicatalog also creates out1/trial0_distortedlist.txt
# it has 0-12 folders and 1000 fitsfiles (total: 12420 files)
# line     1: out1/distorted_0/distorted_0.fits
# line 12420: out1/distorted_12/distorted_12419.fits
catalog_file="catalog.txt"
convolvedlist_file="convolvedlist.txt"
distortedlist_file="distortedlist.txt"
#-----------catalog files for jedidistort -----------------------------
# jeditransform creates out1/trial0_dislist.txt along with 12420 .gz stamps
# jedidistort will use these files.
# Input galaxy parameter file for jedidistort: x y nx ny zs file
#           x - x coord. of lower left pixel where galaxy should be embedded
#           y - y coord. of lower left pixel where galaxy should be embedded
#           nx - width of the galaxy in pixels
#           ny - height of the galaxy in pixels
#           zs - redshift of this galaxy
#           infile - filepath to the FITS file for this galaxy, 1024 chars max
#           outfile - filepath for the output FITS file for this galaxy, 1024 chars max
#
#  e.g. out1/trial0_dislist.txt looks like this: (was created by jeditransform)
# 6813 888 10 23 1.500000 out1/stamp_0/stamp_.fits.gz out1/distorted_0/distorted_0.fits
# x    y   nx ny zs       infile                      outfile
dislist_file="dislist.txt"  # arg for jedidistort
convlist_file="toconvolvelist.txt"
#-----------source images-------------------------------------
num_source_images=302
# jedicolor scales bulge_f814w and disk_f814w galaxies and writes these files.
# jedicatalog will read MAG, MAG0, PIXSCALE, RADIUS from these files.
# jedicatalog will write these names in out1/trial0_catalog.txt
# Required headers:
# MAG      : magnitude of the postage stamp image
# MAG0     : magnitude zeropoint of the postage stamp image
# PIXSCALE : pixel scale of the postage stamp image
# RADIUS   : R50 radius of the image, in pixels
image="simdatabase/bulge_disk_f8/f8_bulge_disk0.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk1.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk2.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk3.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk4.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk5.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk6.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk7.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk8.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk9.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk10.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk11.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk12.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk13.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk14.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk15.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk16.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk17.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk18.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk19.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk20.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk21.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk22.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk23.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk24.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk25.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk26.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk27.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk28.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk29.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk30.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk31.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk32.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk33.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk34.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk35.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk36.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk37.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk38.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk39.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk40.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk41.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk42.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk43.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk44.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk45.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk46.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk47.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk48.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk49.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk50.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk51.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk52.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk53.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk54.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk55.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk56.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk57.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk58.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk59.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk60.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk61.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk62.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk63.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk64.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk65.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk66.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk67.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk68.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk69.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk70.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk71.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk72.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk73.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk74.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk75.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk76.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk77.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk78.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk79.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk80.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk81.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk82.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk83.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk84.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk85.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk86.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk87.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk88.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk89.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk90.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk91.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk92.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk93.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk94.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk95.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk96.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk97.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk98.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk99.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk100.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk101.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk102.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk103.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk104.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk105.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk106.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk107.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk108.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk109.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk110.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk111.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk112.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk113.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk114.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk115.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk116.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk117.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk118.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk119.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk120.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk121.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk122.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk123.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk124.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk125.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk126.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk127.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk128.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk129.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk130.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk131.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk132.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk133.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk134.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk135.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk136.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk137.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk138.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk139.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk140.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk141.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk142.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk143.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk144.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk145.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk146.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk147.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk148.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk149.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk150.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk151.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk152.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk153.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk154.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk155.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk156.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk157.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk158.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk159.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk160.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk161.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk162.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk163.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk164.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk165.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk166.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk167.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk168.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk169.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk170.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk171.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk172.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk173.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk174.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk175.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk176.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk177.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk178.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk179.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk180.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk181.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk182.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk183.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk184.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk185.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk186.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk187.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk188.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk189.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk190.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk191.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk192.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk193.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk194.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk195.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk196.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk197.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk198.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk199.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk200.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk201.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk202.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk203.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk204.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk205.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk206.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk207.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk208.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk209.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk210.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk211.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk212.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk213.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk214.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk215.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk216.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk217.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk218.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk219.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk220.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk221.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk222.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk223.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk224.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk225.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk226.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk227.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk228.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk229.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk230.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk231.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk232.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk233.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk234.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk235.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk236.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk237.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk238.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk239.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk240.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk241.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk242.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk243.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk244.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk245.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk246.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk247.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk248.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk249.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk250.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk251.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk252.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk253.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk254.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk255.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk256.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk257.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk258.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk259.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk260.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk261.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk262.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk263.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk264.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk265.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk266.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk267.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk268.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk269.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk270.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk271.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk272.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk273.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk274.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk275.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk276.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk277.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk278.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk279.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk280.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk281.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk282.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk283.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk284.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk285.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk286.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk287.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk288.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk289.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk290.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk291.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk292.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk293.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk294.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk295.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk296.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk297.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk298.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk299.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk300.fits"
image="simdatabase/bulge_disk_f8/f8_bulge_disk301.fits"

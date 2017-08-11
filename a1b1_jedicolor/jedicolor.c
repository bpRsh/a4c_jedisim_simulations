/* Author    : Bhishan Poudel
 * Date      : Jul 19, 2016
 * Update    : Sep 17, 2016
 *
 * Compile   : gcc -o jedicolor jedicolor.c -lm -lcfitsio
 * Run       : ./jedicolor jedisim_out/color_out/color0.txt 20.0
 *
 * Command   : gcc -o jedicolor jedicolor.c -lm -lcfitsio  && ./jedicolor jedisim_out/color_out/color0.txt 20.0
 *
 *
 * Depends   : ~/jedisim/simdatabase/colors/*.fits (101 blue and red galaxies as from color.txt)
 *                                                 ( f606w_gal0_to_100.fits and f814w*)
 *
 * Output    : jedisim_out/color_out/color_out0/blue_red_0_to100.fits
 *
 * Algorithm : pix3[ii] = (1-m) * pix1[ii]  +  m * pix2[ii] ;
 *
 * Info      : This program reads in two fitsfiles from input directory,
 *             applies the algorithm and create one output fitsfile.
 *
 *             e.g. input  1: ~/jedisim/simdatabase/colors/f606w_gal0.fits
 *                  input  1: ~/jedisim/simdatabase/colors/f814w_gal0.fits
 *                  output 1: jedisim_out/color_out/color_out0/blue_red_0.fits
 */

#include <stdio.h>
#include <string.h>
#include "fitsio.h"

int main(int argc,char *argv[]){

// variables
int check =1;
int status = 0;
int n=0;
double m;
char s[101][101];
char t[101][101];
char y[101][101];
//char z[101][101];

fitsfile *in1[101]; //fits file for reading red images
fitsfile *in2[101]; //fits file for reading blue images
fitsfile *out[101]; //fitsfile for reading output images

long   anaxes1[3]  = {1,1,1};
long   anaxes2[3]  = {1,1,1};
int    anaxis1     = 0;
int    anaxis2     = 0;
long   npixels     = 1;
long   firstpix[3] = {1,1,1};
long   bitpix      = -32;
int    ii;

m = atof(argv[2]) / 1.0;  // if divisor is 1.0, pass /20 in jedimaster.py
printf("The factor m =  %f\n\n",m);
FILE *fp;

fp = fopen(argv[1],"r");


//==============================================================================
// note: input file argv[1] should have n=101 lines
for(n=0;n<=100;n++){

    fscanf(fp,"%s %s %s",s[n],t[n],y[n]);
    
    // prepend ! sign
    //strcpy(z[n],"!");
    //strcat(z[n],y[n]);

    // print lines of input file
    printf("%d: \t%s \t%s \t%s\n",n,s[n],t[n],y[n]);
}
//==============================================================================


// for loop of input file (101 lines)
for(n=0;n<=100;n++){
    fits_open_file(&in1[n],s[n],READONLY,&status); // reading blue  files
    //printf("%d %s\n",status,s[n]);

    fits_open_file(&in2[n],t[n],READONLY,&status); //reading red files
    //printf("%d %s\n",status,t[n]);


    if (status) {
       fits_report_error(stderr, status);
       return(status);
    }

    fits_get_img_dim(in1[n],&anaxis1,&status);
    fits_get_img_dim(in2[n],&anaxis2,&status);
    fits_get_img_size(in1[n],3,anaxes1,&status);
    fits_get_img_size(in1[n],3,anaxes2,&status);

    //printf("%ld %ld\n",anaxes1[0],anaxes2[0]); // no. of pixels in each axis
    //printf("%d\n",anaxis2); // total no. of axis(suppose x,y or z)

    if(check && !fits_create_file(&out[n],y[n],&status)){
        fits_copy_header(in1[n],out[n],&status);

        npixels = anaxes1[0];
        //printf("the value of npixels is %ld\n",npixels);

        double *pix1,*pix2,*pix3;

        pix1 = (double*)malloc(npixels*sizeof(double));
        pix2 = (double*)malloc(npixels*sizeof(double));
        pix3 = (double*)malloc(npixels*sizeof(double));

        if(pix1==NULL|| pix2==NULL){
            printf("Memory allocation error\n");
            return(1);
        }

        //printf("%ld\n",npixels);

        for(firstpix[2]=1;firstpix[2]<=anaxes1[2];firstpix[2]++){
            for(firstpix[1]=1;firstpix[1]<=anaxes1[1];firstpix[1]++){
                if(fits_read_pix(in1[n],TDOUBLE,firstpix,npixels,NULL,pix1,NULL,&status))  break;
                if(fits_read_pix(in2[n],TDOUBLE,firstpix,npixels,NULL,pix2,NULL,&status))  break;

                for(ii=0;ii<npixels;ii++){
                        // pix1[ii] += pix2[ii];
                        pix3[ii] = ( ( m*pix1[ii])+( (1-m) *pix2[ii]);
                } //for loop of ii

            fits_update_key(out[n],TLONG,"BITPIX",&bitpix,0,&status);
            fits_write_pix(out[n],TDOUBLE,firstpix,npixels,pix3,&status);

            } //end of for loop of firstpix[2]
        } // end of for loop of firstpix[1]


    free(pix1);
    free(pix2);
    free(pix3);
    fits_close_file(out[n],&status);
    } // end of check

    fits_close_file(in1[n],&status);
    fits_close_file(in2[n],&status);
} // end of for loop of line from input text file

m=0;
fclose(fp);
return 0;
} // end of main

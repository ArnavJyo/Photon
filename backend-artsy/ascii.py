from  PIL  import  ( 
    Image ,  
    ImageOps ,  
    ImageFont ,  
    ImageDraw 
)
import  numpy  as  np
symbols  =  list ( "!@#%¨&*()-_=+ {} []<>^~,.:;?|" ) 
symbols  +=  [ chr ( e )  for  e  in  range ( ord ( "a" ),  ord ( "z" )  +  1 )] 
symbols  +=  [ chr ( e )  for  e  in  range ( ord ( "A" ),  ord ( "Z" )  +  1 )] 
symbols  +=  list ( "0123456789" ) 
N  =  len ( symbols )
open ( "Roboto-Regular.ttf", "wb" ) 
# Raster symbol set parameters 
S ,  T  =  32 ,  32  # raster sizes

# Create raster symbol set 
SYMBOLS  =  np . zeros (( N ,  T ,  S )) 
for  i ,  e  in  enumerate ( symbols ): 
    image  =  Image . fromarray ( np . zeros (( S ,  S ))) 
    draw  =  ImageDraw . Draw ( image ) 
    font  =  ImageFont . truetype ( "Roboto-Regular.ttf" ,  S ) 
    draw . text (( S / 2 ,  S / 2 ),  e ,  anchor = "mm" ,  font = font ) 
    SYMBOLS [ i ]  =  np . asarray ( image )
def ASCII(img_path):
    IMAGE_RGB  =  Image . open ( img_path )

    # Histogram equalization 
    IMAGE_RGB  =  ImageOps . equalize ( IMAGE_RGB )

    # Convert to HSV 
    IMAGE_HSV  =  IMAGE_RGB . convert ( "HSV" )

    m ,  n  =  80 ,  40  # number of ascii symbols per axis
# Resize input image based on inputs 
    IMAGE_  =  IMAGE_HSV . resize (( m * S ,  n * T )) 
    IMAGE_  =  np . asarray ( IMAGE_ ) / 255

    # Build ascii conversions 
    OUTPUT  =  [[{ "chr" :  "" ,  "hue" :  "" }  for  _  in  range ( m )]  for  _  in  range ( n )] 
    for  j ,  ROW  in  enumerate ( OUTPUT ): 
        for  i ,  e  in  enumerate ( ROW ): 
            image  =  IMAGE_ [ j * S :( j + 1 ) * S ,  i * S :( i + 1 ) * S ,  2 ] 
            diff  =  np . power ( SYMBOLS  -  image ,  2 ) . reshape (( N ,  - 1 )) 
            OUTPUT [ j ][ i ][ "chr" ]  =  symbols [ np . argmin ( diff . sum ( axis = 1 ))] 
            block_hue  =  int ( np . median ( IMAGE_ [ j * S :( j + 1 ) * S ,  i * S :( i + 1 ) * S ,  0 ]) * 360 ) 
            block_sat  =  int ( np . median ( IMAGE_ [ j * S :( j + 1 ) * S ,  i * S :( i + 1 ) * S ,  1 ]) * 100 ) 
            block_val  =  int ( np . median (IMAGE_ [ j * S :( j + 1 ) * S ,  i * S :( i + 1 ) * S ,  2 ]) * 100 ) 
            OUTPUT [ j ][ i ][ "color" ]  =  f'hsl( { block_hue } , { block_sat } %, { block_val } %)'
    return OUTPUT
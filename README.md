# Labl.it
Image dataset labeling utility for image classification tasks

Main script at [link](https://github.com/muzzart/Labl.it/blob/master/Labl.it/App/main.py)


usage: main.py [-h] -k KEYWORDS -c CLASSES -s SHORTCUTS [-f FILENAME]


optional arguments:

  -h, --help            show this help message and exit
  
  -k KEYWORDS, --keywords KEYWORDS
  
                        keywords in url to be found, must be comma-separted if
                        
                        more than 1 Eg. class1,positve,png or
                        
                        class2,negative,jpg
                        
  -c CLASSES, --classes CLASSES
  
                        names of target classes to be used, must be comma-
                        
                        separted and mentioned ordinally (as we'll use 0 for
                        
                        first class, 1 for second and so on) . Eg. dog,cat or
                        
                        abnormal,normal
                        
  -s SHORTCUTS, --shortcuts SHORTCUTS
  
                        keyboard shortcuts to be used to trigger label
                        
                        buttons, must be comma-separted and in same order as
                        
                        the classes in -c argument. Eg. d,g (for dog,cat) or
                        
                        a,n (for abnormal,normal)
                        
  -f FILENAME, --filename FILENAME
  
                        filename used to save the final label files, filename
                        
                        must be given without extension (mylabel for
                        
                        mylabels.csv). if this argument is empty, default name
                        
                        is "labels.csv"
